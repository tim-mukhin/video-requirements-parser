"""Parser evaluation against ground truth: out/<lang>/<id>/parsed[-variant]/evidence.json vs out/<lang>/<id>/truth/evidence.json.

python evaluate.py [--variant low] [id ...]
Metrics:
  wer        - word error rate of the speech;
  critical   - were the scenario's critical moments found (a toast, a message arriving, a setting reverting);
               a moment is found if an event with matching text exists within ±0.7 s;
               moments visible only as a cursor click, or not on screen at all, are listed separately;
  recall     - share of visible screen changes from the ground truth that the parser found;
  precision  - share of parser events that have a ground-truth match;
  short      - for brief appearances (< 1 s): how precisely the parser measured the duration.
"""
import argparse
import json
import re
from pathlib import Path

from rapidfuzz import fuzz
from rapidfuzz.distance import Levenshtein

OUT = Path(__file__).resolve().parents[1] / "out"
WIN = 700
SCREEN_KINDS = {"appear", "disappear", "text_change", "screen_change", "window_change"}


def words(s: str) -> list[str]:
    return re.sub(r"[^\w ]", " ", (s or "").lower().replace("ё", "е")).split()


def text_match(a: str | None, b: str | None) -> bool:
    if not a or not b:
        return False
    a, b = " ".join(words(a)), " ".join(words(b))
    if len(a) < 3 or len(b) < 3:
        return a == b
    return fuzz.partial_ratio(a, b) >= 75


def pair(te: dict, preds: list[dict]) -> dict | None:
    for p in preds:
        if p["kind"] in SCREEN_KINDS and abs(p["t_ms"] - te["t_ms"]) <= WIN and text_match(te["text"], p["text"]):
            return p
    return None


def wer(truth: dict, pred: dict) -> float | None:
    t = [w for u in truth["speech"]["utterances"] for w in words(u["text"])]
    p = [w for u in pred["speech"]["utterances"] for w in words(u["text"])]
    if not t or not p:
        return None
    return Levenshtein.distance(t, p) / len(t)


def evaluate(sid: str, variant: str | None) -> dict:
    truth = json.loads((OUT / sid / "truth" / "evidence.json").read_text())
    pred = json.loads((OUT / sid / (f"parsed-{variant}" if variant else "parsed") / "evidence.json").read_text())
    tev = {e["id"]: e for e in truth["events"]}
    pev = pred["events"]

    crit, cursor_only = [], []
    for c in truth.get("critical", []):
        evs = [tev[i] for i in c["events"] if i in tev]
        screen = [e for e in evs if e["kind"] in SCREEN_KINDS and e["visible"]]
        if not screen:
            cursor_only.append(c["name"])
            continue
        hit = next((pair(e, pev) for e in screen if pair(e, pev)), None)
        crit.append({"name": c["name"], "t_ms": c["t_ms"], "found": bool(hit), "text": screen[0]["text"], "pred": hit and hit["text"]})

    visible = [e for e in truth["events"] if e["kind"] in SCREEN_KINDS and e["visible"] and e["text"]]
    found = [e for e in visible if pair(e, pev)]
    screen_pred = [p for p in pev if p["kind"] in SCREEN_KINDS]
    matched = [p for p in screen_pred if any(abs(p["t_ms"] - e["t_ms"]) <= WIN and text_match(e["text"], p["text"]) for e in truth["events"])]

    short = []
    for e in visible:
        if e["kind"] == "appear" and e["end_ms"] and e["end_ms"] - e["t_ms"] < 1000:
            p = pair(e, pev)
            short.append({"text": e["text"], "truth_ms": e["end_ms"] - e["t_ms"], "pred_ms": (p["end_ms"] - p["t_ms"]) if p and p.get("end_ms") else None})

    return {
        "id": sid,
        "wer": wer(truth, pred),
        "critical": crit,
        "critical_found": sum(c["found"] for c in crit),
        "critical_total": len(crit),
        "cursor_only": cursor_only,
        "recall": len(found) / len(visible) if visible else None,
        "precision": len(matched) / len(screen_pred) if screen_pred else None,
        "short": short,
        "missed": [{"t_ms": e["t_ms"], "kind": e["kind"], "text": e["text"][:70]} for e in visible if e not in found],
    }


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
    print(f"{'scenario':37} {'WER':>5} {'crit.':>7} {'recall':>6} {'prec':>6}  cursor only / not on screen")
    for r in rows:
        print(f"{r['id']:37} {pct(r['wer'])} {r['critical_found']:>3}/{r['critical_total']:<3} {pct(r['recall'])} {pct(r['precision'])}  {', '.join(r['cursor_only'])}")
    tot_f, tot_t = sum(r["critical_found"] for r in rows), sum(r["critical_total"] for r in rows)
    print(f"{'critical total':37} {'':5} {tot_f:>3}/{tot_t:<3}")
    # merge into the stored results so evaluating a few scenarios does not drop the others
    path = OUT / f"_eval{'-' + a.variant if a.variant else ''}.json"
    stored = {r["id"]: r for r in json.loads(path.read_text())} if path.exists() else {}
    stored.update({r["id"]: r for r in rows})
    path.write_text(json.dumps(sorted(stored.values(), key=lambda r: r["id"]), ensure_ascii=False, indent=1))
