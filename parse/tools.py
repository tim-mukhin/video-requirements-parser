"""vrp: a bug video (and its ticket) to a report; the parser on demand for a closer look at one moment.

  vrp report <video> [--ticket ticket.md] [--model claude-sonnet-5.5] [--speech-lang auto|en|ru]
                                               the whole pipeline: parse the video, a watcher reads the frames, an
                                               investigator checks them against the timeline and asks the video with
                                               the commands below; writes <video>.report.md next to the video
The other commands run in a parsed folder (or pass --work); they print plain lines and the paths of images they save.
  vrp events --near 12.5 [--window 2]          what the timeline has around a moment, speech included
  vrp look --from 4.0 --to 4.4 [--box x,y,w,h] [--fps native|N] [--scale 2]
                                               every frame of a span (native rate by default), cropped and enlarged
  vrp diff --box x,y,w,h --at 4.0 --to 4.4     how an area differs between two moments: brightness, drawing kept or
                                               new, the text before and after, both crops side by side
  vrp ocr --at 4.2 [--box x,y,w,h]             the text on screen at a moment
  vrp find --text "Connecting" [--from 0 --to 30] [--box x,y,w,h]
                                               every frame of a span searched for a text, so a state that lasts one
                                               frame is found; prints when it was visible and for how many frames
Times are seconds from the start of the video; boxes are full-frame pixels, as in the timeline.
"""
import argparse
import json
import sys
from pathlib import Path

import av
import cv2
import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
from vrp import ocr as ocr_engine  # noqa: E402
from vrp.events import look as look_numbers, look_words  # noqa: E402
from vrp.timeline import describe, ts  # noqa: E402

MAX_FRAMES = 24


def video_of(work: Path) -> Path:
    name = json.loads((work / "run.json").read_text())["video"]
    return next(p for p in (work.parent / name, work.parent.parent / name) if p.exists())


def frames(video: Path, t0: float, t1: float, fps: float | None) -> list[tuple[float, np.ndarray]]:
    """Frames with their own times from t0 to t1; fps None - every frame the video has. A screen recorder may write no
    frame while nothing changes, so the frame on screen at t0 (the last one before it) comes first."""
    out, nxt, prev = [], t0, None
    with av.open(str(video)) as c:
        vs = c.streams.video[0]
        c.seek(int(max(0.0, t0 - 1.0) / vs.time_base), stream=vs, backward=True)
        for f in c.decode(vs):
            t = float(f.pts * vs.time_base)
            if t < t0 - 1e-3:
                prev = f
                continue
            if t > t1 + 1e-3:
                break
            if fps is None or t + 1e-6 >= nxt:
                out.append((t, f.to_ndarray(format="bgr24")))
                nxt = t + 1 / fps if fps else nxt
    if prev is not None and (not out or out[0][0] > t0 + 1e-3):
        out.insert(0, (float(prev.pts * prev.time_base), prev.to_ndarray(format="bgr24")))
    return out


def at(video: Path, t: float) -> np.ndarray:
    """The frame on screen at t: the last one at or before it."""
    got = frames(video, t, t, None)
    return got[0][1]


def crop(img: np.ndarray, box: list[int] | None, scale: float) -> np.ndarray:
    if box:
        x, y, w, h = box
        pad = max(8, round(0.15 * max(w, h)))
        img = img[max(0, y - pad):y + h + pad, max(0, x - pad):x + w + pad]
    return cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_NEAREST) if scale != 1 else img


def label(img: np.ndarray, text: str) -> np.ndarray:
    img = img.copy()
    cv2.rectangle(img, (0, 0), (8 * len(text) + 8, 18), (0, 0, 0), -1)
    cv2.putText(img, text, (4, 13), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1, cv2.LINE_AA)
    return img


def sheet(images: list[np.ndarray], cols: int = 4) -> np.ndarray:
    h, w = max(i.shape[0] for i in images), max(i.shape[1] for i in images)
    tiles = [cv2.copyMakeBorder(i, 0, h - i.shape[0] + 4, 0, w - i.shape[1] + 4, cv2.BORDER_CONSTANT, value=(255, 255, 255)) for i in images]
    tiles += [np.full_like(tiles[0], 255)] * (-len(tiles) % cols)
    return np.vstack([np.hstack(tiles[r:r + cols]) for r in range(0, len(tiles), cols)])


def cmd_events(work: Path, a) -> None:
    ev = json.loads((work / "evidence.json").read_text())
    lo, hi = (a.near - a.window) * 1000, (a.near + a.window) * 1000
    rows = [(e["t_ms"], f'{ts(e["t_ms"])}  {describe(e)}  [{e["id"]}]' + (f"  box {e['bbox']}" if e.get("bbox") else "")) for e in ev["events"] if lo <= e["t_ms"] <= hi]
    rows += [(u["start_ms"], f'{ts(u["start_ms"])}  SAID: "{u["text"]}"  [{u["id"]}]') for u in ev["speech"]["utterances"] if lo <= u["start_ms"] <= hi]
    for s in ev["screens"]:
        if s["start_ms"] <= a.near * 1000 < s["end_ms"]:
            rows.append((s["start_ms"] - 1, f'{ts(s["start_ms"])}-{ts(s["end_ms"])}  SCREEN STATE {s["id"]}: {" | ".join(t["text"] for t in s["texts"])[:400]}'))
    for _, line in sorted(rows) or [(0, f"nothing in the timeline within {a.window} s of {a.near} s")]:
        print(line)


