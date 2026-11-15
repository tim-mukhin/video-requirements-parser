"""Screen: a change scanner over every frame at half resolution -> stable states -> OCR of the key frame.

The mouse cursor is found and followed (vrp/cursor.py); its area is left out of the comparison, so the scanner can
react to small changes - a status "Sending…" turning into a check mark - without every cursor move splitting the
state. A state is a run of frames that do not change for MIN_STABLE frames; its key frame is saved at full resolution.
Each frame is also compared with the key frame of the current state: a change that happened under the cursor shows up
as soon as the cursor leaves.
"""
from pathlib import Path

import cv2
import numpy as np
from ocrmac import ocrmac
from PIL import Image

from . import cursor as cur
from . import regions

SMALL_W = 960
DIFF = 18  # brightness threshold of the per-pixel difference
MIN_AREA = 25  # changed px of the half-size frame; fewer is compression noise
MIN_STABLE = 3  # frames without changes before the screen counts as stable
GLOBAL_EVERY = 90  # frames between full-frame cursor searches while it is lost
KERNEL = np.ones((3, 3), np.uint8)


def blobs(mask: np.ndarray) -> np.ndarray:
    """Changed areas: neighbouring pixels are joined by dilation (letters of one word), the area counts changed pixels only,
    since at half size a text stroke is one pixel wide."""
    n, labels, stats, _ = cv2.connectedComponentsWithStats(cv2.dilate(mask.astype(np.uint8), KERNEL))
    stats[:, 4] = np.bincount(labels[mask], minlength=n)
    return stats[1:n]


def cut(mask: np.ndarray, boxes, k: float, ox: int, oy: int) -> np.ndarray:
    """Leaves out boxes given in full-frame pixels from a mask of the scaled screen region at (ox, oy)."""
    for b in boxes:
        if b:
            x0, y0, x1, y1 = (max(0, round((v - o) * k)) for v, o in zip(b, (ox, oy, ox, oy)))
            mask[y0:y1, x0:x1] = False
    return mask


def scan(video: Path, frames_dir: Path) -> tuple[list[dict], dict, list[list]]:
    cap = cv2.VideoCapture(str(video))
    fps = cap.get(cv2.CAP_PROP_FPS)
    W, H = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    n_total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frames_dir.mkdir(parents=True, exist_ok=True)

    samples = []
    for f in np.linspace(0, n_total - 1, 8)[1:-1].astype(int):
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(f))
        ok, frame = cap.read()
        if ok:
            samples.append(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    reg = regions.detect(samples)
    sx, sy, sw, sh = reg["screen"]
    k = SMALL_W / max(sw, sh)
    size = (round(sw * k), round(sh * k))
    cal = cur.calibrate(samples)
    tracker = cur.Tracker(cal[0], cal[1], min(W, H)) if cal else None

    segs: list[dict] = []
    track: list[list] = []  # [t_ms, x, y] when the cursor position changes; x, y = None - not found
    prev = key_g = None
    prev_box = key_box = None
    run_start = 0
    i = 0
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        g = cv2.cvtColor(cv2.resize(frame[sy:sy + sh, sx:sx + sw], size, interpolation=cv2.INTER_AREA), cv2.COLOR_BGR2GRAY)
        raw = cv2.absdiff(g, prev) > DIFF if prev is not None else np.zeros_like(g, bool)
        box = None
        if tracker:
            st = blobs(raw)
            moved = [(sx + round(x / k), sy + round(y / k), sx + round((x + w) / k), sy + round((y + h) / k)) for x, y, w, h, a in sorted(st.tolist(), key=lambda s: -s[4])[:12]]
            pos = tracker.update(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), moved, force_global=i % GLOBAL_EVERY == 0)
            box = tracker.box(pos)
            t = round(i / fps * 1000)
            if not track or (track[-1][1], track[-1][2]) != (pos or (None, None)):
                track.append([t, *(pos or (None, None))])
        changed = False
        if prev is not None:
            changed = any(a >= MIN_AREA for a in blobs(cut(raw, (box, prev_box), k, sx, sy))[:, 4])
            if not changed and key_g is not None:
                changed = any(a >= MIN_AREA for a in blobs(cut(cv2.absdiff(g, key_g) > DIFF, (box, key_box), k, sx, sy))[:, 4])
        if changed:
            if segs and segs[-1]["end"] is None:
                segs[-1]["end"] = i
            run_start, key_g = i, None
        elif i - run_start + 1 == MIN_STABLE:
            path = frames_dir / f"{i:06d}.jpg"
            cv2.imwrite(str(path), frame, [cv2.IMWRITE_JPEG_QUALITY, 92])
            segs.append({"start": run_start, "key": i, "end": None, "frame": str(path)})
            key_g, key_box = g, box
        prev, prev_box = g, box
        i += 1
    cap.release()
    if segs and segs[-1]["end"] is None:
        segs[-1]["end"] = i
    meta = {"width": W, "height": H, "fps": fps, "duration_ms": round(max(i, n_total) / fps * 1000), "cursor_scale": cal and round(cal[0], 3), "regions": reg}
    states = [{"start_ms": round(s["start"] / fps * 1000), "end_ms": round(s["end"] / fps * 1000), "frame": s["frame"]} for s in segs]
    return states, meta, track


