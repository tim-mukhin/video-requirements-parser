"""Regions of a meeting recording: where the shared screen is and where the people are.

The meeting window around the shared screen is dark and does not change; participant tiles sit on that dark background.
Pixels that are dark in every sample frame are the window; the shared screen is the box of the largest connected area
that is not. When that box covers almost the whole frame, or a light strip outside it runs along the frame edge (a desktop menu bar
above a meeting app), the video is a plain screen recording and the whole frame is the screen.
"""
import cv2
import numpy as np

DARK = 45
STEP = 4  # work at a quarter size


def detect(samples: list[np.ndarray]) -> dict:
    """samples - gray full-size frames; -> {"screen": [x, y, w, h], "people": [x, y, w, h] | None}"""
    H, W = samples[0].shape[:2]
    s = np.stack([cv2.resize(g, (W // STEP, H // STEP), interpolation=cv2.INTER_AREA) for g in samples])
    chrome = (s.max(0) < DARK) & (s.max(0).astype(int) - s.min(0) < 12)
    content = cv2.morphologyEx((~chrome).astype(np.uint8), cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    n, _, st, _ = cv2.connectedComponentsWithStats(content)
    if n < 2:
        return {"screen": [0, 0, W, H], "people": None}
    j = 1 + int(np.argmax(st[1:, 4]))
    x, y, w, h = (int(v) * STEP for v in st[j, :4])
    x, y, w, h = max(0, x), max(0, y), min(W - x, w), min(H - y, h)
    if w * h >= 0.9 * W * H:
        return {"screen": [0, 0, W, H], "people": None}
    rest = (~chrome).copy()
    rest[y // STEP:(y + h) // STEP, x // STEP:(x + w) // STEP] = False
    # a wide light strip at the frame edge (a desktop menu bar) means a meeting app on a desktop, not a recording
    m, _, rst, _ = cv2.connectedComponentsWithStats(rest.astype(np.uint8))
    hw, hh = W // STEP, H // STEP
    for x0, y0, cw, ch, _ in rst[1:m]:
        if (cw >= 0.5 * hw and (y0 == 0 or y0 + ch >= hh)) or (ch >= 0.5 * hh and (x0 == 0 or x0 + cw >= hw)):
            return {"screen": [0, 0, W, H], "people": None}
    ys, xs = np.nonzero(rest)
    people = [int(xs.min()) * STEP, int(ys.min()) * STEP, int(xs.max() - xs.min() + 1) * STEP, int(ys.max() - ys.min() + 1) * STEP] if len(xs) else None
    return {"screen": [x, y, w, h], "people": people}
