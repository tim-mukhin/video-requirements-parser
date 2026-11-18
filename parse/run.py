"""Video parser: every pass writes its own file, deterministic code assembles them into evidence.json, timeline.md and timeline.html.

python run.py [--video file.mp4 --speech-lang ru|auto --screen-lang en] [--variant low] [--tag name] [--ocr rapidocr|vision] [--asr mlx|faster-whisper] [--force speech,screens,events] [--no-speech] [<lang>/<id> ...]

out/<lang>/<id>/parsed[-variant][-tag]/
  run.json          video hash, pass versions, timings
  10-speech.json    utterances and word timings
  30-screens.json   stable screen states: time, key frame, OCR text
  50-motion.json    what moved between neighbouring frames, what went back to how it looked a moment ago
  60-events.json    what appeared, disappeared, changed
  70-links.json     what a phrase refers to on the screen
  80-speakers.json  meeting tiles and who spoke: the lit tile during each utterance
  85-voices.json    who speaks when as voice ids (diarization), the voice of each utterance
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
from vrp import moments as moments_pass
from vrp import motion as motion_pass
from vrp import ocr as ocr_engine
from vrp import slides as slides_pass
from vrp import speakers as speakers_pass
from vrp import screen as screen_pass
from vrp import speech as speech_pass
from vrp import voices as voices_pass
from vrp.format import SCHEMA
from vrp.timeline import crops, render_html, render_md

OUT = Path(__file__).resolve().parents[1] / "out"
FILES = {"speech": "10-speech.json", "screens": "30-screens.json", "motion": "50-motion.json", "events": "60-events.json", "links": "70-links.json", "speakers": "80-speakers.json", "voices": "85-voices.json", "slides": "90-slides.json", "checks": "95-checks.json"}
VERSIONS = {"speech": 2, "screens": 11, "motion": 2, "events": 33, "links": 4, "speakers": 2, "voices": 2, "slides": 2, "checks": 5}


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()[:16]


def steady(video: Path, work: Path) -> Path:
    """The video the frame passes read: as is, or re-timed to a steady 30 fps (60 when the video has more than 32 frames
    a second, so a frame shown for 25 ms is not skipped) when frame number / fps is not the time
    (variable frame rate screen recorders: GNOME writes webm that claims 1000 fps and phones drop frames)."""
    import av
    import cv2
    cap = cv2.VideoCapture(str(video))
    fps, n = cap.get(cv2.CAP_PROP_FPS), cap.get(cv2.CAP_PROP_FRAME_COUNT)
    cap.release()
    with av.open(str(video)) as c:
        dur = float(c.duration or 0) / 1e6
        vs = c.streams.video[0]
        pts = sorted(float(p.pts * vs.time_base) for p in c.demux(vs) if p.pts is not None)
    # the frame passes take frame i to be at i / fps: fine only if the real frame times keep to that grid (phones and
    # screen recorders write frames unevenly while the average rate looks right - off by seconds in a minute)
    drift = max((abs(t - pts[0] - k / fps) for k, t in enumerate(pts)), default=0.0) if 0 < fps <= 240 else 1e9
    if 0 < fps <= 240 and n > 0 and abs(n / fps - dur) <= max(0.1, 0.02 * dur) and drift <= 0.1:
        return video
    out = work / "steady.mp4"
    if out.exists() and out.stat().st_mtime >= video.stat().st_mtime:
        return out
    tmp = out.with_suffix(".part.mp4")
    with av.open(str(video)) as src, av.open(str(tmp), "w") as dst:
        vs = src.streams.video[0]
        rate = 60 if len(pts) > 32 * max(dur, 1e-3) else 30
        enc = dst.add_stream("libx264", rate=rate, options={"crf": "12", "preset": "fast"})
        enc.width, enc.height, enc.pix_fmt = vs.codec_context.width // 2 * 2, vs.codec_context.height // 2 * 2, "yuv420p"
        k, last = 0, None

        def put(arr):
            nonlocal k
            f = av.VideoFrame.from_ndarray(arr, format="rgb24")
            dst.mux(enc.encode(f))
            k += 1

        for fr in src.decode(vs):
            t = float(fr.pts * vs.time_base) if fr.pts is not None else k / rate
            while last is not None and k / rate < t:
                put(last)
            last = fr.to_ndarray(width=enc.width, height=enc.height, format="rgb24")
        while last is not None and k / rate < dur:
            put(last)
        dst.mux(enc.encode())
    tmp.replace(out)
    return out


def input_facts(track: list[list], events: list[dict], duration_ms: int, touch: str | None) -> dict:
    """How much of what the user did the video lets us see: cursor coverage, the stretches it was lost, touch marks."""
    seen, lost, t_prev, x_prev = 0, [], 0, None
    for p in [*track, [duration_ms, None, None]]:
        if x_prev is not None:
            seen += p[0] - t_prev
        elif track and p[0] - t_prev >= 1000:
            lost.append([t_prev, p[0]])
        t_prev, x_prev = p[0], p[1]
    return {"cursor_share": round(seen / max(1, duration_ms), 2) if track else 0.0, "cursor_lost": lost, "touch_screen": touch,
            "touch": sum(1 for e in events if e.get("source") == "touch"), "typed": sum(1 for e in events if e["kind"] == "type")}


def dump(path: Path, data) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")


def run(key: str, variant: str | None, force: set[str], no_speech: bool = False, tag: str | None = None,
        file: Path | None = None, speech_lang: str | None = None, screen_lang: str | None = None) -> dict:
    """key = <lang>/<id> of a generated scenario, or file = any video: results go next to it, languages given apart
    (speech_lang "auto" lets Whisper detect the language of every segment, for speech that mixes languages)."""
    if file:
        video, home = file, file.parent
        key = home.name
    else:
        video = OUT / (f"{key}.{variant}.mp4" if variant else f"{key}.mp4")
        home = OUT / key
    lang = screen_lang or key.split("/")[0]  # text on the screen
    said = speech_lang or key.split("/")[0]  # speech; word lists of links and checks follow it
    words_lang = "en" if said == "auto" else said
    # several recordings in one folder: recording-2.mp4 -> parsed-recording-2
    own = file.stem if file and file.stem not in ("recording", "video") else None
    work = home / "-".join(["parsed", *filter(None, (own, variant, tag))])
    work.mkdir(parents=True, exist_ok=True)
    rj = work / "run.json"
    prev = json.loads(rj.read_text(encoding="utf-8")).get("passes", {}) if rj.exists() else {}
    vhash = sha(video)
    passes, timing = {}, {}

    def step(name: str, upstream: str, compute):
        key = f"{vhash}:{VERSIONS[name]}:{upstream}"
        passes[name] = {"version": VERSIONS[name], "key": key}
        path = work / FILES[name]
        t0 = time.time()
        if name not in force and prev.get(name, {}).get("key") == key and path.exists():
            data = json.loads(path.read_text(encoding="utf-8"))
        else:
            data = compute()
            dump(path, data)
        timing[name] = round(time.time() - t0, 1)
        return data

    ocr0 = ocr_engine.spent

    def screens():
        for f in (work / "frames").glob("*.jpg"):
            f.unlink()
        segs, meta, track = screen_pass.scan(steady(video, work), work / "frames")
        region = meta["regions"]["screen"]
        ev_pass.setup(work, meta, track)
        texts = screen_pass.ocr_all([s["frame"] for s in segs], lang, region)
        raw = [
            {"id": f"s{i + 1:03d}", "start_ms": s["start_ms"], "end_ms": s["end_ms"], "frame": Path(s["frame"]).relative_to(work).as_posix(), "texts": tx}
            for i, (s, tx) in enumerate(zip(segs, texts))
        ]
        return {"meta": meta, "raw": len(raw), "screens": ev_pass.merge_same(raw), "cursor": track}

    # --no-speech: screen passes only (a heavy model may be busy with other work); the speech pass is left as it was
    cached = work / FILES["speech"]
    sp = (json.loads(cached.read_text(encoding="utf-8")) if cached.exists() else {"speakers": [], "utterances": []}) if no_speech else step("speech", f"{speech_pass.ENGINE}|{said}", lambda: speech_pass.transcribe(video, work, None if said == "auto" else said))
    if no_speech and prev.get("speech"):
        passes["speech"] = prev["speech"]
    sc = step("screens", ocr_engine.ENGINE, screens)
    meta = sc["meta"]

    mo = step("motion", passes["screens"]["key"], lambda: motion_pass.scan(steady(video, work), meta["regions"]["screen"], sc["cursor"], meta.get("cursor_scale"), work / "frames" / "transients"))

    def events():
        ev_pass.setup(work, meta, sc["cursor"])
        screen_events = ev_pass.diff(sc["screens"])
        cursor_events = ev_pass.cursor_events(sc["cursor"], meta.get("cursor_scale"), sc["screens"], screen_events, meta["duration_ms"])
        ev_pass.hover_looks(cursor_events, screen_events)
        screen_events = ev_pass.drop_under_hover([e for e in screen_events if not e.get("under_cursor")], cursor_events, sc["cursor"])
        flickers = ev_pass.flicker_events(mo, sc["screens"])
        screen_events = ev_pass.jumps(ev_pass.drop_flickering(screen_events, flickers))
        motion_events = ev_pass.motion_events(mo, sc["screens"], screen_events) + ev_pass.transient_events(mo, lang)
        out = sorted(screen_events + cursor_events + motion_events + flickers, key=lambda e: (e["t_ms"], e["kind"]))
        for i, e in enumerate(out):
            e["id"] = f"p{i + 1:03d}"
        return out

    events = step("events", passes["motion"]["key"], events)

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
        "input": input_facts(sc["cursor"], events, meta["duration_ms"], ev_pass.touch_screen(sc["screens"], meta["regions"]["screen"], meta.get("cursor_scale"))),
    }
    if not no_speech:
        who = step("speakers", passes["speech"]["key"] + "|" + ocr_engine.ENGINE, lambda: speakers_pass.assign(steady(video, work), sp["utterances"], lang))

        vo = step("voices", passes["speech"]["key"] + "|" + voices_pass.ENGINE, lambda: voices_pass.diarize(video, sp["utterances"]))
        voices_pass.facts(evidence, vo["utterances"], {k: a["tile"] for k, a in who["utterances"].items()})
    attached = sorted((home / "attachments").glob("*.p*")) if (home / "attachments").exists() else []

    def slides():
        shown, words = slides_pass.shown(sc["screens"])
        return {"shown": shown, "attachments": slides_pass.compare(attached, words)}

    sl = step("slides", passes["screens"]["key"] + "|" + ",".join(f.name for f in attached), slides)
    evidence["slides"], evidence["attachments"] = sl["shown"], sl["attachments"]
    evidence["links"] = step("links", f'{passes.get("speech", {}).get("key")}|{passes["events"]["key"]}', lambda: links_pass.build(evidence, words_lang))
    evidence["checks"] = step("checks", f'{passes.get("speech", {}).get("key")}|{passes["events"]["key"]}|{no_speech}', lambda: checks_pass.build(evidence, work, words_lang, speech=not no_speech))
    crops(evidence, work)
    made = moments_pass.build(video, evidence, work)
    for e in evidence["events"]:
        if e["id"] in made:
            e["moment"] = made[e["id"]]
    dump(work / "evidence.json", evidence)
    title = " · ".join([key, *filter(None, (variant, tag))])
    (work / "timeline.md").write_text(render_md(evidence, title), encoding="utf-8")
    (work / "timeline.html").write_text(render_html(evidence, title, video_src=f"../{video.name}" if file else f"../../{video.name}"), encoding="utf-8")
    timing["ocr"] = round(ocr_engine.spent - ocr0, 1)
    dump(rj, {"video": video.name, "video_sha": vhash, "passes": passes, "timing_sec": timing})
    return evidence


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("ids", nargs="*")
    ap.add_argument("--variant")
    ap.add_argument("--force", default="", help="comma-separated passes to recompute")
    ap.add_argument("--no-speech", action="store_true", help="skip the speech pass")
    ap.add_argument("--tag", help="write to parsed[-variant]-<tag>, e.g. to compare engines")
    ap.add_argument("--ocr", choices=["rapidocr", "vision"], help="text engine (default: VRP_OCR or rapidocr)")
    ap.add_argument("--video", type=Path, help="parse any video file instead of generated scenarios; results next to it")
    ap.add_argument("--speech-lang", help="language of the speech: en, ru, ... or auto (detected per segment)")
    ap.add_argument("--screen-lang", help="language of the text on the screen")
    ap.add_argument("--asr", choices=["mlx", "faster-whisper"], help="speech engine (default: VRP_ASR, mlx on Apple Silicon, else faster-whisper)")
    a = ap.parse_args()
    if a.ocr:
        ocr_engine.use(a.ocr)
    if a.asr:
        speech_pass.ENGINE = a.asr
    if a.video:
        ev = run(a.video.parent.name, None, set(filter(None, a.force.split(","))), a.no_speech, a.tag, a.video.resolve(), a.speech_lang or "auto", a.screen_lang or "en")
        print(f"{a.video}: states {len(ev['screens'])}, events {len(ev['events'])}, utterances {len(ev['speech']['utterances'])}", flush=True)
        raise SystemExit
    keys = a.ids or sorted(f"{p.parts[-4]}/{p.parts[-3]}" for p in OUT.glob("*/*/truth/evidence.json"))
    for key in keys:
        ev = run(key, a.variant, set(filter(None, a.force.split(","))), a.no_speech, a.tag)
        print(f"{key}: states {len(ev['screens'])}, events {len(ev['events'])}, utterances {len(ev['speech']['utterances'])}", flush=True)