def cmd_look(work: Path, a) -> None:
    video = video_of(work)
    got = frames(video, a.t_from, a.t_to, None if a.fps == "native" else float(a.fps))
    if len(got) > MAX_FRAMES:
        got = [got[round(i * (len(got) - 1) / (MAX_FRAMES - 1))] for i in range(MAX_FRAMES)]
        print(f"more than {MAX_FRAMES} frames in the span: showing {MAX_FRAMES} spread evenly; narrow the span for every frame")
    box = [int(v) for v in a.box.split(",")] if a.box else None
    out = work / "looks" / (f"{a.t_from:07.2f}-{a.t_to:07.2f}" + (f"-{'_'.join(map(str, box))}" if box else ""))
    out.mkdir(parents=True, exist_ok=True)
    tiles = []
    for t, img in got:
        c = crop(img, box, a.scale)
        p = out / f"{t:07.3f}.jpg"
        cv2.imwrite(str(p), c, [cv2.IMWRITE_JPEG_QUALITY, 92])
        tiles.append(label(c, f"{t:.3f} s"))
        print(p.relative_to(work).as_posix())
    if tiles:
        cv2.imwrite(str(out / "sheet.jpg"), sheet(tiles), [cv2.IMWRITE_JPEG_QUALITY, 90])
        print(f"{(out / 'sheet.jpg').relative_to(work).as_posix()}  all {len(tiles)} frames side by side")


def read_box(img: np.ndarray, box: list[int] | None, lang: str) -> list[str]:
    x, y, w, h = box or [0, 0, img.shape[1], img.shape[0]]
    pil = Image.fromarray(cv2.cvtColor(img[y:y + h, x:x + w], cv2.COLOR_BGR2RGB))
    f = max(1.0, 400 / max(1, min(pil.size)))
    if f > 1:
        pil = pil.resize((round(pil.width * f), round(pil.height * f)), Image.LANCZOS)
    return [f'"{t}" at [{round(x + b[0] / f)}, {round(y + b[1] / f)}, {round(b[2] / f)}, {round(b[3] / f)}]' for t, b in ocr_engine.read(pil, lang)]


def cmd_diff(work: Path, a) -> None:
    video = video_of(work)
    box = [int(v) for v in a.box.split(",")]
    i0, i1 = at(video, a.at), at(video, a.to)
    lk = look_numbers(i0, i1, box)
    print(f"box {box}: brightness {lk['light'][0]} -> {lk['light'][1]} (0-255)" + (f"; {look_words(lk)}" if look_words(lk) else ""))
    if "kept" in lk:
        print(f"of what was drawn inside at {a.at} s, {lk['kept']:.0%} is still drawn at {a.to} s")
    if "new" in lk:
        print(f"of what is drawn inside at {a.to} s, {lk['new']:.0%} is new")
    for t, img in ((a.at, i0), (a.to, i1)):
        texts = read_box(img, box, a.lang)
        print(f"text at {t} s: " + ("; ".join(texts) if texts else "none"))
    out = work / "looks" / f"diff-{a.at:07.2f}-{a.to:07.2f}-{'_'.join(map(str, box))}.jpg"
    out.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(out), sheet([label(crop(i0, box, a.scale), f"{a.at} s"), label(crop(i1, box, a.scale), f"{a.to} s")], cols=2))
    print(out.relative_to(work).as_posix())


def cmd_ocr(work: Path, a) -> None:
    box = [int(v) for v in a.box.split(",")] if a.box else None
    texts = read_box(at(video_of(work), a.at), box, a.lang)
    print("\n".join(texts) if texts else "no text read")


