"""Screen: a change scanner over every frame at low resolution -> stable states -> OCR of the key frame.

The cursor and the click ring are small blobs and are dropped by area. A state is a run of frames that do not change
for longer than MIN_STABLE frames; its key frame is saved at full resolution.
"""
from pathlib import Path

import cv2
import numpy as np
from ocrmac import ocrmac
from PIL import Image

SMALL_W = 480
DIFF = 18  # brightness threshold of the per-pixel difference
MIN_AREA = 140  # smaller blobs (in small-frame pixels) are the cursor, the click ring, compression noise
MIN_STABLE = 3  # frames without changes before the screen counts as stable


def scan(video: Path, frames_dir: Path) -> tuple[list[dict], dict]:
    cap = cv2.VideoCapture(str(video))
    fps = cap.get(cv2.CAP_PROP_FPS)
    W, H = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    n_total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    k = SMALL_W / W
    kernel = np.ones((3, 3), np.uint8)
    frames_dir.mkdir(parents=True, exist_ok=True)

    segs: list[dict] = []
    prev = None
    run_start = 0
    i = 0
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        g = cv2.cvtColor(cv2.resize(frame, (SMALL_W, round(H * k)), interpolation=cv2.INTER_AREA), cv2.COLOR_BGR2GRAY)
        changed = False
        if prev is not None:
            m = cv2.morphologyEx((cv2.absdiff(g, prev) > DIFF).astype(np.uint8), cv2.MORPH_OPEN, kernel)
            n, _, stats, _ = cv2.connectedComponentsWithStats(m)
            changed = any(stats[j, cv2.CC_STAT_AREA] >= MIN_AREA for j in range(1, n))
        if changed:
            if segs and segs[-1]["end"] is None:
                segs[-1]["end"] = i
            run_start = i
        elif i - run_start + 1 == MIN_STABLE:
            path = frames_dir / f"{i:06d}.jpg"
            cv2.imwrite(str(path), frame, [cv2.IMWRITE_JPEG_QUALITY, 92])
            segs.append({"start": run_start, "key": i, "end": None, "frame": str(path)})
        prev = g
        i += 1
    cap.release()
    if segs and segs[-1]["end"] is None:
        segs[-1]["end"] = i
    meta = {"width": W, "height": H, "fps": fps, "duration_ms": round(max(i, n_total) / fps * 1000)}
    return [{"start_ms": round(s["start"] / fps * 1000), "end_ms": round(s["end"] / fps * 1000), "frame": s["frame"]} for s in segs], meta


OCR_LANGS = {"en": ["en-US"], "ru": ["ru-RU", "en-US"]}


def ocr(path: str, lang: str) -> list[dict]:
    img = Image.open(path)
    W, H = img.size
    res = ocrmac.OCR(img, language_preference=OCR_LANGS[lang], recognition_level="accurate").recognize()
    out = []
    for text, conf, (x, y, w, h) in res:
        if conf < 0.3 or not text.strip():
            continue
        out.append({"bbox": [round(x * W), round((1 - y - h) * H), round(w * W), round(h * H)], "text": text.strip()})
    return out
