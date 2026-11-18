"""Motion: what moved between every two neighbouring frames, and what went back to how it looked a moment ago.

The screen states see only stable frames, so a menu that jumps and settles, a page that shifts for one frame, a thumb
that blinks while dragged are invisible there. Here every frame is compared with the one before at small size, the
cursor left out; each changed area is tested for a shift (phase correlation, then the shift must explain most of the
changed pixels, with a clear correlation peak) and for a return to a look it had up to a second ago (a blink, a flicker).
A look that lasts one or two frames between two changes of the same area (a status that flashes past, a menu shown
whole for a frame before it jumps) is kept as a transient, with a full-size crop of that frame for OCR.
"""
from pathlib import Path

import cv2
import numpy as np

SMALL_W = 960
DIFF = 18
MIN_PX = 25  # changed px of the small frame
EXPLAINED = 0.7  # share of the changed px a shift must explain
HISTORY_MS = 1000  # how far back to look for a return
SAME = 0.02  # share of differing px for two looks to be one
PEAK = 0.3  # phase correlation peak; text lines and icons that only look alike give a weak one
TRANSIENT_FRAMES = 2  # a look that lasts at most this many frames between two changes of one area
MAX_TRANSIENTS = 40


def shift_of(a: np.ndarray, b: np.ndarray, changed: np.ndarray) -> tuple[int, int] | None:
    """The shift (dx, dy) of b against a that explains most changed pixels, or None. The strongest peak of the phase
    correlation away from zero: an unchanged background gives the zero peak, the moved content the other one."""
    h, w = a.shape
    if h < 8 or w < 8:
        return None
    win = cv2.createHanningWindow((w, h), cv2.CV_32F)
    fa, fb = np.fft.fft2(a * win), np.fft.fft2(b * win)
    r = fb * np.conj(fa)
    r = np.real(np.fft.ifft2(r / (np.abs(r) + 1e-6)))
    r[:2, :2] = r[:2, -2:] = r[-2:, :2] = r[-2:, -2:] = -1
    py, px = np.unravel_index(int(np.argmax(r)), r.shape)
    dy, dx = (py if py <= h // 2 else py - h), (px if px <= w // 2 else px - w)
    if abs(dx) < 2 and abs(dy) < 2 or r[py, px] < PEAK:
        return None
    ys, xs = np.nonzero(changed)
    sy, sx = ys - dy, xs - dx
    ok = (sy >= 0) & (sy < h) & (sx >= 0) & (sx < w)
    if ok.sum() < 0.5 * len(ys):
        return None
    good = np.abs(b[ys[ok], xs[ok]] - a[sy[ok], sx[ok]]) <= DIFF
    return (int(dx), int(dy)) if good.sum() >= EXPLAINED * len(ys) else None


def overlap(a, b) -> bool:
    return a[0] < b[0] + b[2] and b[0] < a[0] + a[2] and a[1] < b[1] + b[3] and b[1] < a[1] + a[3]


def scan(video: Path, region: list[int], track: list[list], cursor_scale: float | None, crops: Path | None = None) -> dict:
    """-> {"fps", "moves": [[t_ms, x, y, w, h, dx, dy, px]], "changes": [[t_ms, x, y, w, h, back_ms]]}, boxes and shifts
    in full-frame px. Pieces of one frame that moved by the same shift are one move (a scrolled page is many text
    lines); px - changed pixels of the small frame it explains. back_ms > 0: the area now looks as it did that long
    ago (it went back)."""
    rx, ry, rw, rh = region
    k = SMALL_W / max(rw, rh)
    size = (round(rw * k), round(rh * k))
    cap = cv2.VideoCapture(str(video))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    r = round(30 * (cursor_scale or 0) * k) + 2
    pos = {}
    for p in track:
        pos[p[0]] = (p[1], p[2])
    times = sorted(pos)
    moves, changes, transients = [], [], []
    hist: list[np.ndarray] = []
    recent: list[np.ndarray] = []  # the last few frames at full size, for the crop of a transient
    boxes_at: dict[int, list] = {}  # frame index -> changed boxes (small frame)
    if crops:
        crops.mkdir(parents=True, exist_ok=True)
        for f in crops.glob("*.jpg"):
            f.unlink()
    keep = max(3, round(fps * HISTORY_MS / 1000))
    i, ti, cur_pos = 0, 0, None
    prev = prev_pos = None
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        t = round(i / fps * 1000)
        while ti < len(times) and times[ti] <= t:
            cur_pos = pos[times[ti]]
            ti += 1
        g = cv2.cvtColor(cv2.resize(frame[ry:ry + rh, rx:rx + rw], size, interpolation=cv2.INTER_AREA), cv2.COLOR_BGR2GRAY).astype(np.float32)
        if prev is not None:
            m = np.abs(g - prev) > DIFF
            if cursor_scale:
                for c in (cur_pos, prev_pos):
                    if c and c[0] is not None:
                        cx, cy = round((c[0] - rx) * k), round((c[1] - ry) * k)
                        m[max(0, cy - r):cy + 2 * r, max(0, cx - r):cx + r] = False
            if m.sum() >= MIN_PX:
                n, labels, st, _ = cv2.connectedComponentsWithStats(cv2.dilate(m.astype(np.uint8), np.ones((9, 9), np.uint8)))
                cnt = np.bincount(labels[m], minlength=n)
                shifts: dict[tuple[int, int], list] = {}
                for lab in range(1, n):
                    if cnt[lab] < MIN_PX:
                        continue
                    x, y, w, h = (int(v) for v in st[lab, :4])
                    full = [rx + round(x / k), ry + round(y / k), round(w / k), round(h / k)]
                    pad = 8
                    x0, y0, x1, y1 = max(0, x - pad), max(0, y - pad), min(size[0], x + w + pad), min(size[1], y + h + pad)
                    d = shift_of(prev[y0:y1, x0:x1], g[y0:y1, x0:x1], m[y0:y1, x0:x1] & (labels[y0:y1, x0:x1] == lab)) if min(w, h) >= 6 else None
                    if d:
                        same = next((s for s in shifts if abs(s[0] - d[0]) <= 1 and abs(s[1] - d[1]) <= 1), d)
                        shifts.setdefault(same, []).append((x, y, w, h, int(cnt[lab])))
                        continue
                    back = 0
                    sel = m[y:y + h, x:x + w] & (labels[y:y + h, x:x + w] == lab)
                    if w * h <= 0.3 * size[0] * size[1]:
                        for j in range(len(hist) - 2, -1, -1):
                            if (np.abs(g[y:y + h, x:x + w] - hist[j][y:y + h, x:x + w])[sel] > DIFF).mean() < SAME:
                                back = round((len(hist) - j) * 1000 / fps)
                                break
                    changes.append([t, *full, back])
                    boxes_at.setdefault(i, []).append((x, y, w, h, full))
                for d, parts in shifts.items():
                    x0, y0 = min(p[0] for p in parts), min(p[1] for p in parts)
                    x1, y1 = max(p[0] + p[2] for p in parts), max(p[1] + p[3] for p in parts)
                    moves.append([t, rx + round(x0 / k), ry + round(y0 / k), round((x1 - x0) / k), round((y1 - y0) / k), round(d[0] / k), round(d[1] / k), sum(p[4] for p in parts)])
        # a transient: an area changed at frame i - n and changes again now, and had not been changing before that
        for x, y, w, h, fb in boxes_at.get(i, []) if crops and len(transients) < MAX_TRANSIENTS * 3 else []:
            for n in range(1, TRANSIENT_FRAMES + 1):
                first = [b for b in boxes_at.get(i - n, []) if overlap(b[:4], (x, y, w, h))]
                if first and len(recent) >= n:
                    bx = [min(fb[0], first[0][4][0]), min(fb[1], first[0][4][1])]
                    bx += [max(fb[0] + fb[2], first[0][4][0] + first[0][4][2]) - bx[0], max(fb[1] + fb[3], first[0][4][1] + first[0][4][3]) - bx[1]]
                    img = recent[-n]  # recent[-1] is frame i - 1: the transient look is frames i - n .. i - 1
                    pad = 12
                    c = img[max(0, bx[1] - pad):bx[1] + bx[3] + pad, max(0, bx[0] - pad):bx[0] + bx[2] + pad]
                    name = crops / f"{round((i - n) / fps * 1000):07d}-{bx[0]}-{bx[1]}.jpg"
                    if c.size:
                        cv2.imwrite(str(name), c, [cv2.IMWRITE_JPEG_QUALITY, 92])
                        transients.append([round((i - n) / fps * 1000), *bx, n, name.name])
                    break
        hist.append(g)
        if len(hist) > keep:
            hist.pop(0)
        recent.append(frame)
        if len(recent) > TRANSIENT_FRAMES + 2:
            recent.pop(0)
        boxes_at.pop(i - 6, None)
        prev, prev_pos = g, cur_pos
        i += 1
    cap.release()
    # many transients in one place are an animation or a playing video, not a flash: keep the isolated ones
    lone = [tr for tr in transients if sum(overlap(tr[1:5], o[1:5]) and abs(tr[0] - o[0]) < 1000 for o in transients) <= 4][:MAX_TRANSIENTS]
    for tr in transients:
        if tr not in lone and crops:
            (crops / tr[6]).unlink(missing_ok=True)
    return {"fps": fps, "moves": moves, "changes": changes, "transients": lone}
