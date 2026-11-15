"""Video parser: every pass writes its own file, deterministic code assembles them into evidence.json, timeline.md and timeline.html.

python run.py [--variant low] [--force speech,screens,events] [--no-speech] [<lang>/<id> ...]

out/<lang>/<id>/parsed[-variant]/
  run.json          video hash, pass versions, timings
  10-speech.json    utterances and word timings
  30-screens.json   stable screen states: time, key frame, OCR text
  60-events.json    what appeared, disappeared, changed
  70-links.json     what a phrase refers to on the screen
  80-speakers.json  meeting tiles and who spoke: the lit tile during each utterance
  90-slides.json    which slide was on screen when; how attached pdf/pptx differ from what was shown
  95-checks.json    cross-checks: an error nobody mentions, a value that went back, a change behind the front window, claims
  evidence.json     everything together, for machines
  timeline.md       timeline for an agent
  timeline.html     timeline with frames, for a human
  frames/           state key frames and event cut-outs
A pass is skipped when the video and the pass version match run.json.
"""
import argparse
import hashlib
import json
import time
from pathlib import Path

from vrp import checks as checks_pass
from vrp import events as ev_pass
from vrp import links as links_pass
from vrp import slides as slides_pass
from vrp import speakers as speakers_pass
from vrp import screen as screen_pass
from vrp.format import SCHEMA
from vrp.timeline import crops, render_html, render_md

OUT = Path(__file__).resolve().parents[1] / "out"
FILES = {"speech": "10-speech.json", "screens": "30-screens.json", "events": "60-events.json", "links": "70-links.json", "speakers": "80-speakers.json", "slides": "90-slides.json", "checks": "95-checks.json"}
VERSIONS = {"speech": 2, "screens": 7, "events": 22, "links": 4, "speakers": 1, "slides": 2, "checks": 5}


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()[:16]


def dump(path: Path, data) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=1))


def apply_speakers(evidence: dict, who: dict) -> None:
    """Utterances get the lit tile; the speaker is the person if they introduced themselves, else the tile."""
    if not who["tiles"]:
        return
    speakers: dict[str, dict] = {}
    for u in evidence["speech"]["utterances"]:
        a = who["utterances"].get(u["id"])
        if not a:
            continue
        u["tile"] = a["tile"]
        u["speaker"] = a["person"] or a["tile"]
        speakers.setdefault(u["speaker"], {"id": u["speaker"], "name": a["person"] or (a["tile"] if a["tile"] in {t["name"] for t in who["tiles"]} else None), "tile": a["tile"]})
    evidence["speech"] = {**evidence["speech"], "speakers": list(speakers.values())}


