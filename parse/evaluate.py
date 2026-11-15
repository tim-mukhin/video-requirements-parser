"""Parser evaluation against ground truth: out/<lang>/<id>/parsed[-variant]/evidence.json vs out/<lang>/<id>/truth/evidence.json.

python evaluate.py [--variant low] [id ...]
Metrics:
  wer        - word error rate of the speech;
  critical   - were the scenario's critical moments found (a toast, a message arriving, a setting reverting);
               a moment is found if an event with matching text exists within ±0.7 s;
               moments visible only as a cursor click, or not on screen at all, are listed separately;
  recall     - share of visible screen changes from the ground truth that the parser found;
  precision  - share of parser events that have a ground-truth match;
  short      - for brief appearances (< 1 s): how precisely the parser measured the duration;
  clicks     - clicks found: within ±0.6 s and the cursor inside the clicked element; precision of the parser's clicks;
  hovers     - deliberate hovers found (the cursor over the element while the phrase lasts);
  slides     - meetings: share of the time the parser knows the right slide number;
  files      - attached pdf/pptx: share of files where the parser finds exactly the slides that differ from the screen;
  speakers   - meetings: share of utterances attributed to the right tile;
  links      - "right here", "this one", a click while saying "send": share of ground-truth links found;
  checks     - cross-checks from the bug markup (an error nobody mentions, a value that went back, a change behind the
               front window, a claim the video does not show): found / marked, then flags with no mark (+n);
  screen_text- share of the texts of every ground-truth screen state found in the parser state at the same moment,
               weighted by how long the state lasts: this is where facts that never change show up (a garbled name).
"""
import argparse
import json
import re
from pathlib import Path

from rapidfuzz import fuzz
from rapidfuzz.distance import Levenshtein

OUT = Path(__file__).resolve().parents[1] / "out"
WIN = 700
SCREEN_KINDS = {"appear", "disappear", "text_change", "visual_change", "screen_change", "window_change", "type"}
CLICK_WIN = 600


def words(s: str) -> list[str]:
    return re.sub(r"[^\w ]|_", " ", (s or "").lower().replace("ё", "е")).split()


def text_match(truth: str | None, pred: str | None) -> bool:
    # at least half of the truth words must be in the prediction (OCR slack per word); a short "PDF" or a clock no longer
    # matches a whole row. Text cut on screen with an ellipsis is compared up to the cut.
    t = [w for w in words(truth) if len(w) > 1] or words(truth)
    p = words(pred)
    if not t or not p:
        return False
    like = lambda w, q: fuzz.ratio(w, q) >= 80 or (len(w) > 4 and len(q) >= 4 and w.startswith(q))
    hits = [any(like(w, q) for q in p) for w in t]
    if pred and ("..." in pred or "…" in pred):
        # walk the prediction left to right: the cut is where its last word lands in the truth
        i, cut = 0, None
        for q in p:
            j = next((j for j in range(i, len(t)) if like(t[j], q)), None)
            if j is not None:
                i, cut = j + 1, j
        if cut is not None:
            hits = hits[: cut + 1]
    return sum(hits) / len(hits) >= 0.5


def near(te: dict, p: dict) -> bool:
    """Close in time; typing lasts from the first to the last keystroke."""
    if p["kind"] == "type":
        return p["t_ms"] - WIN <= te["t_ms"] <= (p["end_ms"] or p["t_ms"]) + WIN
    return abs(p["t_ms"] - te["t_ms"]) <= WIN


def pred_text(te: dict, p: dict) -> str | None:
    # what a whole-screen change took away is in its "before"
    return p.get("before") if te["kind"] == "disappear" and p["kind"] == "screen_change" else p["text"]


def pair(te: dict, preds: list[dict]) -> dict | None:
    for p in preds:
        if p["kind"] in SCREEN_KINDS and near(te, p) and text_match(te["text"], pred_text(te, p)):
            return p
    return None


def wer(truth: dict, pred: dict) -> float | None:
    t = [w for u in truth["speech"]["utterances"] for w in words(u["text"])]
    p = [w for u in pred["speech"]["utterances"] for w in words(u["text"])]
    if not t or not p:
        return None
    return Levenshtein.distance(t, p) / len(t)


