"""Video parser: every pass writes its own file, deterministic code assembles them into evidence.json, timeline.md and timeline.html.

python run.py [--variant low] [--force speech,screens,events] [<lang>/<id> ...]

out/<lang>/<id>/parsed[-variant]/
  run.json          video hash, pass versions, timings
  10-speech.json    utterances and word timings
  30-screens.json   stable screen states: time, key frame, OCR text
  60-events.json    what appeared, disappeared, changed
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

from vrp import events as ev_pass
from vrp import screen as screen_pass
from vrp.format import SCHEMA
from vrp.timeline import crops, render_html, render_md

OUT = Path(__file__).resolve().parents[1] / "out"
FILES = {"speech": "10-speech.json", "screens": "30-screens.json", "events": "60-events.json"}
VERSIONS = {"speech": 2, "screens": 1, "events": 2}


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()[:16]


def dump(path: Path, data) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=1))


def run(key: str, variant: str | None, force: set[str]) -> dict:
    lang = key.split("/")[0]
    video = OUT / (f"{key}.{variant}.mp4" if variant else f"{key}.mp4")
    work = OUT / key / (f"parsed-{variant}" if variant else "parsed")
    work.mkdir(parents=True, exist_ok=True)
    rj = work / "run.json"
    prev = json.loads(rj.read_text()).get("passes", {}) if rj.exists() else {}
    vhash = sha(video)
    passes, timing = {}, {}

    def step(name: str, upstream: str, compute):
        key = f"{vhash}:{VERSIONS[name]}:{upstream}"
        passes[name] = {"version": VERSIONS[name], "key": key}
        path = work / FILES[name]
        t0 = time.time()
        if name not in force and prev.get(name, {}).get("key") == key and path.exists():
            data = json.loads(path.read_text())
        else:
            data = compute()
            dump(path, data)
        timing[name] = round(time.time() - t0, 1)
        return data

    def speech():
        from vrp.speech import transcribe

        return transcribe(video, work, lang)

    def screens():
        for f in (work / "frames").glob("*.jpg"):
            f.unlink()
        segs, meta = screen_pass.scan(video, work / "frames")
        raw = [
            {"id": f"s{i + 1:03d}", "start_ms": s["start_ms"], "end_ms": s["end_ms"], "frame": str(Path(s["frame"]).relative_to(work)), "texts": screen_pass.ocr(s["frame"], lang)}
            for i, s in enumerate(segs)
        ]
        return {"meta": meta, "raw": len(raw), "screens": ev_pass.merge_same(raw)}

    sp = step("speech", "", speech)
    sc = step("screens", "", screens)
    events = step("events", passes["screens"]["key"], lambda: ev_pass.diff(sc["screens"]))

    meta = sc["meta"]
    evidence = {
        "schema": SCHEMA,
        "video": {"file": video.name, **meta},
        "regions": [{"id": "screen", "bbox": [0, 0, meta["width"], meta["height"]]}],
        "speech": sp,
        "screens": sc["screens"],
        "events": events,
        "links": [],
        "slides": [],
        "findings": {},
    }
    crops(evidence, work)
    dump(work / "evidence.json", evidence)
    title = f"{key}{' · ' + variant if variant else ''}"
    (work / "timeline.md").write_text(render_md(evidence, title))
    (work / "timeline.html").write_text(render_html(evidence, title, video_src=f"../../{video.name}"))
    dump(rj, {"video": video.name, "video_sha": vhash, "passes": passes, "timing_sec": timing})
    return evidence


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("ids", nargs="*")
    ap.add_argument("--variant")
    ap.add_argument("--force", default="", help="comma-separated passes to recompute")
    a = ap.parse_args()
    keys = a.ids or sorted(f"{p.parts[-4]}/{p.parts[-3]}" for p in OUT.glob("*/*/truth/evidence.json"))
    for key in keys:
        ev = run(key, a.variant, set(filter(None, a.force.split(","))))
        print(f"{key}: states {len(ev['screens'])}, events {len(ev['events'])}, utterances {len(ev['speech']['utterances'])}", flush=True)
