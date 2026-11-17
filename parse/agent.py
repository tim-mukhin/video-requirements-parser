"""Agent on top of the parser: reads timeline.md, may look at frames, writes a bug report or meeting requirements.

python agent.py [--model claude-opus-5.5] [--effort high] [--variant low] [<lang>/<id> ...]

The agent is GitHub Copilot CLI in headless mode (`copilot -p`), run inside the parsed folder with only its file
viewer: it reads timeline.md and frames there, cannot run commands, write files or open paths outside the folder,
so the ground truth stays out of reach. Its answer is JSON checked against SCHEMA.
out/<lang>/<id>/parsed[-variant]/agent/<model>@<effort>.json and .md
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import time
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "out"
TIMEOUT_S = 1200

SYSTEM = """You turn the facts extracted from a work video into a report a developer can act on.

The input is a timeline produced by a deterministic parser: what was said (speech recognition, may mishear words),
what appeared, disappeared or changed on the screen (OCR, may misread characters), clicks and hovers of the cursor,
which window was in front, what a pointing word referred to, and cross-checks at the top. Event ids in square brackets
(p012, u004) point to evidence; frames are paths relative to the parsed folder.

How to work:
- The screen is the evidence, speech is the author's view of it. When they disagree, the screen wins, and the
  disagreement itself is a finding (the author says "Send" but the click landed elsewhere, says "it went through" while
  an error flashed).
- A click with no text ("CLICK at [x, y]") hit an icon or an unread control. If it matters for the steps, look at the
  frame to see what it was.
- The "User input" line says how much of the user's own actions the video shows. Where clicks, taps or keys are not
  seen, a window, menu or page that opens was still most likely opened by the user: write "opened (the trigger is not
  visible)", never "by itself" or "with no input", unless the cursor was followed and stood still at that moment.
  Where the cursor is followed, do not assume a click the timeline does not show: a HOVER is not a click.
- Something that flashed for a fraction of a second, or changed in a window behind the front one, is easy to miss for
  the author and is often the real cause.
- Claims about the past, other devices, other people's words or guesses ("it used to work", "he says", "maybe it's
  too big") are not facts of the video. Report them as claims; if the screen refutes one, say so.
- Repro steps are the minimal sequence that reproduces the problem: leave out fumbles, wrong picks that were undone,
  hovers without a click, checks the author made afterwards. Every step cites the event ids it rests on.
- A bug video was recorded to show a problem. If no action visibly fails, look for what looks or behaves wrong: an
  icon or text that vanishes or becomes unreadable, a layout that jumps or flickers, a wrong value, a long delay.
- The class is not-a-bug only when the screen shows the author's own mistake (a wrong pick, a wrong chat, a setting
  they changed) or explains the behaviour; not merely because no error appears. Say what really happened. If you
  cannot tell what is wrong, say so and name the most likely candidate.
- A meeting (slides, several speakers) gets requirements instead of a bug report: what was stated, proposed, decided,
  rejected or left as an open question, who proposed and who decided, with the utterance ids. A proposal nobody
  accepted is not a decision; what the slides or notes say is not decided until the meeting decides it.
- Look at a frame when it would settle a doubt (frames/<n>.jpg are evidence frames named in the timeline,
  frames/crops/<event id>.jpg are cut-outs of single events); do not look just to confirm what the text already says.
- Write in English, plainly, without guessing beyond the evidence."""

SCHEMA = {
            "type": "object",
            "properties": {
                "kind": {"type": "string", "enum": ["bug", "meeting"]},
                "summary": {"type": "string", "description": "Two or three sentences: what happens and why it matters."},
                "bug": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "class": {"type": "string", "enum": ["error-shown", "silent-fail", "wrong-data", "state-revert", "stuck", "intermittent", "not-a-bug"]},
                        "environment": {"type": "string", "description": "Apps, windows, accounts and organizations seen."},
                        "steps": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {"text": {"type": "string"}, "t_ms": {"type": "integer"}, "events": {"type": "array", "items": {"type": "string"}}},
                                "required": ["text", "t_ms", "events"],
                            },
                        },
                        "expected": {"type": "object", "properties": {"text": {"type": "string"}, "source": {"type": "string", "enum": ["speech", "implied"]}}, "required": ["text", "source"]},
                        "actual": {"type": "string"},
                        "key_events": {"type": "array", "items": {"type": "string"}, "description": "Ids of the events the conclusion rests on."},
                        "claims": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {"text": {"type": "string"}, "utterance": {"type": "string"}, "verdict": {"type": "string", "enum": ["confirmed", "refuted", "not shown"]}, "why": {"type": "string"}},
                                "required": ["text", "utterance", "verdict"],
                            },
                        },
                        "missed_by_author": {"type": "array", "items": {"type": "string"}, "description": "Facts on screen the author did not notice or mention, with event ids."},
                    },
                    "required": ["title", "class", "steps", "expected", "actual", "key_events", "claims"],
                },
                "requirements": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string"},
                            "text": {"type": "string"},
                            "status": {"type": "string", "enum": ["stated", "proposed", "decided", "rejected", "open_question"]},
                            "proposed_by": {"type": ["string", "null"]},
                            "decided_by": {"type": ["string", "null"]},
                            "evidence": {"type": "array", "items": {"type": "string"}},
                        },
                        "required": ["id", "text", "status", "evidence"],
                    },
                },
            },
            "required": ["kind", "summary"],
        }

TASK = """Read timeline.md in the current folder: the parser's timeline of one video. Look at frames when needed.
Then answer with a single JSON object, and nothing else, that follows this JSON schema:

{schema}"""


PAGES_TASK = """The parser's timeline of one video is given as images, pages/page-01.png, pages/page-02.png and so on: open
all of them in order and read them as the timeline. Look at frames when needed.
Then answer with a single JSON object, and nothing else, that follows this JSON schema:

{schema}"""
PAGE_LINES = 60


def font(size: int):
    from PIL import ImageFont

    for f in ("/System/Library/Fonts/Menlo.ttc", "C:/Windows/Fonts/consola.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"):
        if Path(f).exists():
            return ImageFont.truetype(f, size)
    return ImageFont.load_default(size)


def pages(work: Path) -> int:
    """timeline.md drawn as pages of monospace text, long lines wrapped."""
    from PIL import Image, ImageDraw

    out = work / "pages"
    out.mkdir(exist_ok=True)
    for f in out.glob("*.png"):
        f.unlink()
    lines = []
    for ln in (work / "timeline.md").read_text(encoding="utf-8").splitlines():
        while len(ln) > 130:
            lines.append(ln[:130])
            ln = "    " + ln[130:]
        lines.append(ln)
    fnt = font(18)
    n = 0
    for i in range(0, len(lines), PAGE_LINES):
        img = Image.new("RGB", (1600, 40 + PAGE_LINES * 24), "white")
        d = ImageDraw.Draw(img)
        for j, ln in enumerate(lines[i:i + PAGE_LINES]):
            d.text((20, 20 + j * 24), ln, fill="black", font=fnt)
        n += 1
        img.save(out / f"page-{n:02d}.png")
    return n


def answer_json(text: str) -> dict:
    m = re.findall(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.S)
    raw = m[-1] if m else text[text.find("{"): text.rfind("}") + 1]
    r = json.loads(raw)
    if r.get("kind") not in ("bug", "meeting") or "summary" not in r or (r["kind"] == "bug" and not r.get("bug")) or (r["kind"] == "meeting" and r.get("requirements") is None):
        raise ValueError("answer does not follow the schema")
    return r


def tag(model: str, effort: str | None) -> str:
    return f"{model.replace(':', '-')}@{effort or 'default'}"


def run(key: str, variant: str | None, model: str, effort: str | None, local: bool = False, input_: str = "text", vision: bool = True) -> dict:
    """One headless Copilot CLI session; its JSON event stream gives the answer, the frames opened and the usage."""
    work = OUT / key / (f"parsed-{variant}" if variant else "parsed")
    if input_ == "pages":
        pages(work)
    prompt = SYSTEM + "\n\n" + (PAGES_TASK if input_ == "pages" else TASK).format(schema=json.dumps(SCHEMA, indent=1))
    cmd = [shutil.which("copilot") or "copilot", "-p", prompt, "--model", model, "--available-tools", "view", "--allow-all-tools",
           "--no-ask-user", "--no-custom-instructions", "--no-auto-update", "--output-format", "json"]
    if effort:
        cmd += ["--reasoning-effort", effort]
    env = None
    if local:  # a model served by Ollama on this machine, through the same Copilot CLI
        env = {**os.environ, "COPILOT_PROVIDER_BASE_URL": "http://127.0.0.1:11434/v1", "COPILOT_MODEL": model, "COPILOT_PROVIDER_VISION": "true" if vision else "false",
               "COPILOT_PROVIDER_MAX_PROMPT_TOKENS": "32768", "COPILOT_PROVIDER_MAX_OUTPUT_TOKENS": "8192"}
        cmd = [c for c in cmd if c not in ("--model", model)]
    err = ""
    nudge = "You stopped before the answer. Answer now with the single JSON object that follows the schema, and nothing else."

    def session(c: list[str]) -> tuple[str, list[str], dict, str | None]:
        p = subprocess.run(c, cwd=work, capture_output=True, text=True, encoding="utf-8", timeout=TIMEOUT_S, env=env)
        final, looked, usage, sid = "", [], {}, None
        for line in p.stdout.splitlines():
            try:
                o = json.loads(line)
            except json.JSONDecodeError:
                continue
            d = o.get("data") or {}
            if o.get("type") == "session.start":
                sid = d.get("sessionId")
            elif o.get("type") == "assistant.message":
                final = d.get("content") or final
                looked += [(t.get("arguments") or {}).get("path", "") for t in d.get("toolRequests") or [] if t.get("name") == "view"]
            elif o.get("type") == "session.usage_checkpoint":
                usage["nano_aiu"] = d.get("totalNanoAiu")
            elif o.get("type") == "result":
                usage.update({"premium_requests": (o.get("usage") or {}).get("premiumRequests"), "exit": o.get("exitCode")})
        return final, looked, usage, sid

    for _ in range(2):
        t0 = time.time()
        final, looked, usage, sid = session(cmd)
        ans = None
        for nudged in (False, True):  # weaker models may stop at "let me look closer": ask once in the same session
            try:
                ans = answer_json(final)
                break
            except (ValueError, json.JSONDecodeError) as ex:
                err = f"{ex}; answer tail: {final[-400:]!r}"
                if nudged or not sid:
                    break
                i = cmd.index("-p")
                final, more, extra, _ = session(cmd[:i] + ["--resume", sid, "-p", nudge] + cmd[i + 2:])
                looked += more
                usage["premium_requests"] = (usage.get("premium_requests") or 0) + (extra.get("premium_requests") or 0)
                usage["nano_aiu"] = (usage.get("nano_aiu") or 0) + (extra.get("nano_aiu") or 0)
                usage["nudged"] = True
        if ans is None:
            continue
        looked = [x[x.index("frames"):] for x in looked if "frames" in x]  # pages of the timeline are input, not looks
        return {"model": model, "effort": effort, "input": input_, "seconds": round(time.time() - t0), **usage, **ans, "looked": looked}
    raise RuntimeError(f"{key}: {err}")


def ts(ms: int) -> str:
    return f"{ms // 60000:02d}:{ms % 60000 / 1000:04.1f}"


def to_md(key: str, r: dict) -> str:
    lines = [f"# {key}", "", f"_{tag(r['model'], r.get('effort'))}, {r.get('seconds')} s; looked at: {', '.join(r.get('looked') or []) or 'nothing'}_", "", r["summary"], ""]
    b = r.get("bug")
    if r["kind"] == "bug" and b:
        lines += [f"## {b['title']}", "", f"Class: **{b['class']}**", ""]
        if b.get("environment"):
            lines += [f"Environment: {b['environment']}", ""]
        lines += ["Steps:", ""] + [f"{i + 1}. {s['text']} ({ts(s['t_ms'])}; {', '.join(s['events'])})" for i, s in enumerate(b["steps"])]
        lines += ["", f"Expected ({b['expected']['source']}): {b['expected']['text']}", "", f"Actual: {b['actual']}", "", f"Key events: {', '.join(b['key_events'])}"]
        if b.get("missed_by_author"):
            lines += ["", "Missed by the author:", ""] + [f"- {m}" for m in b["missed_by_author"]]
        if b.get("claims"):
            lines += ["", "Claims:", ""] + [f"- \"{c['text']}\" [{c['utterance']}]: {c['verdict']}" + (f" - {c['why']}" if c.get("why") else "") for c in b["claims"]]
    for q in r.get("requirements") or []:
        who = ", ".join(x for x in (q.get("proposed_by") and f"proposed by {q['proposed_by']}", q.get("decided_by") and f"decided by {q['decided_by']}") if x)
        lines.append(f"- **{q['id']}** [{q['status']}] {q['text']}" + (f" ({who})" if who else "") + f" - {', '.join(q['evidence'])}")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("ids", nargs="*")
    ap.add_argument("--variant")
    ap.add_argument("--model", default="claude-opus-5.5")
    ap.add_argument("--effort", help="reasoning effort: low, medium, high, xhigh ...; default - the model's own")
    ap.add_argument("--input", default="text", choices=["text", "pages"], help="timeline as text or as images of its pages")
    ap.add_argument("--local", action="store_true", help="the model is served by Ollama on this machine")
    ap.add_argument("--text-only", action="store_true", help="a local model that takes no images")
    ap.add_argument("--force", action="store_true", help="redo videos that already have a report from this model")
    a = ap.parse_args()
    suffix = f"parsed-{a.variant}" if a.variant else "parsed"
    keys = a.ids or sorted(f"{p.parts[-4]}/{p.parts[-3]}" for p in OUT.glob(f"*/*/{suffix}/timeline.md"))
    for key in keys:
        if not (OUT / key / suffix / "timeline.md").exists():
            print(f"{key}: no timeline.md, parse the video first", flush=True)
            continue
        out = OUT / key / suffix / "agent"
        name = tag(a.model, a.effort) + ("+pages" if a.input == "pages" else "")
        if (out / f"{name}.json").exists() and not a.force:
            continue
        try:
            r = run(key, a.variant, a.model, a.effort, a.local, a.input, not a.text_only)
        except (RuntimeError, subprocess.TimeoutExpired) as ex:
            print(f"{key}: failed: {ex}", flush=True)
            continue
        out.mkdir(exist_ok=True)
        (out / f"{name}.json").write_text(json.dumps(r, ensure_ascii=False, indent=1), encoding="utf-8")
        (out / f"{name}.md").write_text(to_md(key, r), encoding="utf-8")
        print(f"{key} {name}: {r['kind']}, {(r.get('bug') or {}).get('class') or len(r.get('requirements') or [])}, looked {len(r['looked'])}, {r['seconds']} s, {r.get('premium_requests')} req", flush=True)
