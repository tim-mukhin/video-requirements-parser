"""Judge: an agent report against the ground truth, scored by a strong model through Copilot CLI (headless, no tools).

python judge.py --report <model>@<effort> [--judge claude-opus-5.5] [--variant low] [--visible] [<lang>/<id> ...]
out/<lang>/<id>/parsed[-variant]/agent/<model>@<effort>.judge-[visible-]<judge>.json

Bug videos, 0-2 each: steps (the minimal repro, in order, no fumbles), actual (what really happened, with the decisive
evidence), verdict (bug or user mistake, the real cause, the traps avoided); plus invented - statements that the ground
truth contradicts or that nothing supports. Meetings, 0-2 each: coverage, status, attribution; plus invented.
"""
import argparse
import json
import re
import shutil
import subprocess
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "out"

RUBRIC = """You grade a report written from a work video against the ground truth of that video. The ground truth was
written by the author of the test video and is correct. Grade only what the report says, not its style.
The ground truth knows more than the video shows: full texts that are cut off with an ellipsis on screen, windows or
tabs that are never shown, the internal reason behind an error. A report built from the video cannot know these; do
not take points for missing them and do not call the report's "not shown" an invention.

{part}

Answer with a single JSON object and nothing else:
{schema}

GROUND TRUTH
{truth}

REPORT
{report}"""

BUG = """Scores, each 0, 1 or 2:
- steps: 2 - the minimal repro steps in the right order, nothing essential missing, fumbles and wrong picks left out;
  1 - mostly right but a step essential to reproduce is vague or missing, or noise steps are included as repro steps;
  0 - the steps would not reproduce the problem.
- actual: 2 - what really happened, including the decisive evidence named in the ground truth (an error text, a value,
  a duration); 1 - the outcome is right but the decisive evidence is missing or wrong; 0 - wrong outcome.
- verdict: 2 - the right conclusion: bug or user mistake, the real cause as far as the video shows it, the traps listed
  in the ground truth avoided (a claim taken as fact, a distractor taken as the cause); 1 - partly; 0 - wrong.
  If the ground truth's class differs from the report's class only by wording of a close category, do not take a point
  for it; take points when the report misjudges what happened.
- invented: statements in the report that the ground truth contradicts or that are presented as facts with nothing to
  back them, each as a short quote; minor wording differences are not invented."""

MEETING = """Scores, each 0, 1 or 2:
- coverage: 2 - every requirement of the ground truth appears in the report; 1 - most do; 0 - fewer than half.
- status: 2 - stated / proposed / decided / rejected / open question right for all found requirements; 1 - one or
  two wrong; 0 - more.
- attribution: 2 - who proposed and who decided right where the ground truth names them; 1 - partly; 0 - mostly wrong.
- invented: requirements or decisions in the report that the meeting did not have, each as a short quote."""

BUG_TICKET = """The report was written from the reporter's ticket plus the video, as a developer picking up the bug would.
Scores, each 0, 1 or 2:
- steps: 2 - the minimal repro steps in the right order, concrete where the video shows them (what was clicked or
  typed, when); 1 - right but vague or with noise steps; 0 - would not reproduce the problem.
- actual: 2 - what really happens, with the decisive evidence the video shows (the moment, a value, a text);
  1 - the outcome is right but the evidence is missing or only taken from the ticket; 0 - wrong outcome.
- verdict: 2 - the right conclusion (bug or user mistake, the cause as far as ticket and video show it); 1 - partly;
  0 - wrong. A control recording (no bug by design) is judged right when the report says it shows the correct behaviour.
- video: what the video added beyond the ticket: 2 - the report confirms or corrects the ticket with concrete video
  evidence (an exact moment, a value on screen, a step or setting the ticket does not mention, a disagreement between
  ticket and video, all true to the ground truth); 1 - some of that; 0 - it only restates the ticket.
- invented: statements the ground truth contradicts or that nothing backs, each as a short quote; a claim of the
  ticket presented as seen in the video when the video does not show it counts."""

SCHEMA_TICKET = '{"steps": 0, "actual": 0, "verdict": 0, "video": 0, "invented": ["..."], "notes": "one or two sentences"}'

SCHEMA_BUG = '{"steps": 0, "actual": 0, "verdict": 0, "invented": ["..."], "notes": "one or two sentences"}'
SCHEMA_MEETING = '{"coverage": 0, "status": 0, "attribution": 0, "invented": ["..."], "notes": "one or two sentences"}'


def visible_text(key: str, variant: str | None) -> str | None:
    """A real recording labelled from its frames: what the video itself shows, so facts only the issue author knew
    are not asked for, and a control recording (no bug by design) is graded as one."""
    f = OUT / key / (f"visible-{variant}.json" if variant else "visible.json")
    if not f.exists():
        return None
    v = json.loads(f.read_text())
    keep = {k: v.get(k) for k in ("control", "shows_bug", "steps", "actual", "decisive", "not_visible")}
    keep["issue"] = json.loads((OUT / key / "source.json").read_text()).get("description")
    keep["note"] = ("labelled from the frames of this recording: grade against what the video shows. Facts in not_visible "
                    "are not required and not a fault when missing. control: true means this recording shows the correct "
                    "behaviour by design - a right report says so and does not invent a bug; shows_bug: no means the "
                    "problem is not in this recording - a right report does not claim it.")
    return json.dumps(keep, ensure_ascii=False, indent=1)