def hit_cursor(te: dict, preds: list[dict]) -> dict | None:
    """A parser click/hover for a ground-truth one: close in time, the cursor inside the element (20 px slack)."""
    if not te.get("bbox"):
        return None
    x, y, w, h = te["bbox"]
    for p in preds:
        if p["kind"] != te["kind"] or "at" not in p:
            continue
        px, py = p["at"]
        if not (x - 20 <= px <= x + w + 20 and y - 20 <= py <= y + h + 20):
            continue
        if te["kind"] == "click" and abs(p["t_ms"] - te["t_ms"]) <= CLICK_WIN:
            return p
        if te["kind"] == "point" and p["t_ms"] < (te["end_ms"] or te["t_ms"] + 1000) and (p["end_ms"] or p["t_ms"]) > te["t_ms"]:
            return p
    return None


def in_screen(truth: dict, box) -> bool:
    """Only the shared screen is parsed; people tiles of a meeting recording are not."""
    if not box:
        return True
    x, y, w, h = next(r["bbox"] for r in truth["regions"] if r["id"] == "screen")
    cx, cy = box[0] + box[2] / 2, box[1] + box[3] / 2
    return x <= cx <= x + w and y <= cy <= y + h


def links_score(truth: dict, pred: dict, k: float) -> float | None:
    """A ground-truth link is found if a parser link overlaps it in time and points at the same thing: the box centre
    inside the element (20 px slack), the same text, or both unresolved."""
    if not truth["links"] or not pred["speech"]["utterances"]:
        return None  # no links, or the speech was not parsed (--no-speech)
    ok = 0
    for tl in truth["links"]:
        for pl in pred.get("links", []):
            if pl["end_ms"] < tl["start_ms"] - 500 or pl["start_ms"] > tl["end_ms"] + 500:
                continue
            tt, pt = tl["target"], pl["target"]
            if tt is None or pt is None:
                if tt is None and pt is None:
                    ok += 1
                    break
                continue
            if tt.get("bbox") and pt.get("bbox"):
                x, y, w, h = tt["bbox"]
                cx, cy = (pt["bbox"][0] + pt["bbox"][2] / 2) * k, (pt["bbox"][1] + pt["bbox"][3] / 2) * k
                if x - 20 <= cx <= x + w + 20 and y - 20 <= cy <= y + h + 20:
                    ok += 1
                    break
            if text_match(pt["text"], tt["text"]) or text_match(tt["text"], pt["text"]):
                ok += 1
                break
    return ok / len(truth["links"])


def speakers_score(truth: dict, pred: dict) -> float | None:
    """Meetings: share of utterances given the right tile (a room tile counts for everyone in the room)."""
    sp = {s["id"]: s for s in truth["speech"]["speakers"]}
    if len(sp) < 2 or not pred["speech"]["utterances"]:
        return None
    ok = n = 0
    for u in truth["speech"]["utterances"]:
        want = sp[u["speaker"]]["tile"] or u["speaker"]
        p = max(pred["speech"]["utterances"], key=lambda x: min(x["end_ms"], u["end_ms"]) - max(x["start_ms"], u["start_ms"]), default=None)
        n += 1
        ok += bool(p and (p.get("tile") or p["speaker"]) == want)
    return ok / n if n else None


def slides_score(sid: str, pred: dict) -> tuple[float | None, float | None]:
    """Share of the time the right slide number is known; share of attached files whose differing slides are found."""
    path = OUT / sid / "truth" / "slides.json"
    if not path.exists():
        return None, None
    truth = json.loads(path.read_text())
    num = den = 0
    for s in truth["shown"]:
        mid, dur = (s["start_ms"] + s["end_ms"]) // 2, s["end_ms"] - s["start_ms"]
        p = next((x for x in pred.get("slides", []) if x["start_ms"] <= mid < x["end_ms"]), None)
        num += dur * bool(p and p["index"] == s["index"])
        den += dur
    files = {a["file"]: {d["index"] for d in a["differs_from_screen"]} for a in pred.get("attachments") or []}
    att = [files.get(a["file"]) == {d["index"] for d in a["differs_from_screen"]} for a in truth["attachments"]]
    return (num / den if den else None), (sum(att) / len(att) if att else None)