def run(key: str, variant: str | None, force: set[str], no_speech: bool = False) -> dict:
    lang = key.split("/")[0]
    video = OUT / (f"{key}.{variant}.mp4" if variant else f"{key}.mp4")
    work = OUT / key / (f"parsed-{variant}" if variant else "parsed")
    work.mkdir(parents=True, exist_ok=True)
    rj = work / "run.json"
    prev = json.loads(rj.read_text()).get("passes", {}) if rj.exists() else {}
    vhash = sha(video)
    passes, timing = {}, {}

    def step(name: str, upstream: str, compute):
        key = f"{vhash}:{VERSIONS[name]}:{upstream}"
        passes[name] = {"version": VERSIONS[name], "key": key}
        path = work / FILES[name]
        t0 = time.time()
        if name not in force and prev.get(name, {}).get("key") == key and path.exists():
            data = json.loads(path.read_text())
        else:
            data = compute()
            dump(path, data)
        timing[name] = round(time.time() - t0, 1)
        return data

    def speech():
        from vrp.speech import transcribe

        return transcribe(video, work, lang)

    def screens():
        for f in (work / "frames").glob("*.jpg"):
            f.unlink()
        segs, meta, track = screen_pass.scan(video, work / "frames")
        region = meta["regions"]["screen"]
        ev_pass.setup(work, meta, track)
        raw = [
            {"id": f"s{i + 1:03d}", "start_ms": s["start_ms"], "end_ms": s["end_ms"], "frame": str(Path(s["frame"]).relative_to(work)), "texts": screen_pass.ocr(s["frame"], lang, region)}
            for i, s in enumerate(segs)
        ]
        return {"meta": meta, "raw": len(raw), "screens": ev_pass.merge_same(raw), "cursor": track}

    # --no-speech: screen passes only (a heavy model may be busy with other work); the speech pass is left as it was
    cached = work / FILES["speech"]
    sp = (json.loads(cached.read_text()) if cached.exists() else {"speakers": [], "utterances": []}) if no_speech else step("speech", "", speech)
    if no_speech and prev.get("speech"):
        passes["speech"] = prev["speech"]
    sc = step("screens", "", screens)
    meta = sc["meta"]

    def events():
        ev_pass.setup(work, meta, sc["cursor"])
        screen_events = ev_pass.diff(sc["screens"])
        cursor_events = ev_pass.cursor_events(sc["cursor"], meta.get("cursor_scale"), sc["screens"], screen_events, meta["duration_ms"])
        screen_events = ev_pass.drop_under_hover([e for e in screen_events if not e.get("under_cursor")], cursor_events, sc["cursor"])
        out = sorted(screen_events + cursor_events, key=lambda e: (e["t_ms"], e["kind"]))
        for i, e in enumerate(out):
            e["id"] = f"p{i + 1:03d}"
        return out

    events = step("events", passes["screens"]["key"], events)

    evidence = {
        "schema": SCHEMA,
        "video": {"file": video.name, **{k: v for k, v in meta.items() if k != "regions"}},
        "regions": [{"id": rid, "bbox": box} for rid, box in meta["regions"].items() if box],
        "speech": sp,
        "screens": sc["screens"],
        "events": events,
        "links": [],  # filled below
        "slides": [],
        "findings": {},
    }
    if not no_speech:
        who = step("speakers", passes["speech"]["key"], lambda: speakers_pass.assign(video, sp["utterances"], lang))
        apply_speakers(evidence, who)
    attached = sorted((OUT / key / "attachments").glob("*.p*")) if (OUT / key / "attachments").exists() else []

    def slides():
        shown, words = slides_pass.shown(sc["screens"])
        return {"shown": shown, "attachments": slides_pass.compare(attached, words)}

    sl = step("slides", passes["screens"]["key"] + "|" + ",".join(f.name for f in attached), slides)
    evidence["slides"], evidence["attachments"] = sl["shown"], sl["attachments"]
    evidence["links"] = step("links", f'{passes.get("speech", {}).get("key")}|{passes["events"]["key"]}', lambda: links_pass.build(evidence, lang))
    evidence["checks"] = step("checks", f'{passes.get("speech", {}).get("key")}|{passes["events"]["key"]}|{no_speech}', lambda: checks_pass.build(evidence, work, lang, speech=not no_speech))
    crops(evidence, work)
    dump(work / "evidence.json", evidence)
    title = f"{key}{' · ' + variant if variant else ''}"
    (work / "timeline.md").write_text(render_md(evidence, title))
    (work / "timeline.html").write_text(render_html(evidence, title, video_src=f"../../{video.name}"))
    dump(rj, {"video": video.name, "video_sha": vhash, "passes": passes, "timing_sec": timing})
    return evidence


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("ids", nargs="*")
    ap.add_argument("--variant")
    ap.add_argument("--force", default="", help="comma-separated passes to recompute")
    ap.add_argument("--no-speech", action="store_true", help="skip the speech pass")
    a = ap.parse_args()
    keys = a.ids or sorted(f"{p.parts[-4]}/{p.parts[-3]}" for p in OUT.glob("*/*/truth/evidence.json"))
    for key in keys:
        ev = run(key, a.variant, set(filter(None, a.force.split(","))), a.no_speech)
        print(f"{key}: states {len(ev['screens'])}, events {len(ev['events'])}, utterances {len(ev['speech']['utterances'])}", flush=True)