def ticket_truth(key: str, variant: str | None) -> str | None:
    """Ticket + video setting: the issue's expected report, what the frames of this recording show, and the ticket the
    agent had, so the judge sees what the video added."""
    vis = visible_text(key, variant)
    t = OUT / key / "ticket.md"
    if vis is None or not t.exists():
        return None
    src = json.loads((OUT / key / "source.json").read_text())
    return json.dumps({"expected_report": src.get("expected_report"), "this_recording": json.loads(vis),
                       "ticket_given_to_the_agent": t.read_text(encoding="utf-8")[:6000]}, ensure_ascii=False, indent=1)


def truth_text(key: str, variant: str | None = None, visible: bool = False) -> tuple[str, bool]:
    if visible:
        return visible_text(key, variant), True
    src = OUT / key / "source.json"
    if src.exists() and not (OUT / key / "truth").exists():  # a real recording: the issue text is the ground truth
        j = json.loads(src.read_text())
        keep = {k: j.get(k) for k in ("url", "description", "expected_report", "bug_in")}
        keep["note"] = ("written from the issue text, not from the frames; the issue may have several recordings and the "
                        "report covers one of them, so facts shown only in another recording are not missing from it")
        return json.dumps(keep, ensure_ascii=False, indent=1), True
    t = OUT / key / "truth"
    if (t / "report.json").exists():
        r = json.loads((t / "report.json").read_text())
        keep = {k: r[k] for k in ("title", "class", "steps", "expected", "actual", "traps")}
        keep["critical_moments"] = [{k: c.get(k) for k in ("name", "t_ms", "text", "duration_ms") if c.get(k) is not None} for c in r["critical"]]
        keep["steps"] = [{k: s.get(k) for k in ("t_ms", "action", "target_text", "window_title", "text") if s.get(k) is not None} for s in r["steps"]]
        keep["note"] = "steps here are every user action in the video, including fumbles; the repro is the subset that matters"
        return json.dumps(keep, ensure_ascii=False, indent=1), True
    reqs = json.loads((t / "requirements.json").read_text())
    speakers = json.loads((t / "speakers.json").read_text()) if (t / "speakers.json").exists() else None
    return json.dumps({"requirements": reqs, "speakers": speakers}, ensure_ascii=False, indent=1), False


def judge(key: str, variant: str | None, report: str, model: str, visible: bool = False, ticket: bool = False) -> dict:
    work = OUT / key / (f"parsed-{variant}" if variant else "parsed")
    if ticket:
        truth, is_bug, part, schema = ticket_truth(key, variant), True, BUG_TICKET, SCHEMA_TICKET
    else:
        truth, is_bug = truth_text(key, variant, visible)
        part, schema = (BUG, SCHEMA_BUG) if is_bug else (MEETING, SCHEMA_MEETING)
    prompt = RUBRIC.format(part=part, schema=schema, truth=truth,
                           report=(work / "agent" / f"{report}.md").read_text())
    cmd = [shutil.which("copilot") or "copilot", "-p", prompt, "--model", model, "--available-tools", "", "--no-ask-user",
           "--no-custom-instructions", "--no-auto-update", "-s"]
    for _ in range(2):
        p = subprocess.run(cmd, cwd=work, capture_output=True, text=True, encoding="utf-8", timeout=900)
        m = re.findall(r"\{.*\}", p.stdout, re.S)
        try:
            return {"judge": model, "kind": "bug" if is_bug else "meeting", **json.loads(m[-1])}
        except (IndexError, json.JSONDecodeError):
            continue
    raise RuntimeError(f"{key}: no JSON from the judge: {p.stdout[-300:]!r} {p.stderr[-300:]!r}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("ids", nargs="*")
    ap.add_argument("--report", required=True, help="<model>@<effort> of the agent report")
    ap.add_argument("--judge", default="claude-opus-5.5")
    ap.add_argument("--variant")
    ap.add_argument("--ticket", action="store_true", help="real recordings, report made from ticket + video: grade it so, with a 'video' score")
    ap.add_argument("--visible", action="store_true", help="real recordings: grade against visible[-variant].json (what the frames show)")
    a = ap.parse_args()
    suffix = f"parsed-{a.variant}" if a.variant else "parsed"
    ids = a.ids or sorted(f"{p.parts[-5]}/{p.parts[-4]}" for p in OUT.glob(f"*/*/{suffix}/agent/{a.report}.json"))
    for key in ids:
        mode = "ticket-" if a.ticket else "visible-" if a.visible else ""
        out = OUT / key / suffix / "agent" / f"{a.report}.judge-{mode}{a.judge}.json"
        need_vis = a.visible or a.ticket
        if out.exists() or (need_vis and not (OUT / key / (f"visible-{a.variant}.json" if a.variant else "visible.json")).exists()):
            continue
        try:
            j = judge(key, a.variant, a.report, a.judge, a.visible, a.ticket)
        except (RuntimeError, subprocess.TimeoutExpired) as ex:
            print(f"{key}: failed: {ex}", flush=True)
            continue
        out.write_text(json.dumps(j, ensure_ascii=False, indent=1), encoding="utf-8")
        sc = {k: j[k] for k in ("steps", "actual", "verdict", "video", "coverage", "status", "attribution") if k in j}
        print(f"{key} {a.report}: {sc}, invented {len(j.get('invented') or [])}", flush=True)
