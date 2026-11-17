"""Mouse cursor: its sprites are learnt from the video itself, then followed near the last position and where the frame moved.

Learning goes by motion: when only small areas change over three distinct frames in a row, the middle frame shows the
cursor where it differs from both neighbours while they agree with each other (the background there). Such cut-outs are
grouped by shape and aligned; pixels that stay the same over many backgrounds are the sprite, and an area they enclose
belongs to it too (a white arrow on a white page). A shape seen in enough places (arrow, hand, I-beam) becomes a template
of its own; a spot that only moves in one place (a spinner), a flat or round mark (a phone's touch circle) does not.
A learnt sprite fits where the RMS difference inside its mask is small against its own contrast, so even a 10 px arrow
does not fit any dark corner. The drawn arrow (white with a black outline, or inverted) found by calibrate() is one more
template: generated videos use it. Portrait videos (phones) learn nothing: they have touch marks, not a cursor.
"""
import cv2
import numpy as np

POLY = np.array([(3, 2), (3, 24), (9, 18.5), (13, 27), (17, 25), (13, 17), (21, 17)], float)
SCALES = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.25]  # of a 1080p frame
MIN_SCORE = 0.8
CAL_SCORE = 0.86  # to accept that a video has a cursor at all (an arrow-like icon on a phone scores ~0.84)
MIN_PX_SCALE = 0.35  # a smaller template (under ~8 px) matches anything
NEAR = 160  # search radius around the last position, px of a 1080p frame

DIFF = 24  # brightness step that counts as a change while learning
PAD = 6  # px around a cut-out
FIT = 0.45  # a learnt sprite fits where the RMS difference is under 0.55 of its contrast (elsewhere: up to ~0.3)
MIN_SEEN = 5  # cut-outs a shape needs to count as a cursor
LOOSE = 0.6  # drawn arrow score that already explains a cut-out
MIN_CONTRAST = 25  # std of a sprite's pixels; a flat mark is not a cursor
MAX_TRIPLES = 2500
MAX_CUTS = 600
ARROW_H = 26  # px of the drawn arrow at scale 1


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


def crop(gray: np.ndarray, roi) -> tuple[np.ndarray, int, int]:
    if roi is None:
        return gray, 0, 0
    x0, y0, x1, y1 = roi
    x0, y0 = max(0, x0), max(0, y0)
    return gray[y0:min(gray.shape[0], y1), x0:min(gray.shape[1], x1)], x0, y0


def match(gray: np.ndarray, t: np.ndarray, m: np.ndarray, roi=None) -> tuple[float, int, int]:
    """Best match of the drawn arrow -> (score, tip x, tip y); the tip is one template pixel in from the corner."""
    gray, x0, y0 = crop(gray, roi)
    if gray.shape[0] < t.shape[0] or gray.shape[1] < t.shape[1]:
        return 0.0, 0, 0
    r = np.nan_to_num(cv2.matchTemplate(gray, t, cv2.TM_CCOEFF_NORMED, mask=m), nan=0.0, posinf=0.0, neginf=0.0)
    _, mx, _, loc = cv2.minMaxLoc(r)
    return mx, x0 + loc[0] + 1, y0 + loc[1] + 1


def fit(gray: np.ndarray, s: dict, roi=None) -> tuple[float, int, int]:
    """Best place of a sprite -> (score, hotspot x, hotspot y); it is there if score >= s["min"]."""
    if s["drawn"]:
        return match(gray, s["t"], s["m"], roi)
    gray, x0, y0 = crop(gray, roi)
    t = s["t"]
    if gray.shape[0] < t.shape[0] or gray.shape[1] < t.shape[1]:
        return 0.0, 0, 0
    r = np.nan_to_num(cv2.matchTemplate(gray, t, cv2.TM_SQDIFF, mask=s["m"]), nan=1e12, posinf=1e12, neginf=1e12)
    mn, _, loc, _ = cv2.minMaxLoc(r)
    return 1 - (max(0.0, mn) / s["n"]) ** 0.5 / s["sd"], x0 + loc[0] + s["hot"][0], y0 + loc[1] + s["hot"][1]


def drawn(scale: float, invert: bool) -> dict:
    t, m = template(scale, invert)
    return {"t": t, "m": m, "hot": (1, 1), "kind": "arrow", "drawn": True, "min": MIN_SCORE, "h": ARROW_H * scale}


