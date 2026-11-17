"""Agent reports against ground truth: out/<lang>/<id>/parsed[-variant]/agent.json vs truth/report.json, requirements.json.

python agent_eval.py [--variant low] [--detail <model>@<effort>] [<lang>/<id> ...]
One row per model and effort (every out/<lang>/<id>/parsed/agent/<model>@<effort>.json); --detail shows its videos.
Metrics, all from ids and times, no model:
  class      - bug class matches; not-a-bug is reported separately (a user mistake must not become a bug and back);
  critical   - critical moments of the scenario covered by the events the agent cites in steps and key events;
  claims     - claims marked in bug.checks that the agent lists as claims (not confirmed by the screen);
  missed     - errors nobody mentions (bug.checks unmentioned) that the agent lists among what the author missed;
  reqs       - meeting requirements found (the agent cites an utterance of the requirement's evidence);
  status     - of the found ones, share with the right status.
"""
import argparse
import json
import re
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "out"
NEAR_MS = 1000


def times(evidence: dict) -> dict[str, tuple[int, int]]:
    """Event and utterance id -> (start, end) in ms."""
    t = {e["id"]: (e["t_ms"], e.get("end_ms") or e["t_ms"]) for e in evidence["events"]}
    t.update({u["id"]: (u["start_ms"], u["end_ms"]) for u in evidence["speech"]["utterances"]})
    return t


def ids_in(*texts) -> set[str]:
    return {m for s in texts for m in re.findall(r"\b[pu]\d{3}\b", s or "")}


def hit(span: tuple[int, int], t: int, end: int | None = None) -> bool:
    return span[0] - NEAR_MS <= (end if end is not None else t) and span[1] + NEAR_MS >= t


def score(key: str, variant: str | None, name: str) -> dict:
    work = OUT / key / (f"parsed-{variant}" if variant else "parsed")
    agent = json.loads((work / "agent" / f"{name}.json").read_text())
    span = times(json.loads((work / "evidence.json").read_text()))
    row = {"id": key, "kind": agent["kind"], "seconds": agent.get("seconds"), "nano_aiu": agent.get("nano_aiu"), "requests": agent.get("premium_requests"),
           "looked": len(agent.get("looked") or []), "judges": {}}
    for jf in (work / "agent").glob(f"{name}.judge-*.json"):
        j = json.loads(jf.read_text())
        keys = ("steps", "actual", "verdict") if j["kind"] == "bug" else ("coverage", "status", "attribution")
        row["judges"][j["judge"]] = {"score": sum(j.get(k, 0) for k in keys) / (2 * len(keys)), "invented": len(j.get("invented") or [])}
    rep_path, req_path = OUT / key / "truth" / "report.json", OUT / key / "truth" / "requirements.json"
    if rep_path.exists():
        rep, bug = json.loads(rep_path.read_text()), agent.get("bug") or {}
        cited = {i for s in bug.get("steps", []) for i in s.get("events", [])} | set(bug.get("key_events", []))
        cited = [span[i] for i in cited if i in span]
        crit = [c for c in rep["critical"] if "t_ms" in c]
        found = [c for c in crit if any(hit(s, c["t_ms"], c.get("end_ms")) for s in cited)]
        claims = [span[c["utterance"]] for c in bug.get("claims", []) if c.get("verdict") != "confirmed" and c.get("utterance") in span]
        missed = [span[i] for m in bug.get("missed_by_author", []) for i in ids_in(m) if i in span]
        marks = rep.get("checks", [])
        row.update({
            "class": bug.get("class"), "class_truth": rep["class"], "class_ok": bug.get("class") == rep["class"],
            "not_a_bug_ok": (bug.get("class") == "not-a-bug") == (rep["class"] == "not-a-bug"),
            "critical_found": len(found), "critical_total": len(crit), "critical_missed": [c["name"] for c in crit if c not in found],
            "claims_found": sum(any(hit(s, m["t_ms"], m["end_ms"]) for s in claims) for m in marks if m["kind"] == "claim"),
            "claims_total": sum(m["kind"] == "claim" for m in marks),
            "missed_found": sum(any(hit(s, m["t_ms"]) for s in missed) for m in marks if m["kind"] == "unmentioned"),
            "missed_total": sum(m["kind"] == "unmentioned" for m in marks),
        })
    if req_path.exists():
        reqs, preds = json.loads(req_path.read_text()), agent.get("requirements") or []
        pspans = [(p, [span[i] for i in p.get("evidence", []) if i in span]) for p in preds]
        found, status_ok = 0, 0
        for r in reqs:
            utts = [e for e in r["evidence"] if "utterance" in e]
            match = [p for p, ss in pspans if any(hit(s, e["t_ms"], e["end_ms"]) for s in ss for e in utts)]
            if match:
                found += 1
                status_ok += any(p["status"] == r["status"] for p in match)
        row.update({"reqs_found": found, "reqs_total": len(reqs), "reqs_status_ok": status_ok, "reqs_predicted": len(preds)})
    return row


