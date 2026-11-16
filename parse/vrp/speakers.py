"""Speakers of a meeting: the tile of the person speaking is outlined (a green frame in Teams-like apps). The frame is
followed over the video, each tile's caption is read once, and every utterance gets the tile lit for most of it.

A room tile (several people at one camera) gives the room, not the person; telling them apart is the voices pass.
No lit tiles - a plain screen recording.
"""
import re
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

from . import ocr as engine

SAMPLE_FPS = 5


def lit_tiles(frame: np.ndarray) -> list[list[int]]:
    """Green outlines the size of a video tile."""
    H, W = frame.shape[:2]
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    m = ((hsv[..., 0] >= 45) & (hsv[..., 0] <= 85) & (hsv[..., 1] > 120) & (hsv[..., 2] > 120)).astype(np.uint8)
    n, _, st, _ = cv2.connectedComponentsWithStats(m)
    out = []
    for x, y, w, h, a in st[1:n]:
        if w < 0.05 * W or h < 0.05 * H or w > 0.6 * W or h > 0.6 * H:
            continue
        if a > 0.25 * w * h:  # filled, not an outline (a green bar on a slide)
            continue
        if a < 1.2 * (w + h):  # not a closed frame
            continue
        out.append([int(x), int(y), int(w), int(h)])
    return out


def iou(a, b) -> float:
    ix = max(0, min(a[0] + a[2], b[0] + b[2]) - max(a[0], b[0]))
    iy = max(0, min(a[1] + a[3], b[1] + b[3]) - max(a[1], b[1]))
    inter = ix * iy
    return inter / (a[2] * a[3] + b[2] * b[3] - inter) if inter else 0.0


def caption(frame: np.ndarray, box: list[int], lang: str) -> str | None:
    """The name written on a tile: the lowest text in it, read from an enlarged crop."""
    x, y, w, h = box
    crop = cv2.cvtColor(frame[y:y + h, x:x + w], cv2.COLOR_BGR2RGB)
    img = Image.fromarray(crop).resize((w * 3, h * 3), Image.LANCZOS)
    texts = [(t, b) for t, b in engine.read(img, lang) if re.search(r"\w{2,}", t)]
    if not texts:
        return None
    t, _ = max(texts, key=lambda tb: tb[1][1] + tb[1][3])
    return re.sub(r"^[^\w]+", "", t).strip() or None


def track(video: Path) -> tuple[list[dict], list[tuple[float, list[int]]], dict[int, np.ndarray]]:
    """-> tiles [{id, box}], samples [(t_ms, [tile ids lit])], one frame per tile to read its caption from."""
    cap = cv2.VideoCapture(str(video))
    fps = cap.get(cv2.CAP_PROP_FPS)
    step = max(1, round(fps / SAMPLE_FPS))
    tiles: list[dict] = []
    frames: dict[int, np.ndarray] = {}
    samples = []
    i = 0
    while True:
        ok = cap.grab()
        if not ok:
            break
        if i % step == 0:
            _, frame = cap.retrieve()
            ids = []
            for box in lit_tiles(frame):
                t = next((t for t in tiles if iou(t["box"], box) > 0.6), None)
                if t is None:
                    t = {"id": len(tiles), "box": box}
                    tiles.append(t)
                    frames[t["id"]] = frame.copy()
                ids.append(t["id"])
            samples.append((i / fps * 1000, ids))
        i += 1
    cap.release()
    return tiles, samples, frames


def assign(video: Path, utterances: list[dict], lang: str) -> dict:
    tiles, samples, frames = track(video)
    for t in tiles:
        t["name"] = caption(frames[t["id"]], t["box"], lang)
    out = {"tiles": [{"box": t["box"], "name": t["name"]} for t in tiles], "utterances": {}}
    if not tiles:
        return out
    for u in utterances:
        votes: dict[int, int] = {}
        for t_ms, ids in samples:
            if u["start_ms"] <= t_ms <= u["end_ms"]:
                for k in ids:
                    votes[k] = votes.get(k, 0) + 1
        if not votes:
            continue
        k = max(votes, key=votes.get)
        out["utterances"][u["id"]] = {"tile": tiles[k]["name"] or f"Tile{k + 1}"}
    return out
