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
  hovers without a click, checks the author made afterwards. Repeated attempts are one step ("repeat: fails 4 of 5
  times"). Every step cites the event ids it rests on, and its time and action come from the timeline or a frame you
  opened at that time, not from an estimate.
- The strongest evidence is often a contrast inside the video: the same action working at one moment or place and
  failing at another. Look for it and give both moments.
- Counts and "always", "never", "every" only after checking each occurrence; otherwise say "in the ones checked". The
  video not showing something does not refute it: call a claim refuted only when the video shows the opposite.
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

BOTH_TASK = """Two views of one video are in the current folder. timeline.md is the parser's timeline: exact times, clicks and
hovers, what appeared, moved, flickered or flashed for a fraction of a second, cross-checks - precise, but it reads
the screen as text and boxes and may miss what a picture means. direct/frames/ holds frames of the whole video every
{step} s, named by time (direct/frames/0012.5.jpg is the frame at 12.5 s): what the screen looks like, but a short
event between two frames is not there. Use both: read the timeline, look through the frames, and where the timeline
points at a moment, open the frames around it; where a frame shows something odd, check the timeline at that time.
Then answer with a single JSON object, and nothing else, that follows this JSON schema:

{schema}"""

INVESTIGATE_TASK = """Three things about one video are in the current folder.
- watcher.md: notes of a first reader who watched only the frames, with no parser: what looked wrong and when. A
  good eye for what a picture means, but it guesses at actions and misses anything shorter than its frame step.
- timeline.md: the parser's timeline: exact times, clicks and hovers, what appeared, moved, flickered or flashed for a
  fraction of a second, cross-checks. Precise, but it reads the screen as text and boxes.
- direct/frames/: frames of the whole video every {step} s, named by time (direct/frames/0012.5.jpg = 12.5 s).
The timeline marks short events with "moment frames/moments/<id>.jpg": a strip of every frame around the event,
cropped to it and enlarged. The frames in direct/frames/ are {step} s apart and miss anything shorter, so before you
accept or drop a problem that rests on a short event (a flash, a jump, a flicker, a vanished icon), open its moment.
You are the investigator. Take each problem the watcher names and each odd moment in the timeline, and check it
against the other source: does the timeline confirm it at that time, do the frames around it show it? Keep what holds,
drop what does not, and say which source settled it. Where they disagree, open the frames and decide. The repro steps
come from the timeline where it has them (exact clicks and times), the meaning of the problem from what the frames show.
Then answer with a single JSON object, and nothing else, that follows this JSON schema:

{schema}"""

TOOLS_NOTE = """
You can also ask the video yourself with the vrp command (run it in this folder; times in seconds, boxes in pixels as in
the timeline). Use it when a moment matters and the frames or the timeline leave a doubt:
  vrp events --near 12.5 --window 1        what the timeline has around a moment
  vrp look --from 4.0 --to 4.4 --box x,y,w,h --scale 3   every frame of a short span, cropped and enlarged; open the
                                           sheet.jpg it prints
  vrp diff --box x,y,w,h --at 4.0 --to 4.4 how an area differs between two moments (brightness, drawing kept or new,
                                           text before and after) and a side-by-side image
  vrp ocr --at 4.2 --box x,y,w,h           the text in an area at a moment
  vrp find --text "Connecting" --from 3 --to 6 [--box x,y,w,h]   every frame of a span searched for a text: finds a
                                           state that lasts a single frame (slow: keep the span short, add a box)
When the ticket names a message or a state that shows only briefly, search for it with vrp find.
"""

TICKET_NOTE = """
ticket.md in this folder is the ticket as the reporter filed it. Together with the video it is your input: the ticket
says what the reporter believes, the video is the evidence. Use the video to make the steps exact (what was clicked,
when), to find the moment that proves the problem, and to check the ticket's claims. Say where the video and the
ticket disagree, and what the video shows that the ticket does not say (a setting on screen, a step the reporter
skipped, a value, a version). Do not copy the ticket's claims as facts of the video when the video does not show them.
"""

TICKET_ONLY = """ticket.md in the current folder is a bug ticket as the reporter filed it. There is no video: write the report
from the ticket alone, and say what stays unclear. Answer with a single JSON object, and nothing else, that follows
this JSON schema (step times are 0 and event ids are empty when the ticket gives none):

{schema}"""

FRAMES_SYSTEM = """You turn a work video into a report a developer can act on. You get no parser output: only frames of the
video taken at a fixed step, each named by its time (frames/0012.5.jpg is the frame at 12.5 s). There is no sound.

How to work:
- Open the frames in order and follow what the user does and what the screen does; open more of them where something
  changes quickly. Clicks, taps and keys are not marked: infer them from what you see, and say when you infer.
- A bug video was recorded to show a problem. If no action visibly fails, look for what looks or behaves wrong: an
  icon or text that vanishes or becomes unreadable, a layout that jumps or flickers, a wrong value, a long delay.
- The class is not-a-bug only when the screen shows the author's own mistake or explains the behaviour; not merely
  because no error appears. If you cannot tell what is wrong, say so and name the most likely candidate.
- Repro steps are the minimal sequence that reproduces the problem. Every step cites the frames it rests on: in the
  schema, event ids are frame names (0012.5) and t_ms is the frame time.
- Write in English, plainly, without guessing beyond what the frames show."""

FRAMES_TASK = """frames/ in the current folder holds the frames of one video every {step} s, {n} frames, {w}x{h}, {dur:.1f} s long.{dense}
Open them, then answer with a single JSON object, and nothing else, that follows this JSON schema:

{schema}"""


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


def sample_frames(work: Path, dense: bool = False) -> tuple[Path, dict]:
    """The video's frames at a fixed step into parsed/direct/frames, for a model that reads frames. dense: plus every
    frame around the short events the parser found (named with three decimals, 0012.533.jpg), so a one-frame change is
    among the frames the model goes through anyway."""
    import av

    from vrp.moments import wanted

    name = json.loads((work / "run.json").read_text())["video"]
    video = next(p for p in (work.parent / name, work.parent.parent / name) if p.exists())
    windows = []
    if dense and (work / "evidence.json").exists():
        evs = json.loads((work / "evidence.json").read_text())["events"]
        top = sorted((r, e["t_ms"], i, e) for i, e in enumerate(evs) if (r := wanted(e)) is not None)[:30]
        windows = [(e["t_ms"] / 1000 - 0.15, min((e.get("end_ms") or e["t_ms"]) / 1000 + 0.25, e["t_ms"] / 1000 + 1.85)) for _, _, _, e in top]
    out = work / "direct"
    fr = out / "frames"
    fr.mkdir(parents=True, exist_ok=True)
    for f in fr.glob("*.jpg"):
        f.unlink()
    with av.open(str(video)) as c:
        vs = c.streams.video[0]
        dur = float(c.duration or 0) / 1e6
        step = 0.5 if dur <= 60 else 1.0 if dur <= 150 else max(2.0, dur / 150)
        nxt, n, extra, last, size = 0.0, 0, 0, -1.0, (vs.codec_context.width, vs.codec_context.height)
        for f in c.decode(vs):
            t = float(f.pts * vs.time_base) if f.pts is not None else nxt
            regular = t + 1e-6 >= nxt
            near = extra < 150 and t - last >= 1 / 31 and any(a <= t <= b for a, b in windows)
            if not (regular or near):
                continue
            img = f.to_image()
            if img.width > 1280:
                img = img.resize((1280, round(img.height * 1280 / img.width)))
            if regular:
                img.save(fr / f"{nxt:06.1f}.jpg", quality=88)
                n += 1
                nxt += step
            else:
                img.save(fr / f"{t:08.3f}.jpg", quality=88)
                extra += 1
            last = t
    return out, {"step": step, "n": n, "w": size[0], "h": size[1], "dur": dur, "extra": extra, "around": len(windows)}


def answer_json(text: str) -> dict:
    m = re.findall(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.S)
    raw = m[-1] if m else text[text.find("{"): text.rfind("}") + 1]
    r = json.loads(raw)
    if r.get("kind") not in ("bug", "meeting") or "summary" not in r or (r["kind"] == "bug" and not r.get("bug")) or (r["kind"] == "meeting" and r.get("requirements") is None):
        raise ValueError("answer does not follow the schema")
    return r


def tag(model: str, effort: str | None) -> str:
    return f"{model.replace(':', '-')}@{effort or 'default'}"


def run(key: str, variant: str | None, model: str, effort: str | None, local: bool = False, input_: str = "text", vision: bool = True, tools: bool = False, ticket: bool = False, home: Path | None = None, ticket_file: Path | None = None, dense: bool = False) -> dict:
    """One headless Copilot CLI session; its JSON event stream gives the answer, the frames opened and the usage."""
    home = home or OUT / key  # a video anywhere: its folder; the test set: out/<key>
    work = home / (f"parsed-{variant}" if variant else "parsed")
    if input_ == "pages":
        pages(work)
    if input_ == "frames":  # baseline: the model watches the frames itself, no parser
        work, facts = sample_frames(work, dense)
        more = (f"\nAround {facts['around']} short changes the video also has every frame ({facts['extra']} more frames, named with three "
                "decimals, e.g. 0012.533.jpg): a change that lasts a single frame is there. Look at those runs closely.") if facts.get("extra") else ""
        prompt = FRAMES_SYSTEM + "\n\n" + FRAMES_TASK.format(schema=json.dumps(SCHEMA, indent=1), dense=more, **facts)
    elif input_ == "investigate":  # second pass: the frames-only report as a lead, checked against the timeline
        facts = sample_frames(work, dense)[1]
        w = work / "agent" / f"{tag(model, effort)}+frames{'+dense' if dense else ''}{'+ticket' if ticket else ''}.md"
        if not w.exists():
            raise RuntimeError(f"{key}: no watcher report {w.name}, run --input frames first")
        (work / "watcher.md").write_text(w.read_text(encoding="utf-8").replace("frames/", "direct/frames/"), encoding="utf-8")
        prompt = SYSTEM + "\n\n" + INVESTIGATE_TASK.format(schema=json.dumps(SCHEMA, indent=1), step=facts["step"]) + (TOOLS_NOTE if tools else "")
    elif input_ == "none":  # baseline for the ticket setting: the ticket alone, no video
        work = work / "ticketonly"
        work.mkdir(exist_ok=True)
        prompt = TICKET_ONLY.format(schema=json.dumps(SCHEMA, indent=1))
    elif input_ == "both":  # the parser's timeline as precise eyes, the frames for what things look like
        facts = sample_frames(work)[1]
        prompt = SYSTEM + "\n\n" + BOTH_TASK.format(schema=json.dumps(SCHEMA, indent=1), step=facts["step"])
    else:
        prompt = SYSTEM + "\n\n" + (PAGES_TASK if input_ == "pages" else TASK).format(schema=json.dumps(SCHEMA, indent=1))
    if ticket:
        t = ticket_file or home / "ticket.md"
        if not t.exists():
            raise RuntimeError(f"{key}: no ticket.md")
        (work / "ticket.md").write_text(t.read_text(encoding="utf-8"), encoding="utf-8")
        prompt += "" if input_ == "none" else TICKET_NOTE
    cmd = [shutil.which("copilot") or "copilot", "-p", prompt, "--model", model, "--available-tools", "view", "--allow-all-tools",
           "--no-ask-user", "--no-custom-instructions", "--no-auto-update", "--output-format", "json"]
    if effort:
        cmd += ["--reasoning-effort", effort]
    env = None
    if tools:  # the shell, but only for vrp: the parser on demand
        i = cmd.index("--available-tools")
        cmd[i + 1:i + 2] = ["view", "bash", "shell"]
        cmd[cmd.index("--allow-all-tools"):cmd.index("--allow-all-tools") + 1] = ["--allow-tool", "view", "--allow-tool", "shell(vrp:*)"]
        env = {**os.environ, "PATH": str(Path(__file__).resolve().parent / "bin") + os.pathsep + os.environ.get("PATH", "")}
    if local:  # a model served by Ollama on this machine, through the same Copilot CLI
        env = {**(env or os.environ), "COPILOT_PROVIDER_BASE_URL": "http://127.0.0.1:11434/v1", "COPILOT_MODEL": model, "COPILOT_PROVIDER_VISION": "true" if vision else "false",
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
        looked = [x[x.index(k):] for x in looked for k in ("frames", "looks") if k in x][:200]  # pages of the timeline are input, not looks
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
    ap.add_argument("--input", default="text", choices=["text", "pages", "frames", "both", "investigate", "none"], help="timeline as text or as images of its pages; frames - no parser, the model gets frames only (baseline); both - timeline and frames; investigate - the frames-only report checked against the timeline")
    ap.add_argument("--local", action="store_true", help="the model is served by Ollama on this machine")
    ap.add_argument("--dense", action="store_true", help="frames/investigate: every frame around the short events the parser found, among the regular frames")
    ap.add_argument("--ticket", action="store_true", help="real recordings: the reporter's ticket (out/<key>/ticket.md) goes in with the video")
    ap.add_argument("--tools", action="store_true", help="investigate: the model may run vrp (look, diff, ocr, events) to ask the video itself")
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
        name = tag(a.model, a.effort) + ("" if a.input == "text" else f"+{a.input}") + ("+tools" if a.tools else "") + ("+dense" if a.dense else "") + ("+ticket" if a.ticket else "")
        if (out / f"{name}.json").exists() and not a.force:
            continue
        try:
            r = run(key, a.variant, a.model, a.effort, a.local, a.input, not a.text_only, a.tools, a.ticket, dense=a.dense)
        except (RuntimeError, subprocess.TimeoutExpired) as ex:
            print(f"{key}: failed: {ex}", flush=True)
            continue
        finally:  # the ticket copy must not leak into a later run made without it
            for d in ("", "direct", "ticketonly"):
                (OUT / key / suffix / d / "ticket.md").unlink(missing_ok=True)
        out.mkdir(exist_ok=True)
        (out / f"{name}.json").write_text(json.dumps(r, ensure_ascii=False, indent=1), encoding="utf-8")
        (out / f"{name}.md").write_text(to_md(key, r), encoding="utf-8")
        print(f"{key} {name}: {r['kind']}, {(r.get('bug') or {}).get('class') or len(r.get('requirements') or [])}, looked {len(r['looked'])}, {r['seconds']} s, {r.get('premium_requests')} req", flush=True)
