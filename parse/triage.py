"""Triage: why an agent configuration loses points, grouped into causes, each with a proposed fix.

python triage.py <report> [--truth ticket|visible|issue] [--model gpt-6-sol] [--below 0.75]
-> out/triage/<report>.<truth>.md

Collects the judges' notes and invented statements for every recording scored below the threshold, and asks a strong
model (Copilot CLI, headless, no tools) to group them into causes. For each cause it names the recordings, and the fix,
deterministic first: a parser pass or a vrp command when the fact is measurable, a prompt rule only when it is
judgement. One step of the improvement loop: triage -> one change -> bench -> keep it or roll back.
"""
import argparse
import json
import re
import shutil
import subprocess
from pathlib import Path

from bench import recordings

OUT = Path(__file__).resolve().parents[1] / "out"

ASK = """You review where a video-to-bug-report pipeline loses points. The pipeline: a deterministic parser (cursor,
clicks, hovers, what appeared, moved, flickered or flashed, OCR, speech) writes a timeline; a watcher model reads the
frames; an investigator model checks the watcher against the timeline and can call `vrp events/look/diff/ocr/find` to
ask the video about a moment; with a ticket when there is one. Two judges compared each report with a ground truth.

Below: for every recording that scored under {below:.0%}, the judges' notes and the statements they called invented,
plus what the frames of the recording show (the label).

Group the losses into causes (5-10). For each cause:
- what goes wrong, in one or two sentences, and the recordings it hits (ids);
- whether the fact was in reach: in the frames at all, in the parser's output, or only in the ticket or nowhere;
- the fix, deterministic first: a parser pass or a vrp command when the fact can be measured (a move, a duration, a
  text, a count); a prompt rule only for judgement; "out of reach" when the video cannot show it;
- how to check the fix: which recordings should change.
Then the single change you would make first, and why. Write markdown, plainly, no preamble.

{items}"""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("report")
    ap.add_argument("--truth", default="ticket", choices=["ticket", "visible", "issue"])
    ap.add_argument("--model", default="gpt-6-sol")
    ap.add_argument("--below", type=float, default=0.75)
    a = ap.parse_args()
    items = []
    for r in recordings():
        pat = f"{a.report}.judge-{a.truth}-*.json" if a.truth != "issue" else f"{a.report}.judge-*.json"
        js = [json.loads(p.read_text()) for p in (r["work"] / "agent").glob(pat) if a.truth != "issue" or ".judge-visible-" not in p.name and ".judge-ticket-" not in p.name]
        if len(js) < 2:
            continue
        keys = ("steps", "actual", "verdict", "video") if a.truth == "ticket" else ("steps", "actual", "verdict")
        sc = sum(j.get(k, 0) for j in js for k in keys) / (2 * len(keys) * len(js))
        if sc >= a.below:
            continue
        lab = r["label"]
        items.append(f"## {r['id']} - {sc:.0%}\nlabel: shows_bug {lab['shows_bug']}, control {lab['control']}; decisive: {lab.get('decisive')}; not visible: {lab.get('not_visible')}\n"
                     + "\n".join(f"- {j.get('judge')}: {' '.join(f'{k} {j.get(k)}' for k in keys)}. {j.get('notes', '')} Invented: {j.get('invented')}" for j in js))
    prompt = ASK.format(below=a.below, items="\n\n".join(items))
    cmd = [shutil.which("copilot") or "copilot", "-p", prompt, "--model", a.model, "--available-tools", "", "--no-ask-user",
           "--no-custom-instructions", "--no-auto-update", "-s"]
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", timeout=1800)
    out = OUT / "triage" / f"{a.report}.{a.truth}.md"
    out.parent.mkdir(exist_ok=True)
    out.write_text(f"# Triage: {a.report} against {a.truth}, {len(items)} recordings under {a.below:.0%}\n\n" + re.sub(r"^\s+", "", p.stdout), encoding="utf-8")
    print(f"{len(items)} recordings under {a.below:.0%} -> {out}")


if __name__ == "__main__":
    main()