def frac(a, b) -> str:
    return "-" if not b else f"{a}/{b}"


def total(rows: list[dict]) -> dict:
    bugs = [r for r in rows if "class" in r]
    S = lambda k: sum(r.get(k) or 0 for r in rows)
    return {
        "videos": len(rows), "class": f"{sum(r['class_ok'] for r in bugs)}/{len(bugs)}", "not_a_bug": f"{sum(r['not_a_bug_ok'] for r in bugs)}/{len(bugs)}",
        "critical": f"{S('critical_found')}/{S('critical_total')}", "claims": f"{S('claims_found')}/{S('claims_total')}",
        "missed": f"{S('missed_found')}/{S('missed_total')}", "reqs": f"{S('reqs_found')}/{S('reqs_total')}", "status": f"{S('reqs_status_ok')}/{S('reqs_found')}",
        "seconds": round(S("seconds") / max(1, len(rows))), "requests": round(S("requests") / max(1, len(rows)), 1), "looked": round(S("looked") / max(1, len(rows)), 1),
        "judges": {j: {"score": round(sum(r["judges"][j]["score"] for r in rows if j in r["judges"]) / n, 2),
                       "invented": round(sum(r["judges"][j]["invented"] for r in rows if j in r["judges"]) / n, 2), "videos": n}
                   for j in sorted({j for r in rows for j in r["judges"]}) for n in [sum(j in r["judges"] for r in rows)]},
    }


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("ids", nargs="*")
    ap.add_argument("--variant")
    ap.add_argument("--detail")
    a = ap.parse_args()
    suffix = f"parsed-{a.variant}" if a.variant else "parsed"
    found = sorted(OUT.glob(f"*/*/{suffix}/agent/*.json"))
    found = [f for f in found if ".judge-" not in f.stem]
    names = sorted({f.stem for f in found})
    all_ids = sorted({f"{f.parts[-5]}/{f.parts[-4]}" for f in found})
    ids = a.ids or [k for k in all_ids if (OUT / k / "truth").exists()]
    results = {n: [score(k, a.variant, n) for k in ids if (OUT / k / suffix / "agent" / f"{n}.json").exists()] for n in names}
    print(f"{'model@effort':32} {'videos':>6} {'class':>6} {'notbug':>6} {'crit.':>6} {'claims':>6} {'missed':>6} {'reqs':>6} {'status':>6} {'s/video':>7} {'req':>5} {'frames':>6}  judges: score, invented per video")
    for n, rows in results.items():
        t = total(rows)
        print(f"{n:32} {t['videos']:>6} {t['class']:>6} {t['not_a_bug']:>6} {t['critical']:>6} {t['claims']:>6} {t['missed']:>6} {t['reqs']:>6} {t['status']:>6} {t['seconds']:>7} {t['requests']:>5} {t['looked']:>6}  "
              + "  ".join(f"{j} {v['score'] * 100:.0f}% {v['invented']:.1f}" + ("" if v["videos"] == t["videos"] else f" ({v['videos']})") for j, v in t["judges"].items()))
    if a.detail:
        print(f"\n{a.detail}")
        print(f"{'scenario':33} {'class':>27} {'crit.':>6} {'claims':>6} {'missed':>6} {'reqs':>6} {'status':>6}")
        for r in results.get(a.detail, []):
            cls = "" if "class" not in r else f"{r['class']}{'' if r['class_ok'] else ' ≠ ' + r['class_truth']}"
            print(f"{r['id']:33} {cls:>27} {frac(r.get('critical_found'), r.get('critical_total')):>6} {frac(r.get('claims_found'), r.get('claims_total')):>6} "
                  f"{frac(r.get('missed_found'), r.get('missed_total')):>6} {frac(r.get('reqs_found'), r.get('reqs_total')):>6} {frac(r.get('reqs_status_ok'), r.get('reqs_found')):>6}"
                  + (f"  missed: {', '.join(r['critical_missed'])}" if r.get("critical_missed") else ""))
    (OUT / f"_agent_eval{'-' + a.variant if a.variant else ''}.json").write_text(json.dumps({n: {"total": total(rows), "videos": rows} for n, rows in results.items()}, ensure_ascii=False, indent=1))
