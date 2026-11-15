"""Mouse cursor: find the arrow by template, then follow it near its last position and in places where the frame moved.

The template is the usual arrow (white with a black outline, or inverted as on macOS). The scale is found once from a few
frames; a video with no arrow match (a phone recording) has no cursor. Matching is normalised correlation inside the
arrow mask, so it does not depend on the background brightness.
"""
import cv2
import numpy as np

POLY = np.array([(3, 2), (3, 24), (9, 18.5), (13, 27), (17, 25), (13, 17), (21, 17)], float)
SCALES = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.25]  # of a 1080p frame
MIN_SCORE = 0.8
CAL_SCORE = 0.86  # to accept that a video has a cursor at all (an arrow-like icon on a phone scores ~0.84)
MIN_PX_SCALE = 0.35  # a smaller template (under ~8 px) matches anything
NEAR = 160  # search radius around the last position, px of a 1080p frame


def template(scale: float, invert: bool) -> tuple[np.ndarray, np.ndarray]:
    ss = 4
    w, h = int(np.ceil(22 * scale)) + 3, int(np.ceil(28 * scale)) + 3
    pts = ((POLY - (3, 2)) * scale * ss + ss).astype(np.int32)
    fill, mask = np.zeros((h * ss, w * ss), np.uint8), np.zeros((h * ss, w * ss), np.uint8)
    stroke = max(1, round(1.6 * scale * ss))
    cv2.fillPoly(fill, [pts], 255)
    cv2.polylines(fill, [pts], True, 0, stroke, cv2.LINE_AA)
    cv2.fillPoly(mask, [pts], 255)
    cv2.polylines(mask, [pts], True, 255, stroke)
    t = cv2.resize(fill, (w, h), interpolation=cv2.INTER_AREA)
    m = (cv2.resize(mask, (w, h), interpolation=cv2.INTER_AREA) > 200).astype(np.uint8)
    t = 255 - t if invert else t
    t[m == 0] = round(t[m == 1].mean())  # neutral outside the arrow, so the unmasked search ignores the background
    return t, m


def match(gray: np.ndarray, t: np.ndarray, m: np.ndarray, roi=None) -> tuple[float, int, int]:
    """Best match -> (score, tip x, tip y); the tip is one template pixel in from the corner."""
    x0, y0 = 0, 0
    if roi is not None:
        x0, y0, x1, y1 = roi
        x0, y0 = max(0, x0), max(0, y0)
        gray = gray[y0:min(gray.shape[0], y1), x0:min(gray.shape[1], x1)]
    if gray.shape[0] < t.shape[0] or gray.shape[1] < t.shape[1]:
        return 0.0, 0, 0
    r = np.nan_to_num(cv2.matchTemplate(gray, t, cv2.TM_CCOEFF_NORMED, mask=m), nan=0.0, posinf=0.0, neginf=0.0)
    _, mx, _, loc = cv2.minMaxLoc(r)
    return mx, x0 + loc[0] + 1, y0 + loc[1] + 1


def calibrate(frames: list[np.ndarray]) -> tuple[float, bool] | None:
    """Scale and polarity of the arrow from sample frames (gray, full size); None - no cursor in the video.

    A fast search without the mask gives candidate places, the masked match checks them. The same scale has to win on
    two frames, so a random arrow-like corner on a phone screen does not count as a cursor.
    """
    wins: dict[tuple[float, bool], int] = {}
    for g in frames:
        k = min(g.shape[:2]) / 1080
        f = 0.5 if k >= 0.75 else 1.0  # a coarse pass at half size, unless the video is small already
        half = cv2.resize(g, None, fx=f, fy=f, interpolation=cv2.INTER_AREA)
        best = (0.0, 0.0, False)
        for inv in (False, True):
            for s in SCALES:
                if s * k < MIN_PX_SCALE:
                    continue
                t, m = template(s * k, inv)
                r = cv2.matchTemplate(half, template(s * k * f, inv)[0], cv2.TM_CCOEFF_NORMED)
                for _ in range(8):
                    _, _, _, (hx, hy) = cv2.minMaxLoc(r)
                    r[max(0, hy - 4):hy + 4, max(0, hx - 4):hx + 4] = -1
                    x, y = round(hx / f), round(hy / f)
                    sc = match(g, t, m, (x - 6, y - 6, x + t.shape[1] + 6, y + t.shape[0] + 6))[0]
                    if sc > best[0]:
                        best = (sc, s, inv)
        if best[0] >= CAL_SCORE:
            key = (best[1], best[2])
            wins[key] = wins.get(key, 0) + 1
            if wins[key] >= 2:
                return best[1] * k, best[2]
    return None


class Tracker:
    def __init__(self, scale: float, invert: bool, frame_h: int):
        self.scale = scale
        self.t, self.m = template(scale, invert)
        self.near = round(NEAR * frame_h / 1080)
        self.pos: tuple[int, int] | None = None

    def box(self, pos=None) -> tuple[int, int, int, int] | None:
        """Area to ignore when comparing frames: the arrow and a click ring around the tip."""
        p = pos or self.pos
        if p is None:
            return None
        r = round(30 * self.scale)
        return p[0] - r, p[1] - r, p[0] + r, p[1] + round(36 * self.scale)

    def update(self, gray: np.ndarray, moved: list[tuple[int, int, int, int]], force_global: bool) -> tuple[int, int] | None:
        """moved - boxes (x0, y0, x1, y1) of changed areas in full-frame pixels."""
        if self.pos is not None:
            b = self.box()
            if not any(x0 < b[2] and b[0] < x1 and y0 < b[3] and b[1] < y1 for x0, y0, x1, y1 in moved):
                return self.pos  # nothing moved around the arrow
            x, y = self.pos
            sc, tx, ty = match(gray, self.t, self.m, (x - self.near, y - self.near, x + self.near, y + self.near))
            if sc >= MIN_SCORE:
                self.pos = (tx, ty)
                return self.pos
        pad = self.near // 2
        for x0, y0, x1, y1 in moved:
            sc, tx, ty = match(gray, self.t, self.m, (x0 - pad, y0 - pad, x1 + pad, y1 + pad))
            if sc >= MIN_SCORE:
                self.pos = (tx, ty)
                return self.pos
        if force_global:
            sc, tx, ty = match(gray, self.t, self.m)
            self.pos = (tx, ty) if sc >= MIN_SCORE else None
            return self.pos
        self.pos = None if moved else self.pos
        return self.pos
