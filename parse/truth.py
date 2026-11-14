"""Generator ground truth (out/<lang>/<id>/truth/*.json) -> evidence.json in the parser format.

python truth.py [<lang>/<id> ...]   no arguments - every built scenario
"""
import json
import sys
from pathlib import Path

from vrp.format import SCHEMA
from vrp.timeline import render_html, render_md

OUT = Path(__file__).resolve().parents[1] / "out"
# containers that OCR never sees as a separate text
CONTAINERS = {"list", "slide", "column", "panel", "menu", "listbox", "breadcrumb", "header"}


def load(d: Path, name: str):
    p = d / "truth" / name
    return json.loads(p.read_text()) if p.exists() else None


def convert(sid: str) -> dict:
    d = OUT / sid
    man = json.loads((d / "manifest.json").read_text())
    states = load(d, "ui-states.json")
    timeline = load(d, "timeline.json")
    speakers = load(d, "speakers.json") or []
    transcript = load(d, "transcript.json")
    links = load(d, "links.json")
    report = load(d, "report.json")
    reqs = load(d, "requirements.json")
    slides = load(d, "slides.json")

    def state_at(t: int):
        for s in states:
            if s["start_ms"] <= t < s["end_ms"]:
                return s
        return states[-1]

    def element(el: str, t: int):
        for e in state_at(t)["elements"]:
            if e["id"] == el:
                return e
        return None

    label = {s["id"]: s["label"] for s in speakers}
    ev_out, by_truth = [], {}

    def add(truth_id, **e):
        e["id"] = f"e{len(ev_out) + 1:03d}"
        e.setdefault("end_ms", None)
        e.setdefault("visible", True)
        e.update(source="truth", evidence=[])
        ev_out.append(e)
        for tid in truth_id if isinstance(truth_id, list) else [truth_id]:
            by_truth.setdefault(tid, []).append(e["id"])

    for x in timeline:
        if x["kind"] == "action" and x["actor"] == "user":
            el = element(x["target"], x["t_ms"] - 1) if x.get("target") else None
            kind = {"click": "click", "focus_window": "click", "point": "point", "key": "key", "type_text": "type"}.get(x["type"])
            if not kind:
                continue
            add(
                x["event_id"],
                t_ms=x["t_ms"],
                end_ms=x["t_ms"] + x["duration_ms"] if x.get("duration_ms") else None,
                kind=kind,
                bbox=el["bbox"] if el else None,
                text=x.get("text") or x.get("key") or (el["text"] if el else x.get("target_text")),
            )
        elif x["kind"] == "ui_change":
            t = x["t_ms"]
            if x["type"] == "element_added" and x["role"] not in CONTAINERS:
                add(x["caused_by"], t_ms=t, end_ms=t + x["visible_for_ms"], kind="appear", bbox=x["bbox"], text=x["text"], visible=x["visibility"] == "visible")
            elif x["type"] == "element_removed" and x["role"] not in CONTAINERS:
                prev = element(x["target"], t - 1)
                add(x["caused_by"], t_ms=t, kind="disappear", bbox=prev["bbox"] if prev else None, text=x["text"], visible=bool(prev and prev["visibility"] == "visible"))
            elif x["type"] == "text_changed":
                el = element(x["target"], t)
                if el and el["role"] not in CONTAINERS:
                    add(x["caused_by"], t_ms=t, kind="text_change", bbox=el["bbox"], text=x["after"], before=x["before"], after=x["after"], visible=el["visibility"] == "visible")
            elif x["type"] == "z_order_changed":
                top = x["after"][-1]
                w = next((w for w in state_at(t)["windows"] if w["id"] == top), None)
                add(x["caused_by"], t_ms=t, kind="window_change", bbox=w["bbox"] if w else None, text=w["title"] if w else top)

    shown = []
    if slides:
        for s in slides["shown"]:
            title = next((e["text"] for e in state_at(s["start_ms"])["elements"] if e["id"].endswith("/slide/title")), "")
            shown.append({"index": s["index"], "title": title, "start_ms": s["start_ms"], "end_ms": s["end_ms"]})
            if s["start_ms"] > 0:
                add([], t_ms=s["start_ms"], kind="screen_change", bbox=None, text=title)

    ev_out.sort(key=lambda e: e["t_ms"])

    screens = [
        {
            "id": s["state_id"],
            "start_ms": s["start_ms"],
            "end_ms": s["end_ms"],
            "frame": None,
            "texts": [{"bbox": e["bbox"], "text": e["text"]} for e in s["elements"] if e["visibility"] == "visible" and e["text"] and e["role"] not in CONTAINERS],
        }
        for s in states
    ]

    out_links = []
    for ln in links:
        tgt = None
        if ln["target"] != "unresolved":
            el = element(ln["target"], ln["end_ms"] if ln["relation"] == "mentions" else ln["start_ms"])
            tgt = {"bbox": el["bbox"], "text": el["text"]} if el else {"bbox": None, "text": ln["target_text"]}
        out_links.append({"utterance": ln["utterance"], "phrase": ln["phrase"], "start_ms": ln["start_ms"], "end_ms": ln["end_ms"], "target": tgt, "relation": ln["relation"]})

    def ev_ids(ref: dict) -> list[str]:
        if "event_id" in ref:
            return by_truth.get(ref["event_id"], [])
        if "utterance" in ref:
            return [ref["utterance"]]
        return []

    findings = {}
    if report:
        findings["bug"] = {
            "title": report["title"],
            "kind": report["class"],
            "steps": [{"t_ms": s["t_ms"], "action": s["action"], "target_text": s["target_text"] or s.get("text") or s.get("key"), "window": s["window_title"]} for s in report["steps"]],
            "expected": report["expected"],
            "actual": report["actual"],
            "key_events": sorted({i for c in report["critical"] for i in ev_ids(c)}),
            "claims": [],
        }
    if reqs:
        findings["requirements"] = [
            {
                "id": r["id"],
                "text": r["text"],
                "status": r["status"],
                "proposed_by": label.get(r.get("proposed_by"), r.get("proposed_by")),
                "decided_by": label.get(r.get("decided_by"), r.get("decided_by")),
                "evidence": [i for e in r["evidence"] for i in ev_ids(e)],
            }
            for r in reqs
        ]

    master = man["variants"][0]
    return {
        "schema": SCHEMA,
        "video": {"file": master["file"], "width": man["frame"]["w"], "height": man["frame"]["h"], "fps": master["fps"], "duration_ms": man["duration_ms"]},
        "regions": [{"id": "screen", "bbox": man["regions"]["screen"]}] + ([{"id": "people", "bbox": man["regions"]["people"]}] if man["regions"]["people"] else []),
        "speech": {
            "speakers": [{"id": s["label"], "name": s["name_on_video"], "tile": s["tile_name"]} for s in speakers],
            "utterances": [{"id": u["id"], "speaker": label.get(u["speaker_id"], u["speaker_id"]), "start_ms": u["start_ms"], "end_ms": u["end_ms"], "text": u["text"], "words": u["words"]} for u in transcript],
        },
        "screens": screens,
        "events": ev_out,
        "links": out_links,
        "slides": shown,
        "findings": findings,
        "traps": man.get("traps", []) + (report or {}).get("traps", []),
        # ground truth only: critical moments of the scenario and the events, any of which confirms it
        "critical": [
            {"name": c["name"], "t_ms": c["t_ms"], "events": [i for i in ev_ids(c) if i.startswith("e") and next(e for e in ev_out if e["id"] == i)["kind"] != "disappear"] or ev_ids(c)}
            for c in (report or {}).get("critical", []) if "event_id" in c or "utterance" in c
        ],
    }


if __name__ == "__main__":
    keys = sys.argv[1:] or sorted(f"{p.parts[-3]}/{p.parts[-2]}" for p in OUT.glob("*/*/manifest.json"))
    for key in keys:
        ev = convert(key)
        name = key.split("/")[1]
        (OUT / key / "truth" / "evidence.json").write_text(json.dumps(ev, ensure_ascii=False, indent=1))
        (OUT / key / "truth" / "timeline.md").write_text(render_md(ev, f"{key} · ground truth"))
        (OUT / key / "truth" / "timeline.html").write_text(render_html(ev, f"{key} · ground truth", video_src=f"../../{name}.mp4"))
        print(f"{key}: {len(ev['events'])} events, {len(ev['speech']['utterances'])} utterances, {len(ev['critical'])} critical moments")