OCR_LANGS = {"en": ["en-US"], "ru": ["ru-RU", "en-US"]}
OCR_MIN_SIDE = 1080


OVERLAP = 120  # px shared by the two halves


def _read(img: Image.Image, lang: str) -> list[tuple[str, list[float]]]:
    """Apple Vision on one image -> (text, [x, y, w, h] in its pixels)."""
    W, H = img.size
    res = ocrmac.OCR(img, language_preference=OCR_LANGS[lang], recognition_level="accurate").recognize()
    return [(t.strip(), [x * W, (1 - y - h) * H, w * W, h * H]) for t, c, (x, y, w, h) in res if c >= 0.3 and t.strip()]


def ocr(path: str, lang: str, region: list[int]) -> list[dict]:
    """Text of the screen region of a key frame; boxes in full-frame pixels.

    Vision reads the whole region well but may drop whole columns of a wide, sparse screen (a file list with Owner,
    Modified, Size). So the region is also read in two overlapping halves along its long side; when they find clearly
    more, their texts are added where the whole-region pass found nothing - a line is never stitched from cut pieces."""
    rx, ry, rw, rh = region
    img = Image.open(path).crop((rx, ry, rx + rw, ry + rh))
    f = 1.0
    if min(rw, rh) < OCR_MIN_SIDE:  # small text of a low-resolution video reads better enlarged
        f = OCR_MIN_SIDE / min(rw, rh)
        img = img.resize((round(rw * f), round(rh * f)), Image.LANCZOS)
    W, H = img.size
    base = [{"text": t, "b": b} for t, b in _read(img, lang)]
    wide = W >= H
    half = (W if wide else H) // 2
    extra: list[dict] = []
    found = 0
    for lo, hi in ((0, half + OVERLAP), (half - OVERLAP, W if wide else H)):
        box = (lo, 0, hi, H) if wide else (0, lo, W, hi)
        for t, (x, y, w, h) in _read(img.crop(box), lang):
            found += 1
            b = [x + box[0], y + box[1], w, h]
            if not any(_overlap(b, o["b"]) > 0.2 for o in base + extra):
                extra.append({"text": t, "b": b})
    # the halves are trusted only when the whole-region pass clearly lost something (columns of a sparse list);
    # otherwise what they add is mostly icons read as letters and lines cut by something on top
    if found < 1.3 * len(base) + 3:
        extra = []
    return [{"bbox": [rx + round(b[0] / f), ry + round(b[1] / f), round(b[2] / f), round(b[3] / f)], "text": t["text"]} for t in base + extra for b in [t["b"]]]


def _overlap(a: list[float], b: list[float]) -> float:
    """Share of the smaller box covered by the other."""
    ix = max(0, min(a[0] + a[2], b[0] + b[2]) - max(a[0], b[0]))
    iy = max(0, min(a[1] + a[3], b[1] + b[3]) - max(a[1], b[1]))
    return ix * iy / max(1.0, min(a[2] * a[3], b[2] * b[3]))
