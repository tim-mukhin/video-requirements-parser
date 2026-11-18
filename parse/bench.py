"""Bench: agent configurations side by side on the real bug recordings, as the judges scored them.

python bench.py <report> [<report> ...] [--truth issue|visible|ticket|both] [--per-item]
  <report> - <model>@<effort>[+input][+tools], e.g. claude-sonnet-5.5@default+investigate
Scores are the judges' steps + actual + verdict (0-2 each) as a share of the maximum, averaged over the judges.
The set: out/real/<id>/ recordings that have visible[-stem].json labels (issue edits and long talks are left out).
"""
import argparse
import json
from pathlib import Path

REAL = Path(__file__).resolve().parents[1] / "out" / "real"


def recordings() -> list[dict]:
    out = []
    for vf in sorted(REAL.glob("*/visible*.json")):
        v = json.loads(vf.read_text())
        stem = Path(v["recording"]).stem
        work = vf.parent / ("parsed" if stem in ("recording", "video") else f"parsed-{stem}")
        if not (work / "evidence.json").exists():
            continue
        ev = json.loads((work / "evidence.json").read_text())
        out.append({"id": f"{vf.parent.name}/{v['recording']}", "work": work, "label": v,
                    "seconds": ev["video"]["duration_ms"] / 1000, "cursor": (ev.get("input") or {}).get("cursor_share", 0) > 0})
    return out


def score(work: Path, report: str, truth: str) -> float | None:
    """issue - judged against the issue text; visible - against what the frames show; ticket - a report made from the
    ticket plus the video, with a fourth score for what the video added (max 8 instead of 6)."""
    pat = f"{report}.judge-{truth}-*.json" if truth in ("visible", "ticket") else f"{report}.judge-*.json"
    js = [json.loads(p.read_text()) for p in (work / "agent").glob(pat)
          if truth != "issue" or not any(f".judge-{m}-" in p.name for m in ("visible", "ticket"))]
    if len(js) < 2:
        return None
    keys = ("steps", "actual", "verdict", "video") if truth == "ticket" else ("steps", "actual", "verdict")
    return 100 * sum(j.get(k, 0) for j in js for k in keys) / (2 * len(keys) * len(js))


GROUPS = {
    "all": lambda r: True,
    "cursor": lambda r: r["cursor"],
    "no cursor": lambda r: not r["cursor"],
    "bug shown": lambda r: r["label"]["shows_bug"] == "yes" and not r["label"]["control"],
    "partly/no/control": lambda r: r["label"]["shows_bug"] != "yes" or r["label"]["control"],
    "<=20 s": lambda r: r["seconds"] <= 20,
    "20-60 s": lambda r: 20 < r["seconds"] <= 60,
    ">60 s": lambda r: r["seconds"] > 60,
}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("reports", nargs="+")
    ap.add_argument("--truth", default="both", choices=["issue", "visible", "ticket", "both"])
    ap.add_argument("--per-item", action="store_true")
    a = ap.parse_args()
    truths = ["issue", "visible"] if a.truth == "both" else [a.truth]
    recs = recordings()
    cols = [(rep, t) for rep in a.reports for t in truths]
    S = {(r["id"], rep, t): score(r["work"], rep, t) for r in recs for rep, t in cols}
    full = [r for r in recs if all(S[(r["id"], rep, t)] is not None for rep, t in cols)]
    print(f"{len(full)} of {len(recs)} recordings scored by every configuration\n")
    head = f"{'group':20} {'n':>3}  " + "  ".join(f"{rep.split('@')[-1][:22] + '/' + t[:3]:>26}" for rep, t in cols)
    if len(a.reports) > 1:
        head += f"  {'best of all/' + truths[-1][:3]:>16}"
    print(head)
    for g, f in GROUPS.items():
        rs = [r for r in full if f(r)]
        if not rs:
            continue
        line = f"{g:20} {len(rs):>3}  " + "  ".join(f"{sum(S[(r['id'], rep, t)] for r in rs) / len(rs):>25.0f}%" for rep, t in cols)
        if len(a.reports) > 1:
            best = sum(max(S[(r["id"], rep, truths[-1])] for rep in a.reports) for r in rs) / len(rs)
            line += f"  {best:>15.0f}%"
        print(line)
    if a.per_item:
        print()
        for r in full:
            print(f"{r['id']:52} " + "  ".join(f"{S[(r['id'], rep, t)]:>4.0f}" for rep, t in cols))


if __name__ == "__main__":
    main()