def screen_text(truth: dict, pred: dict) -> float | None:
    num = den = 0.0
    for ts in truth["screens"]:
        texts = [t["text"] for t in ts["texts"] if len(words(t["text"])) > 0 and in_screen(truth, t["bbox"])]
        dur = ts["end_ms"] - ts["start_ms"]
        if not texts or dur <= 0:
            continue
        mid = (ts["start_ms"] + ts["end_ms"]) // 2
        ps = next((s for s in pred["screens"] if s["start_ms"] <= mid < s["end_ms"]), None)
        if ps is None:
            ps = min(pred["screens"], key=lambda s: min(abs(s["start_ms"] - mid), abs(s["end_ms"] - mid)), default=None)
        blob = " ".join(t["text"] for t in ps["texts"]) if ps else ""
        num += dur * sum(text_match(t, blob) for t in texts) / len(texts)
        den += dur
    return num / den if den else None


def checks_score(sid: str, pred: dict) -> dict:
    """A mark is found by a flag of its kind at the same moment (a claim: during its line)."""
    rep = OUT / sid / "truth" / "report.json"
    marks = json.loads(rep.read_text()).get("checks", []) if rep.exists() else []
    flags = pred.get("checks", [])
    if not pred["speech"]["utterances"]:  # parsed without speech: only the checks that need none
        marks = [m for m in marks if m["kind"] in ("revert", "covered")]

    def hit(m: dict, f: dict) -> bool:
        if m["kind"] != f["kind"]:
            return False
        if m["kind"] == "claim":
            return f["t_ms"] <= m["end_ms"] + 500 and f.get("end_ms", f["t_ms"]) >= m["t_ms"] - 500
        return abs(f["t_ms"] - m["t_ms"]) <= 1000

    return {
        "checks_found": sum(any(hit(m, f) for f in flags) for m in marks),
        "checks_total": len(marks),
        "checks_missed": [f'{m["kind"]}:{m["name"]}' for m in marks if not any(hit(m, f) for f in flags)],
        "checks_extra": [f'{f["kind"]}@{f["t_ms"]}: {f["text"][:80]}' for f in flags if not any(hit(m, f) for m in marks)],
    }


def evaluate(sid: str, variant: str | None) -> dict:
    truth = json.loads((OUT / sid / "truth" / "evidence.json").read_text())
    pred = json.loads((OUT / sid / (f"parsed-{variant}" if variant else "parsed") / "evidence.json").read_text())
    tev = {e["id"]: e for e in truth["events"]}
    pev = pred["events"]
    # a quality variant is smaller than the master the ground truth is measured on
    k = truth["video"]["width"] / pred["video"]["width"]
    if k != 1:
        pev = [{**e, "bbox": e["bbox"] and [round(v * k) for v in e["bbox"]], **({"at": [round(v * k) for v in e["at"]]} if "at" in e else {})} for e in pev]

    crit, not_on_screen = [], []
    for c in truth.get("critical", []):
        evs = [tev[i] for i in c["events"] if i in tev]
        screen = [e for e in evs if e["kind"] in SCREEN_KINDS and e["visible"]]
        cursor = [e for e in evs if e["kind"] in ("click", "point")]
        if screen:
            hit = next((pair(e, pev) for e in screen if pair(e, pev)), None)
            crit.append({"name": c["name"], "t_ms": c["t_ms"], "by": "screen", "found": bool(hit), "text": screen[0]["text"], "pred": hit and hit["text"]})
        elif cursor:
            hit = next((hit_cursor(e, pev) for e in cursor if hit_cursor(e, pev)), None)
            crit.append({"name": c["name"], "t_ms": c["t_ms"], "by": "cursor", "found": bool(hit), "text": cursor[0]["text"], "pred": hit and hit["text"]})
        else:
            not_on_screen.append(c["name"])

    visible = [e for e in truth["events"] if e["kind"] in SCREEN_KINDS and e["visible"] and e["text"] and in_screen(truth, e["bbox"])]
    found = [e for e in visible if pair(e, pev)]
    screen_pred = [p for p in pev if p["kind"] in SCREEN_KINDS]
    matched = [p for p in screen_pred if any(near(e, p) and text_match(e["text"], pred_text(e, p)) for e in truth["events"])]

    short = []
    for e in visible:
        if e["kind"] == "appear" and e["end_ms"] and e["end_ms"] - e["t_ms"] < 1000:
            p = pair(e, pev)
            short.append({"text": e["text"], "truth_ms": e["end_ms"] - e["t_ms"], "pred_ms": (p["end_ms"] - p["t_ms"]) if p and p.get("end_ms") else None})

    t_clicks = [e for e in truth["events"] if e["kind"] == "click" and e.get("bbox")]
    p_clicks = [p for p in pev if p["kind"] == "click"]
    t_points = [e for e in truth["events"] if e["kind"] == "point" and e.get("bbox")]
    click_ok = [p for p in p_clicks if any(hit_cursor(e, [p]) for e in t_clicks)]
    return {
        "id": sid,
        "wer": wer(truth, pred),
        "critical": crit,
        "critical_found": sum(c["found"] for c in crit),
        "critical_total": len(crit),
        "not_on_screen": not_on_screen,
        "recall": len(found) / len(visible) if visible else None,
        "precision": len(matched) / len(screen_pred) if screen_pred else None,
        "short": short,
        "clicks": len([e for e in t_clicks if hit_cursor(e, pev)]) / len(t_clicks) if t_clicks else None,
        "click_precision": len(click_ok) / len(p_clicks) if p_clicks else None,
        "hovers": len([e for e in t_points if hit_cursor(e, pev)]) / len(t_points) if t_points else None,
        "screen_text": screen_text(truth, pred),
        "links": links_score(truth, pred, k),
        "speakers": speakers_score(truth, pred),
        "slides": slides_score(sid, pred)[0],
        "files": slides_score(sid, pred)[1],
        **checks_score(sid, pred),
        "missed": [{"t_ms": e["t_ms"], "kind": e["kind"], "text": e["text"][:70]} for e in visible if e not in found],
        "missed_clicks": [{"t_ms": e["t_ms"], "text": e["text"]} for e in t_clicks if not hit_cursor(e, pev)],
    }