def calibrate(frames: list[np.ndarray]) -> tuple[float, bool] | None:
    """Scale and polarity of the drawn arrow from sample frames (gray, full size); None - no such arrow.

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


# --- learning sprites from motion ---------------------------------------------------------------------------------

def holes(m: np.ndarray) -> np.ndarray:
    """The mask with the areas it encloses filled."""
    h, w = m.shape
    out = np.ones((h + 2, w + 2), np.uint8)
    out[1:-1, 1:-1] = m == 0
    cv2.floodFill(out, np.zeros((h + 4, w + 4), np.uint8), (0, 0), 2)
    return (out[1:-1, 1:-1] != 2).astype(np.uint8)


def cutouts(video, region) -> tuple[list[dict], int]:
    """Moving small things: a distinct frame where it differs from a frame before and one after, which agree there.
    Neighbours one apart and ~1/15 s apart: a slow cursor still overlaps itself in the next frame."""
    cap = cv2.VideoCapture(str(video))
    n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    gap = max(1, round(cap.get(cv2.CAP_PROP_FPS) / 15))
    rx, ry, rw, rh = region
    side = min(rw, rh)
    lo, hi = 7, max(24, round(0.06 * side))
    S = hi + 2 * PAD
    stride = max(1, n // MAX_TRIPLES)
    ker = np.ones((5, 5), np.uint8)
    buf: list[np.ndarray] = []
    out: list[dict] = []
    d = 0
    while True:
        ok, fr = cap.read()
        if not ok:
            break
        g = cv2.cvtColor(fr[ry:ry + rh, rx:rx + rw], cv2.COLOR_BGR2GRAY)
        if buf and np.count_nonzero(cv2.absdiff(g, buf[-1]) > DIFF) < 3:
            continue  # a repeated frame
        buf = (buf + [g])[-(2 * gap + 1):]
        d += 1
        if len(buf) < 2 * gap + 1 or d % stride:
            continue
        b = buf[gap]
        for k in sorted({1, gap}):
            a, c = buf[gap - k], buf[gap + k]
            dab, dbc = cv2.absdiff(a, b) > DIFF, cv2.absdiff(b, c) > DIFF
            if dab.mean() > 0.02 or dbc.mean() > 0.02:
                continue  # scrolling, a new page
            m = dab & dbc & (cv2.absdiff(a, c) <= DIFF)
            num, lab, st, _ = cv2.connectedComponentsWithStats(cv2.dilate(m.astype(np.uint8), ker))
            comps = [j for j in range(1, num) if st[j, 4] >= 20]
            if not comps or len(comps) > 3:
                continue
            for j in comps:
                x, y, w, h = st[j, :4]
                ys, xs = np.nonzero((lab[y:y + h, x:x + w] == j) & m[y:y + h, x:x + w])
                if len(xs) < 12:
                    continue
                x0, y0, x1, y1 = x + xs.min(), y + ys.min(), x + xs.max() + 1, y + ys.max() + 1
                if not (lo <= y1 - y0 <= hi and 3 <= x1 - x0 <= hi) or x0 < PAD or y0 < PAD or x0 - PAD + S > rw or y0 - PAD + S > rh:
                    continue
                sl = np.s_[y0 - PAD:y0 - PAD + S, x0 - PAD:x0 - PAD + S]
                out.append({"x": int(x0), "y": int(y0), "w": int(x1 - x0), "h": int(y1 - y0), "B": b[sl].copy(), "fg": (m[sl] & (lab[sl] == j)).astype(np.uint8)})
    cap.release()
    return out, S


def groups(cuts: list[dict]) -> list[list[dict]]:
    """Cut-outs of one shape: about the same size and the same filled outline."""
    out: list[tuple[dict, np.ndarray, list[dict]]] = []
    for c in sorted(cuts, key=lambda c: -int(c["fg"].sum())):
        f = holes(c["fg"])
        for seed, sf, members in out:
            if abs(seed["w"] - c["w"]) <= max(2, 0.2 * seed["w"]) and abs(seed["h"] - c["h"]) <= max(2, 0.2 * seed["h"]) \
                    and np.count_nonzero(sf & f) >= 0.5 * np.count_nonzero(sf | f):
                members.append(c)
                break
        else:
            out.append((c, f, [c]))
    return [m for _, _, m in out]


def sprite(stack: np.ndarray, fgs: np.ndarray) -> dict | None:
    """A sprite from aligned cut-outs (NaN - no data): pixels that differ from the background often and stay the same."""
    seen = np.count_nonzero(~np.isnan(stack), 0) >= 0.5 * len(stack)
    med = np.nanmedian(np.where(seen, stack, 0), 0)
    mad = np.nanmedian(np.abs(np.where(seen, stack, 1e3) - med), 0)
    steady = seen & (mad <= 20)
    m = holes(((np.nanmean(np.where(seen, fgs, 0), 0) >= 0.3) & steady).astype(np.uint8)) & steady
    n, lab, st, _ = cv2.connectedComponentsWithStats(m.astype(np.uint8), connectivity=8)
    if n < 2:
        return None
    m = np.isin(lab, [j for j in range(1, n) if st[j, 4] >= max(4, 0.05 * st[1:, 4].max())])  # specks of background
    ys, xs = np.nonzero(m)
    if len(xs) < 12:
        return None
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    m = m[y0:y1, x0:x1].astype(np.uint8)
    t = med[y0:y1, x0:x1].astype(np.uint8)
    sd = float(t[m > 0].std())
    h, w = m.shape
    sym = np.count_nonzero(m & m[:, ::-1]) / np.count_nonzero(m)
    rows = m.sum(1)
    ends = max(rows[:max(1, h // 6)].max(), rows[-max(1, h // 6):].max())
    px = t[m > 0].astype(np.float32)
    off = np.count_nonzero(np.abs(px - np.median(px)) > 40)  # pixels that are not the main tone: what a match rests on
    if sd < MIN_CONTRAST or (off < 10 and off < 0.25 * len(px)) or (0.8 <= w / h <= 1.25 and 0.6 <= m.mean() <= 0.9 and sym > 0.85) \
            or (w <= 0.4 * h and ends < 2 * np.median(rows[h // 3:2 * h // 3])):
        return None  # flat or almost (a white hand whose outline was lost on dark pages), a round touch mark, a text caret
    edge = np.mean([r.any() and np.argmax(r) <= max(1, 0.2 * w) for r in m[:max(2, h // 2)]])
    if sym > 0.75:  # I-beam, crosshair, resize arrows: the hotspot is the middle
        hot, kind = (w // 2, h // 2), "text" if w <= 0.6 * h else "other"
    elif edge >= 0.5:  # an arrow: a straight left edge down from the tip
        hot, kind = (int(np.argmax(m[0])), 0), "arrow"
    else:  # a hand: the fingertip
        hot, kind = (int(np.nonzero(m[0])[0].mean()), 0), "hand"
    if h < 14:
        kind = None  # too few pixels to tell a hand from an arrow
    t[m == 0] = round(t[m > 0].mean())
    return {"t": t, "m": m, "hot": hot, "kind": kind, "drawn": False, "min": FIT, "n": int(m.sum()), "sd": max(sd, 1.0), "h": h}


def first_guess(members: list[dict]) -> dict | None:
    """Sprite of a group: cut-outs aligned by their top left corner, then each moved by up to 2 px towards the median."""
    shifts = [(0, 0)] * len(members)
    for _ in range(2):
        stack = np.stack([np.roll(c["B"], s, (0, 1)) for c, s in zip(members, shifts)]).astype(np.float32)
        frac = np.stack([np.roll(c["fg"], s, (0, 1)) for c, s in zip(members, shifts)]).mean(0)
        med, sel = np.median(stack, 0), frac >= 0.5
        if sel.sum() < 5:
            return None
        shifts = [min(((dy, dx) for dy in range(-2, 3) for dx in range(-2, 3)),
                      key=lambda s: float(np.abs(np.roll(c["B"], s, (0, 1)).astype(np.float32) - med)[sel].mean())) for c in members]
    return sprite(np.stack([np.roll(c["B"], s, (0, 1)) for c, s in zip(members, shifts)]).astype(np.float32),
                  np.stack([np.roll(c["fg"], s, (0, 1)) for c, s in zip(members, shifts)]).astype(np.float32))


def refit(s: dict, cuts: list[dict], hits: dict[int, tuple[int, int]], S: int) -> dict | None:
    """The sprite again from the cut-outs it fits, aligned where it fits, in a window wide enough for a whole cursor:
    a template of part of a shape (the palm of a hand) grows to the whole shape."""
    if len(hits) < MIN_SEEN:
        return None
    stack, fgs = [], []
    for i, (hx, hy) in hits.items():
        b, f = np.full((3 * S, 3 * S), np.nan, np.float32), np.full((3 * S, 3 * S), np.nan, np.float32)
        b[S:2 * S, S:2 * S], f[S:2 * S, S:2 * S] = cuts[i]["B"], cuts[i]["fg"]
        stack.append(b[hy:hy + 2 * S, hx:hx + 2 * S])
        fgs.append(f[hy:hy + 2 * S, hx:hx + 2 * S])
    return sprite(np.stack(stack), np.stack(fgs))


def same(a: dict, b: dict) -> bool:
    """One sprite fits the picture of the other."""
    for x, y in ((a, b), (b, a)):
        h, w = y["t"].shape
        img = np.full((h + 8, w + 8), int(y["t"][y["m"] > 0].mean()), np.uint8)
        img[4:4 + h, 4:4 + w] = np.where(y["m"] > 0, y["t"], img[4:4 + h, 4:4 + w])
        if fit(img, x)[0] >= x["min"]:
            return True
    return False


def learn(video, region, given: list[dict]) -> list[dict]:
    """Sprites seen moving in the screen region that the given ones (the drawn arrow) do not already explain."""
    cuts, S = cutouts(video, region)
    cuts = cuts[::max(1, -(-len(cuts) // MAX_CUTS))]  # an even sample: every candidate is fitted to every cut-out
    side = min(region[2], region[3])
    cands = [s for s in (first_guess(m) for m in sorted(groups(cuts), key=len, reverse=True)[:12] if len(m) >= 3) if s]

    def hits(s: dict, floor: float | None = None) -> dict[int, tuple[int, int]]:
        out = {}
        for i, c in enumerate(cuts):
            sc, x, y = fit(c["B"], s)
            if sc >= (floor or s["min"]):
                out[i] = (x, y)
        return out

    covered: set[int] = set()
    for s in given:  # loosely: a resampled copy of the drawn arrow (a shared screen scaled down) is not a new shape
        covered |= hits(s, LOOSE).keys()
    pool = []
    for s in cands:
        r = refit(s, cuts, hits(s), S)
        if r:
            pool.append((r, hits(r)))
    out: list[dict] = []
    while pool:
        s, h = pool.pop(max(range(len(pool)), key=lambda i: len(pool[i][1].keys() - covered)))
        new = {i: p for i, p in h.items() if i not in covered}
        if len(new) < MIN_SEEN:
            break
        xs, ys = [cuts[i]["x"] for i in new], [cuts[i]["y"] for i in new]
        covered |= h.keys()
        if max(max(xs) - min(xs), max(ys) - min(ys)) >= 0.08 * side and not any(same(s, o) for o in given + out):
            out.append(s)  # not an animation in one place, not a variant of a shape already there
    return out


def sprites(video, samples: list[np.ndarray], region) -> tuple[list[dict], float] | None:
    """Every cursor template of a video and the cursor scale (1 = the drawn arrow of a 1080p frame); None - no cursor."""
    cal = calibrate(samples)
    given = [drawn(*cal)] if cal else []
    if region[3] <= 1.3 * region[2]:
        given += learn(video, region, given)
    if not given:
        return None
    arrows = [s["h"] for s in given if s["kind"] == "arrow"]
    return given, cal[0] if cal else (arrows[0] if arrows else max(s["h"] for s in given)) / ARROW_H


class Tracker:
    def __init__(self, templates: list[dict], scale: float, frame_h: int):
        self.sprites = templates
        self.scale = scale
        self.near = round(NEAR * frame_h / 1080)
        self.pos: tuple[int, int] | None = None
        self.kind: str | None = None

    def box(self, pos=None) -> tuple[int, int, int, int] | None:
        """Area to ignore when comparing frames: the cursor and a click ring around the tip."""
        p = pos or self.pos
        if p is None:
            return None
        r = round(30 * self.scale)
        return p[0] - r, p[1] - r, p[0] + r, p[1] + round(36 * self.scale)

    def find(self, gray: np.ndarray, roi=None) -> tuple[int, int] | None:
        best = None
        for s in self.sprites:
            sc, x, y = fit(gray, s, roi)
            if sc >= s["min"] and (best is None or (sc - s["min"]) / (1 - s["min"]) > best[0]):
                best = ((sc - s["min"]) / (1 - s["min"]), x, y, s["kind"])
        if best is None:
            return None
        self.kind = best[3]
        return best[1], best[2]

    def update(self, gray: np.ndarray, moved: list[tuple[int, int, int, int]], force_global: bool) -> tuple[int, int] | None:
        """moved - boxes (x0, y0, x1, y1) of changed areas in full-frame pixels."""
        if self.pos is not None:
            b = self.box()
            if not any(x0 < b[2] and b[0] < x1 and y0 < b[3] and b[1] < y1 for x0, y0, x1, y1 in moved):
                return self.pos  # nothing moved around the cursor
            x, y = self.pos
            p = self.find(gray, (x - self.near, y - self.near, x + self.near, y + self.near))
            if p:
                self.pos = p
                return p
        pad = self.near // 2
        for x0, y0, x1, y1 in moved:
            p = self.find(gray, (x0 - pad, y0 - pad, x1 + pad, y1 + pad))
            if p:
                self.pos = p
                return p
        if force_global:
            self.pos = self.find(gray)
            return self.pos
        self.pos = None if moved else self.pos
        return self.pos