def cmd_find(work: Path, a) -> None:
    from rapidfuzz import fuzz

    video = video_of(work)
    box = [int(v) for v in a.box.split(",")] if a.box else None
    t1 = a.t_to if a.t_to is not None else 1e9
    want = a.text.lower()
    hits, prev, last_hit, n, read = [], None, False, 0, 0
    with av.open(str(video)) as c:
        vs = c.streams.video[0]
        if a.t_from > 1:
            c.seek(int((a.t_from - 1) / vs.time_base), stream=vs, backward=True)
        for f in c.decode(vs):
            t = float(f.pts * vs.time_base)
            if t < a.t_from:
                continue
            if t > t1 or n >= a.limit:
                break
            n += 1
            img = f.to_ndarray(format="bgr24")
            x, y, w, h = box or [0, 0, img.shape[1], img.shape[0]]
            g = cv2.cvtColor(img[y:y + h, x:x + w], cv2.COLOR_BGR2GRAY)
            if prev is None or (np.abs(g.astype(int) - prev) > 24).sum() >= 12:  # a few changed pixels are enough: one word
                read += 1
                texts = read_box(img, box, a.lang)
                words = [(tx, tx.split('" at [')[0].strip('"').lower()) for tx in texts]
                last_hit = [tx for tx, w in words if len(w) >= 0.6 * len(want) and fuzz.partial_ratio(want, w) >= a.match]
                prev = g.astype(int)
            if last_hit:
                if hits and hits[-1]["end_frame"] == n - 1:
                    hits[-1].update(end=t, end_frame=n, frames=hits[-1]["frames"] + 1)
                else:
                    hits.append({"start": t, "end": t, "frames": 1, "end_frame": n, "text": last_hit[0]})
    print(f"searched {n} frames from {a.t_from} s ({read} read, the rest unchanged)" + (f"; stopped at the limit of {a.limit} frames" if n >= a.limit else ""))
    for h in hits:
        print(f"{h['start']:.3f}-{h['end']:.3f} s, {h['frames']} frame{'s' if h['frames'] > 1 else ''}: {h['text']}")
    if not hits:
        print(f'"{a.text}" not found')


def cmd_report(a) -> None:
    import shutil

    import agent
    import run as parser

    video = Path(a.video).resolve()
    home, stem = video.parent, video.stem
    variant = None if stem in ("recording", "video") else stem
    ticket = Path(a.ticket).resolve() if a.ticket else None
    print(f"1/3 parsing {video.name} (minutes for a long video; cached on a second run)", flush=True)
    parser.run(home.name, None, set(), False, None, video, a.speech_lang, a.lang)
    work = home / (f"parsed-{variant}" if variant else "parsed")
    out = work / "agent"
    out.mkdir(exist_ok=True)
    try:
        for step, inp, tools in (("2/3 watcher: the frames", "frames", False), ("3/3 investigator: frames, timeline and vrp", "investigate", True)):
            print(step, flush=True)
            r = agent.run(home.name, variant, a.model, None, input_=inp, tools=tools, ticket=ticket is not None, home=home, ticket_file=ticket)
            name = agent.tag(a.model, None) + f"+{inp}" + ("+tools" if tools else "") + ("+ticket" if ticket else "")
            (out / f"{name}.json").write_text(json.dumps(r, ensure_ascii=False, indent=1), encoding="utf-8")
            (out / f"{name}.md").write_text(agent.to_md(video.name, r), encoding="utf-8")
    finally:
        for d in ("", "direct"):
            (work / d / "ticket.md").unlink(missing_ok=True)
    report = home / f"{video.name}.report.md"
    shutil.copyfile(out / f"{name}.md", report)
    print(f"report: {report}\nevidence: {work / 'timeline.html'} (timeline with frames), {work / 'agent'} (both passes)")


def main() -> None:
    ap = argparse.ArgumentParser(prog="vrp", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--work", type=Path, default=Path("."), help="the parsed folder (default: the current one)")
    ap.add_argument("--lang", default="en", help="language of the text on screen")
    sub = ap.add_subparsers(dest="cmd", required=True)
    rp = sub.add_parser("report")
    rp.add_argument("video")
    rp.add_argument("--ticket", help="the ticket as text or markdown")
    rp.add_argument("--model", default="claude-sonnet-5.5")
    rp.add_argument("--speech-lang", default="auto")
    e = sub.add_parser("events")
    e.add_argument("--near", type=float, required=True)
    e.add_argument("--window", type=float, default=2.0)
    lk = sub.add_parser("look")
    lk.add_argument("--from", dest="t_from", type=float, required=True)
    lk.add_argument("--to", dest="t_to", type=float, required=True)
    lk.add_argument("--box")
    lk.add_argument("--fps", default="native")
    lk.add_argument("--scale", type=float, default=1.0)
    d = sub.add_parser("diff")
    d.add_argument("--box", required=True)
    d.add_argument("--at", type=float, required=True)
    d.add_argument("--to", type=float, required=True)
    d.add_argument("--scale", type=float, default=2.0)
    o = sub.add_parser("ocr")
    o.add_argument("--at", type=float, required=True)
    o.add_argument("--box")
    fd = sub.add_parser("find")
    fd.add_argument("--text", required=True)
    fd.add_argument("--from", dest="t_from", type=float, default=0.0)
    fd.add_argument("--to", dest="t_to", type=float)
    fd.add_argument("--box")
    fd.add_argument("--match", type=int, default=80, help="fuzzy match, 0-100")
    fd.add_argument("--limit", type=int, default=3000, help="frames at most")
    a = ap.parse_args()
    if a.cmd == "report":
        return cmd_report(a)
    work = a.work.resolve()
    if not (work / "evidence.json").exists():
        sys.exit(f"{work}: not a parsed folder (no evidence.json); run vrp in parsed/ or pass --work")
    {"events": cmd_events, "look": cmd_look, "diff": cmd_diff, "ocr": cmd_ocr, "find": cmd_find}[a.cmd](work, a)


if __name__ == "__main__":
    main()
