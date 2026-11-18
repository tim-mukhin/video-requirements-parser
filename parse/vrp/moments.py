"""Moments: for the short, decisive events, a strip of every frame around them, cropped and enlarged.

A model reading the timeline sees "MOVED 14 px right in one frame" or "FLASHED for 0.2 s" but has to guess what it
looked like; the key frames of the screen states usually miss it. Here every such event gets one image: the frames from
just before to just after, at the video's own rate, around the event's box, with times written on them.
frames/moments/<event id>.jpg, referenced from the timeline line of the event.
"""
from pathlib import Path

import av
import cv2
import numpy as np

MAX_MOMENTS = 30
MAX_FRAMES = 8
BEFORE_S, AFTER_S = 0.15, 0.25
KINDS = ("transient", "move", "flicker", "drag", "scroll")


def wanted(e: dict) -> float | None:
    """Rank of an event as a moment worth a strip (lower first), or None."""
    span = ((e.get("end_ms") or e["t_ms"]) - e["t_ms"]) / 1000
    if e["kind"] == "appear" and e.get("end_ms") and span < 1.0:
        return span  # flashed: the shorter, the easier to miss
    if e["kind"] == "transient":
        return 0.5
    if e["kind"] in KINDS:
        return 1.0 + min(span, 5) / 10
    if e["kind"] == "visual_change" and (e.get("look") or {}).get("kept", 1) < 0.3:
        return 1.5  # what was drawn there is gone
    if e["kind"] == "point" and e.get("reaction"):
        return 1.6
    return None


def strip(video: Path, t0: float, t1: float, box: list[int] | None, W: int, H: int) -> np.ndarray | None:
    got, prev = [], None
    with av.open(str(video)) as c:
        vs = c.streams.video[0]
        c.seek(int(max(0.0, t0 - 1.0) / vs.time_base), stream=vs, backward=True)
        for f in c.decode(vs):
            t = float(f.pts * vs.time_base)
            if t < t0:
                prev = (t, f)
                continue
            if t > t1:
                break
            got.append((t, f))
    if prev and (not got or got[0][0] > t0):
        got.insert(0, prev)
    if not got:
        return None
    if len(got) > MAX_FRAMES:
        got = [got[round(i * (len(got) - 1) / (MAX_FRAMES - 1))] for i in range(MAX_FRAMES)]
    x, y, w, h = box or [0, 0, W, H]
    side = max(w, h, 120)
    cx, cy = x + w / 2, y + h / 2
    x0, y0 = int(max(0, cx - side * 0.8)), int(max(0, cy - side * 0.8))
    x1, y1 = int(min(W, cx + side * 0.8)), int(min(H, cy + side * 0.8))
    k = min(3.0, 260 / max(1, y1 - y0))
    tiles = []
    for t, f in got:
        img = f.to_ndarray(format="bgr24")[y0:y1, x0:x1]
        if k != 1:
            img = cv2.resize(img, None, fx=k, fy=k, interpolation=cv2.INTER_NEAREST if k > 1 else cv2.INTER_AREA)
        cv2.rectangle(img, (0, 0), (74, 16), (0, 0, 0), -1)
        cv2.putText(img, f"{t:.3f} s", (3, 12), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_AA)
        tiles.append(cv2.copyMakeBorder(img, 0, 0, 0, 3, cv2.BORDER_CONSTANT, value=(255, 255, 255)))
    return np.hstack(tiles)


def build(video: Path, evidence: dict, work: Path) -> dict[str, str]:
    """{event id: frames/moments/<id>.jpg} for the most decisive short events."""
    out = work / "frames" / "moments"
    out.mkdir(parents=True, exist_ok=True)
    for f in out.glob("*.jpg"):
        f.unlink()
    W, H = evidence["video"]["width"], evidence["video"]["height"]
    ranked = sorted(((r, e["t_ms"], i, e) for i, e in enumerate(evidence["events"]) if (r := wanted(e)) is not None))[:MAX_MOMENTS]
    made = {}
    for _, _, _, e in ranked:
        t0 = e["t_ms"] / 1000 - BEFORE_S
        t1 = (e.get("end_ms") or e["t_ms"]) / 1000 + AFTER_S
        img = strip(video, max(0.0, t0), min(t1, t0 + 2.0), e.get("bbox"), W, H)
        if img is None:
            continue
        p = out / f"{e['id']}.jpg"
        cv2.imwrite(str(p), img, [cv2.IMWRITE_JPEG_QUALITY, 88])
        made[e["id"]] = p.relative_to(work).as_posix()
    return made