def chk(r: dict) -> str:
    if not r["checks_total"] and not r["checks_extra"]:
        return "-"
    return f'{r["checks_found"]}/{r["checks_total"]}' + (f'+{len(r["checks_extra"])}' if r["checks_extra"] else "")


def pct(x):
    return "  -  " if x is None else f"{x * 100:4.0f}%"


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("ids", nargs="*")
    ap.add_argument("--variant")
    a = ap.parse_args()
    suffix = f"parsed-{a.variant}" if a.variant else "parsed"
    ids = a.ids or sorted(f"{p.parts[-4]}/{p.parts[-3]}" for p in OUT.glob(f"*/*/{suffix}/evidence.json"))
    rows = [evaluate(s, a.variant) for s in ids]
    print(f"{'scenario':33} {'WER':>5} {'crit.':>7} {'recall':>6} {'prec':>6} {'clicks':>6} {'c.prec':>6} {'hover':>6} {'text':>6} {'links':>6} {'spkr':>6} {'slides':>6} {'files':>6} {'checks':>7}  not on screen")
    for r in rows:
        print(f"{r['id']:33} {pct(r['wer'])} {r['critical_found']:>3}/{r['critical_total']:<3} {pct(r['recall'])} {pct(r['precision'])} {pct(r['clicks'])} {pct(r['click_precision'])} {pct(r['hovers'])} {pct(r['screen_text'])} {pct(r['links'])} {pct(r['speakers'])} {pct(r['slides'])} {pct(r['files'])} {chk(r):>7}  {', '.join(r['not_on_screen'])}")
    tot_f, tot_t = sum(r["critical_found"] for r in rows), sum(r["critical_total"] for r in rows)
    print(f"{'critical total':33} {'':5} {tot_f:>3}/{tot_t:<3}")
    print(f"{'checks total':33} {sum(r['checks_found'] for r in rows)}/{sum(r['checks_total'] for r in rows)}, flags with no mark: {sum(len(r['checks_extra']) for r in rows)}")
    # merge into the stored results so evaluating a few scenarios does not drop the others
    path = OUT / f"_eval{'-' + a.variant if a.variant else ''}.json"
    stored = {r["id"]: r for r in json.loads(path.read_text())} if path.exists() else {}
    stored.update({r["id"]: r for r in rows})
    path.write_text(json.dumps(sorted(stored.values(), key=lambda r: r["id"]), ensure_ascii=False, indent=1))
