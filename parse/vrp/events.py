"""Neighbouring screen states -> events; the cursor track -> clicks and hovers.

Text that appeared or disappeared is grouped by its container: the area of one background colour around it (a message
bubble, a dialog, a menu, a toast). So a new message is one event with all its lines, not one event per OCR line.
A container whose own text changed gives a text_change; pixels that changed inside a container without any text change
(a status icon, a check mark, a lock) give a visual_change. Clicks are inferred: the cursor stopped and the screen
changed right after; hovers are the cursor wiggling over one place.
"""
import re
from pathlib import Path

import cv2
import numpy as np
from rapidfuzz import fuzz
from rapidfuzz.distance import Levenshtein

from .slides import page_of

DIFF = 18
SMALL_W = 960
MAX_CONTAINER = 0.06  # share of the screen; a larger same-colour area is a panel or the page, not a container
MAX_DIALOG = 0.2  # unless it is new: a dialog
SCREEN_CHANGE = 0.6  # share of texts that changed for the whole screen to count as changed
SCREEN_AREA = 0.3  # or share of the screen whose pixels changed (a slide inside a meeting app)


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.lower().replace("ё", "е")).strip()


def same(a: str, b: str) -> bool:
    """One text read twice: close spelling and the same numbers ("Uploading 12%" is not "Uploading 99%")."""
    a, b = norm(a), norm(b)
    return re.findall(r"\d+", a) == re.findall(r"\d+", b) and fuzz.ratio(a, b) >= 88


def still_there(t: dict, others: list[dict]) -> bool:
    """The same text near the same place (content may shift a little, e.g. older messages move up)."""
    x, y = t["bbox"][:2]
    return any(abs(o["bbox"][0] - x) <= 40 and abs(o["bbox"][1] - y) <= 250 and same(o["text"], t["text"]) for o in others)


def match_texts(prev: list[dict], cur: list[dict]) -> tuple[list[dict], list[dict]]:
    """One-to-one: every text of the previous state accounts for one text of the current state, the nearest one with
    the same reading (so "private" in the next row does not hide a row that turned "private"). -> (added, removed)"""
    pairs = []
    for i, c in enumerate(cur):
        # this place held another text before: the text changed here, a far copy of the new text does not explain it
        replaced = any(iou(p["bbox"], c["bbox"]) > 0.3 and not same(p["text"], c["text"]) for p in prev)
        for j, p in enumerate(prev):
            dx, dy = abs(p["bbox"][0] - c["bbox"][0]), abs(p["bbox"][1] - c["bbox"][1])
            if dx <= 40 and dy <= 250 and same(p["text"], c["text"]) and not (replaced and dx + dy > 12):
                pairs.append((dx + dy, i, j))
    used_c, used_p = set(), set()
    for _, i, j in sorted(pairs):
        if i not in used_c and j not in used_p:
            used_c.add(i)
            used_p.add(j)
    return [c for i, c in enumerate(cur) if i not in used_c], [p for j, p in enumerate(prev) if j not in used_p]


def iou(a, b) -> float:
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    ix, iy = max(0, min(ax + aw, bx + bw) - max(ax, bx)), max(0, min(ay + ah, by + bh) - max(ay, by))
    inter = ix * iy
    return inter / (aw * ah + bw * bh - inter) if inter else 0.0


def inside(box, outer, pad: int = 0) -> bool:
    cx, cy = box[0] + box[2] / 2, box[1] + box[3] / 2
    return outer[0] - pad <= cx <= outer[0] + outer[2] + pad and outer[1] - pad <= cy <= outer[1] + outer[3] + pad


def union(boxes) -> list[int]:
    x0, y0 = min(b[0] for b in boxes), min(b[1] for b in boxes)
    x1, y1 = max(b[0] + b[2] for b in boxes), max(b[1] + b[3] for b in boxes)
    return [x0, y0, x1 - x0, y1 - y0]


def reading(texts: list[dict]) -> str:
    """Texts in reading order: lines top to bottom, " | " between lines."""
    if not texts:
        return ""
    lines: list[list[dict]] = []
    for t in sorted(texts, key=lambda t: t["bbox"][1] + t["bbox"][3] / 2):
        cy = t["bbox"][1] + t["bbox"][3] / 2
        if lines and abs(cy - (lines[-1][0]["bbox"][1] + lines[-1][0]["bbox"][3] / 2)) < 0.6 * t["bbox"][3]:
            lines[-1].append(t)
        else:
            lines.append([t])
    return " | ".join(" ".join(t["text"] for t in sorted(ln, key=lambda t: t["bbox"][0])) for ln in lines)


def merge_same(screens: list[dict]) -> list[dict]:
    """Neighbouring states with the same text (the cursor moved, a participant tile blinked) are merged."""
    out = []
    for s in screens:
        if out:
            p = out[-1]
            a, b = sorted(norm(t["text"]) for t in p["texts"]), sorted(norm(t["text"]) for t in s["texts"])
            if a == b and not visual_diff(p, s):
                p["end_ms"] = s["end_ms"]
                continue
        out.append(s)
    return out


# --- pixels -------------------------------------------------------------------------------------------------------

_imgs: dict[str, np.ndarray] = {}
WORK: Path = Path(".")
REGION: list[int] = [0, 0, 0, 0]
TRACK: list[list] = []
CURSOR_SCALE: float | None = None
TOUCH: str | None = None  # why the screen looks like a touch screen
PEOPLE: list[int] | None = None  # participant tiles of a meeting
FPS = 30.0


def setup(work: Path, meta: dict, track: list[list]) -> None:
    """Context of one video: where key frames are, the screen region, the cursor track."""
    global WORK, REGION, TRACK, CURSOR_SCALE, FPS, PEOPLE
    WORK, REGION, TRACK, CURSOR_SCALE, FPS = work, meta["regions"]["screen"], track, meta.get("cursor_scale"), meta["fps"]
    PEOPLE = meta["regions"].get("people")
    _imgs.clear()
    _small.clear()


STATUS_CLOCK = re.compile(r"^\d{1,2}[:.]\d{2}$")
DESK_MENU = re.compile(r"^(File|Edit|View|Window|Help|Go)$")


def touch_screen(screens: list[dict], region: list[int], cursor_scale: float | None) -> str | None:
    """Why the recording looks like a phone or tablet screen (a guess, not a fact), or None. Only when no mouse cursor
    was found: a portrait screen, or a mobile status bar - a clock alone at the top left, no desktop menu bar."""
    if cursor_scale is not None:
        return None
    x0, y0, W, H = region
    if H > W:
        return "portrait screen"
    for s in screens[:20]:
        top = [t for t in s["texts"] if t["bbox"][1] + t["bbox"][3] <= y0 + 0.06 * H]
        for c in top:
            if STATUS_CLOCK.match(c["text"].strip()) and c["bbox"][0] < x0 + 0.3 * W:
                cy0, cy1 = c["bbox"][1], c["bbox"][1] + c["bbox"][3]
                row = [t for t in top if cy0 <= t["bbox"][1] + t["bbox"][3] / 2 <= cy1]
                if not any(DESK_MENU.match(t["text"].strip()) for t in row):
                    return "mobile status bar (a clock at the top left)"
    return None


def img(screen: dict) -> np.ndarray:
    f = screen["frame"]
    if f not in _imgs:
        if len(_imgs) > 8:
            _imgs.pop(next(iter(_imgs)))
        _imgs[f] = cv2.imread(str(WORK / f))
    return _imgs[f]


def key_ms(screen: dict) -> int:
    return round(int(Path(screen["frame"]).stem) / FPS * 1000)


def cursor_at(t_ms: int) -> tuple[int, int] | None:
    pos = None
    for t, x, y, *_ in TRACK:
        if t > t_ms:
            break
        pos = (x, y) if x is not None else None
    return pos


def shape_at(t_ms: int) -> str | None:
    """Cursor shape at a moment: arrow, hand, text (I-beam), other; None - unknown."""
    kind = None
    for p in TRACK:
        if p[0] > t_ms:
            break
        kind = p[3] if len(p) > 3 else None
    return kind


def cursor_box(pos) -> list[int] | None:
    if pos is None or CURSOR_SCALE is None:
        return None
    r = round(30 * CURSOR_SCALE)
    return [pos[0] - r, pos[1] - r, 2 * r, r + round(36 * CURSOR_SCALE)]


def changed_areas(a: dict, b: dict) -> list[list[int]]:
    """Boxes (full-frame px) where two key frames differ, the cursor left out."""
    rx, ry, rw, rh = REGION
    k = SMALL_W / max(rw, rh)
    size = (round(rw * k), round(rh * k))
    ga = cv2.cvtColor(cv2.resize(img(a)[ry:ry + rh, rx:rx + rw], size, interpolation=cv2.INTER_AREA), cv2.COLOR_BGR2GRAY)
    gb = cv2.cvtColor(cv2.resize(img(b)[ry:ry + rh, rx:rx + rw], size, interpolation=cv2.INTER_AREA), cv2.COLOR_BGR2GRAY)
    m = cv2.absdiff(ga, gb) > DIFF
    for s in (a, b):
        cb = cursor_box(cursor_at(key_ms(s)))
        if cb:
            x0, y0 = max(0, round((cb[0] - rx) * k)), max(0, round((cb[1] - ry) * k))
            m[y0:round((cb[1] + cb[3] - ry) * k), x0:round((cb[0] + cb[2] - rx) * k)] = False
    n, labels, st, _ = cv2.connectedComponentsWithStats(cv2.dilate(m.astype(np.uint8), np.ones((5, 5), np.uint8)))
    cnt = np.bincount(labels[m], minlength=n)
    return [[rx + round(x / k), ry + round(y / k), round(w / k), round(h / k)] for (x, y, w, h, _), c in zip(st[1:], cnt[1:]) if c >= 25]


def visual_diff(a: dict, b: dict) -> bool:
    return bool(a.get("frame") and b.get("frame") and changed_areas(a, b))


_small: dict[int, tuple[np.ndarray, np.ndarray, float]] = {}


def small(image: np.ndarray) -> tuple[np.ndarray, float]:
    """The screen region at half size, for flood fills; cached per frame (the frame itself is kept, so an id reused
    by another array never hits a stale entry)."""
    hit = _small.get(id(image))
    if hit is None or hit[0] is not image:
        if len(_small) > 8:
            _small.pop(next(iter(_small)))
        rx, ry, rw, rh = REGION
        k = SMALL_W / max(rw, rh)
        hit = (image, cv2.resize(image[ry:ry + rh, rx:rx + rw], (round(rw * k), round(rh * k)), interpolation=cv2.INTER_AREA), k)
        _small[id(image)] = hit
    return hit[1], hit[2]


def fills(image: np.ndarray, box: list[int]) -> list[tuple[list[int], float]]:
    """Same-colour areas around a box, seeded from the pixels just outside each side: (box in full px, share of the
    screen). Thin lines inside are bridged (a progress bar, a divider); the text itself counts as inside."""
    rx, ry, rw, rh = REGION
    sm, k = small(image)
    sh, sw = sm.shape[:2]
    x, y, w, h = ((v - o) * k for v, o in zip(box, (rx, ry, 0, 0)))
    out = []
    for px, py in [(x - 2, y + h / 2), (x + w + 2, y + h / 2), (x + w / 2, y - 2), (x + w / 2, y + h + 2)]:
        px, py = round(px), round(py)
        if not (0 <= px < sw and 0 <= py < sh):
            continue
        mask = (np.abs(sm.astype(np.int16) - sm[py, px].astype(np.int16)).max(axis=2) <= 4).astype(np.uint8)
        mask[max(0, round(y)):round(y + h) + 1, max(0, round(x)):round(x + w) + 1] = 1
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))
        _, labels, st, _ = cv2.connectedComponentsWithStats(mask, connectivity=4)
        lab = labels[py, px]
        if lab == 0:
            continue
        fx, fy, fw, fh = (int(v) for v in st[lab, :4])
        fill = [rx + round(fx / k), ry + round(fy / k), round(fw / k), round(fh / k)]
        if inside(box, fill):  # otherwise the fill is a neighbour, not something around the text
            out.append((fill, fw * fh / (sw * sh)))
    return out


def container(image: np.ndarray, box: list[int], limit: float = MAX_CONTAINER, found: list | None = None) -> list[int]:
    """The largest same-colour area around a box that is not a panel or the page (limit, share of the screen) - a
    bubble rather than the file icon inside it."""
    ok = [(f, a) for f, a in (found if found is not None else fills(image, box)) if a <= limit]
    return union([box, max(ok, key=lambda fa: fa[1])[0]]) if ok else box


def group(texts: list[dict], image: np.ndarray, others: list[dict]) -> list[tuple[list[int], list[dict]]]:
    """Texts -> (container box, texts in it); a container inside a bigger one joins it; a text with no container of
    its own stays single. A large container (a dialog) counts only if it holds more of these texts than of the others
    (texts that did not change): otherwise it is a panel, and a smaller container is taken."""

    def box_for(t: dict) -> list[int]:
        found = fills(image, t["bbox"])
        c = container(image, t["bbox"], MAX_DIALOG, found)
        if c != t["bbox"] and sum(inside(o["bbox"], c) for o in others) <= sum(inside(x["bbox"], c) for x in texts):
            return c
        return container(image, t["bbox"], MAX_CONTAINER, found)

    boxes = [box_for(t) for t in texts]
    order = sorted(range(len(texts)), key=lambda i: -boxes[i][2] * boxes[i][3])
    out: list[tuple[list[int], list[dict]]] = []
    for i in order:
        c, t = boxes[i], texts[i]
        g = next((g for g in out if iou(g[0], c) > 0.8 or inside(c, g[0]) and c[2] * c[3] <= g[0][2] * g[0][3] and g[0] != g[1][0]["bbox"]), None)
        if g:
            g[1].append(t)
        else:
            out.append((c, [t]))
    return out


def front_window(image: np.ndarray, texts: list[dict]) -> dict | None:
    """The front window by its title-bar buttons: three coloured dots (red, yellow, green) in a row; a window in the
    background has them grey. The title is the nearest text to the right on the same line."""
    rx, ry, rw, rh = REGION
    sm, k = small(image)
    hsv = cv2.cvtColor(sm, cv2.COLOR_BGR2HSV)
    sat = (hsv[..., 1] > 110) & (hsv[..., 2] > 140)
    hue = hsv[..., 0]
    red, yellow, green = sat & ((hue < 8) | (hue > 170)), sat & (hue >= 12) & (hue <= 32), sat & (hue >= 45) & (hue <= 85)
    n, _, st, cen = cv2.connectedComponentsWithStats(red.astype(np.uint8))
    for (x, y, w, h, a), (cx, cy) in zip(st[1:], cen[1:]):
        if not (3 <= w <= 12 and 3 <= h <= 12 and abs(w - h) <= 2 and a >= 0.5 * w * h):
            continue
        d = None
        for dx in range(int(1.2 * w), int(3 * w) + 1):
            yx = (round(cy), min(sm.shape[1] - 1, round(cx + dx)))
            gx = (round(cy), min(sm.shape[1] - 1, round(cx + 2 * dx)))
            if yellow[yx] and green[gx]:
                d = dx
                break
        if d is None:
            continue
        fx, fy = rx + (cx + 2 * d) / k, ry + cy / k
        row = [t for t in texts if abs(t["bbox"][1] + t["bbox"][3] / 2 - fy) < 14 and t["bbox"][0] > fx]
        if row:
            row.sort(key=lambda t: t["bbox"][0])
            run = [row[0]]
            for t in row[1:]:  # OCR may split a title in two: "Relay +" "Fabrikam"
                if t["bbox"][0] - (run[-1]["bbox"][0] + run[-1]["bbox"][2]) < 2 * t["bbox"][3]:
                    run.append(t)
            return {"title": " ".join(t["text"] for t in run), "bbox": union([t["bbox"] for t in run]), "y": round(fy)}
    return None


def patch(image: np.ndarray, box: list[int], dx: int = 0, dy: int = 0) -> np.ndarray | None:
    x, y, w, h = box
    x, y = x + dx, y + dy
    if x < 0 or y < 0 or x + w > image.shape[1] or y + h > image.shape[0] or w < 2 or h < 2:
        return None
    return cv2.cvtColor(image[y:y + h, x:x + w], cv2.COLOR_BGR2GRAY).astype(np.float32)


def look(prev_img: np.ndarray, cur_img: np.ndarray, box: list[int]) -> dict | None:
    """How an area changed, in numbers anyone can check: mean brightness before -> after, and in the inner part (the
    frame of a button left out) the share of what was drawn before that is still drawn after, and the reverse."""
    a, b = patch(prev_img, box), patch(cur_img, box)
    if a is None or b is None:
        return None
    out = {"light": [round(float(a.mean())), round(float(b.mean()))]}
    h, w = a.shape
    ia, ib = a[h // 5:h - h // 5, w // 5:w - w // 5], b[h // 5:h - h // 5, w // 5:w - w // 5]
    da, db = np.abs(ia - np.median(ia)) > 25, np.abs(ib - np.median(ib)) > 25
    if da.sum() >= 12:
        out["kept"] = round(float((da & db).sum() / da.sum()), 2)
    if db.sum() >= 12:
        out["new"] = round(float((db & ~da).sum() / db.sum()), 2)
    return out


def look_words(lk: dict | None) -> str:
    """lighter / darker, and what was drawn there vanishing or appearing (an icon gone on hover)."""
    if not lk:
        return ""
    l0, l1 = lk["light"]
    words = ["lighter" if l1 - l0 > 15 else "darker" if l0 - l1 > 15 else ""]
    if lk.get("kept") is not None and lk["kept"] < 0.3:
        words.append(f"the drawing inside is gone, {lk['kept']:.0%} of it left")
    return ", ".join(w for w in words if w)


def similarity(a: np.ndarray | None, b: np.ndarray | None) -> float:
    """Correlation of two patches of one size, independent of brightness and contrast."""
    if a is None or b is None:
        return 0.0
    if a.std() < 3 or b.std() < 3:
        return 1.0 if a.std() < 3 and b.std() < 3 and abs(a.mean() - b.mean()) < 12 else 0.0
    return float(cv2.matchTemplate(a, b, cv2.TM_CCOEFF_NORMED)[0, 0])


def alike(a: np.ndarray | None, b: np.ndarray | None) -> bool:
    """Same picture up to brightness and contrast (a dimmed backdrop keeps the content): after both are normalised,
    almost no pixel differs. Two changed digits in a line ("88%" -> "99%") are enough to differ."""
    if a is None or b is None:
        return False
    if a.std() < 3 or b.std() < 3:
        return a.std() < 3 and b.std() < 3 and abs(a.mean() - b.mean()) < 12
    za, zb = (a - a.mean()) / a.std(), (b - b.mean()) / b.std()
    return float((np.abs(za - zb) > 1.0).mean()) < 0.01


def content_changed(prev_img: np.ndarray, cur_img: np.ndarray, grid: tuple[int, int] = (16, 9)) -> float:
    """Share of the screen whose picture changed, not just its brightness: a dimmed backdrop under a dialog keeps
    its content, a new slide does not."""
    a, k = small(prev_img)
    b, _ = small(cur_img)
    a, b = cv2.cvtColor(a, cv2.COLOR_BGR2GRAY).astype(np.float32), cv2.cvtColor(b, cv2.COLOR_BGR2GRAY).astype(np.float32)
    h, w = a.shape
    gx, gy = grid
    changed = 0
    for j in range(gy):
        for i in range(gx):
            pa = a[j * h // gy:(j + 1) * h // gy, i * w // gx:(i + 1) * w // gx]
            pb = b[j * h // gy:(j + 1) * h // gy, i * w // gx:(i + 1) * w // gx]
            fa, fb = pa.std() < 3, pb.std() < 3
            if fa and fb:
                continue
            if fa != fb or float(cv2.matchTemplate(pa, pb, cv2.TM_CCOEFF_NORMED)[0, 0]) < 0.8:
                changed += 1
    return changed / (gx * gy)


def moved_from(prev_img: np.ndarray, cur_img: np.ndarray, box: list[int]) -> tuple[int, int] | None:
    """Where the box content was in the previous frame, if it only moved (up to 400 px); (0, 0) - did not change."""
    cur = patch(cur_img, box)
    if cur is None:
        return None
    if alike(cur, patch(prev_img, box)):
        return (0, 0)
    if cur.std() < 3:
        return None
    x, y, w, h = box
    pad = 400
    y0, y1, x0, x1 = max(0, y - pad), min(prev_img.shape[0], y + h + pad), max(0, x - 60), min(prev_img.shape[1], x + w + 60)
    area = cv2.cvtColor(prev_img[y0:y1, x0:x1], cv2.COLOR_BGR2GRAY).astype(np.float32)
    if area.shape[0] < h or area.shape[1] < w:
        return None
    _, mx, _, loc = cv2.minMaxLoc(cv2.matchTemplate(area, cur, cv2.TM_CCOEFF_NORMED))
    dx, dy = x0 + loc[0] - x, y0 + loc[1] - y
    if mx <= 0.95 or (abs(dx) <= 2 and abs(dy) <= 2):
        return None  # nothing like it, or the same place: changed in place
    src = patch(prev_img, box, dx, dy)
    if not alike(cur, src) or alike(patch(cur_img, box, dx, dy), src):
        return None  # only similar, or the original is still where it was: a copy, not a move
    return dx, dy


def tap_mark(area: list[int], prev_img: np.ndarray, cur_img: np.ndarray) -> bool:
    """A touch indicator on a phone or tablet recording: a round mark about a fingertip wide. The change fills a disc
    and stays inside it, so a key popup, an icon or a word of the same size is not a tap."""
    side = min(REGION[2], REGION[3])
    x, y, w, h = area
    if not TOUCH:
        return False  # a desktop with no cursor found: no touch indicator to look for
    if not (0.05 * side <= w <= 0.12 * side and 0.8 <= w / max(h, 1) <= 1.25):
        return False
    a, b = (cv2.cvtColor(im[y:y + h, x:x + w], cv2.COLOR_BGR2GRAY).astype(int) for im in (prev_img, cur_img))
    if a.shape != b.shape or a.size == 0:
        return False
    d = np.abs(a - b) > 12
    yy, xx = np.mgrid[0:h, 0:w]
    disc = ((xx + 0.5 - w / 2) / (w / 2)) ** 2 + ((yy + 0.5 - h / 2) / (h / 2)) ** 2 <= 1
    return d[disc].mean() >= 0.45 and d[~disc].mean() <= 0.25


def shifted(prev: dict, cur: dict, box: list[int]) -> bool:
    """The container's texts are all in the previous state too, at another place: content moved, nothing changed.
    A text with the same pixels in the same place stayed, however OCR read it the two times ("prlvate", "private")."""
    mine = [c for c in cur["texts"] if inside(c["bbox"], box)]
    if not mine:
        return False
    moved = False
    for c in mine:
        if alike(patch(img(prev), c["bbox"]), patch(img(cur), c["bbox"])):
            continue
        ps = [p for p in prev["texts"] if same(p["text"], c["text"])]
        if not ps:
            return False
        p = min(ps, key=lambda p: abs(p["bbox"][0] - c["bbox"][0]) + abs(p["bbox"][1] - c["bbox"][1]))
        moved = moved or max(abs(p["bbox"][0] - c["bbox"][0]), abs(p["bbox"][1] - c["bbox"][1])) > 4
    return moved


def near_cursor(box: list[int], screens: tuple[dict, dict]) -> bool:
    pad = round(10 * (CURSOR_SCALE or 1))
    for s in screens:
        pos = cursor_at(key_ms(s))
        if pos and box[0] - pad <= pos[0] <= box[0] + box[2] + pad and box[1] - pad <= pos[1] <= box[1] + box[3] + pad:
            return True
    return False


# --- screen events ------------------------------------------------------------------------------------------------


def drop_covered(events: list[dict], screens: list[dict]) -> list[dict]:
    """At one moment, inside the box of something that went away or came up:
    - text that appears and was right there before that thing covered it: the list behind a closed dialog shows again;
    - text that goes away and shows up right there again once that thing is gone: a toast over a line.
    Neither changes the content. New text in the place of a closed menu (an attached file chip) is kept."""
    def at(t: int) -> dict | None:
        return next((s for s in screens if s["start_ms"] <= t < s["end_ms"]), None)

    def before_cover(cover: dict) -> dict | None:
        # the state right before the covering thing first showed: walk back while its own texts are there
        own = cover.get("members") or []
        i = next((i for i, s in enumerate(screens) if s["start_ms"] <= cover["t_ms"] - 1 < s["end_ms"]), None)
        while i is not None and i >= 0 and own and sum(still_there(m, screens[i]["texts"]) for m in own) * 2 >= len(own):
            i -= 1
        return screens[i] if i is not None and i >= 0 else None

    def all_there(e: dict, s: dict | None) -> bool:
        own = e.get("members") or []
        return bool(s and own and all(still_there(m, s["texts"]) for m in own))

    by_t: dict[int, list[dict]] = {}
    for e in events:
        by_t.setdefault(e["t_ms"], []).append(e)
    drop = set()
    for evs in by_t.values():
        for e in evs:
            if e["kind"] == "appear":
                for g in evs:
                    if g["kind"] == "disappear" and g.get("bbox") and inside(e["bbox"], g["bbox"]) and g["bbox"][2] * g["bbox"][3] > e["bbox"][2] * e["bbox"][3]:
                        if all_there(e, before_cover(g)):
                            drop.add(id(e))
            if e["kind"] == "disappear":
                for a in evs:
                    if a["kind"] == "appear" and a.get("bbox") and inside(e["bbox"], a["bbox"]) and a["bbox"][2] * a["bbox"][3] > e["bbox"][2] * e["bbox"][3]:
                        if a.get("end_ms") and all_there(e, at(a["end_ms"])):
                            drop.add(id(e))
    return [e for e in events if id(e) not in drop]


CLOCK = re.compile(r"\b\d{1,2}:\d{2}\b")


def drop_ticking(events: list[dict]) -> list[dict]:
    """A change where only a clock moved ("12:57" -> "13:00" in a meeting header) says nothing about the content."""
    return [e for e in events if not (e["kind"] == "text_change" and e.get("before") and e.get("after") and CLOCK.search(e["after"])
                                      and CLOCK.sub("#", norm(e["before"])) == CLOCK.sub("#", norm(e["after"])))]


def drop_meters(events: list[dict], duration_ms: int) -> list[dict]:
    """A text with digits that keeps changing in one place through the whole video (a menu bar clock with seconds, a
    network or CPU meter) is an indicator: dropped. A progress counter changes for a while, not all the video."""
    digits = lambda e: sum(ch.isdigit() for ch in (e.get("after") or e.get("text") or "")) >= 2
    tc = [e for e in events if e["kind"] == "text_change" and digits(e)]
    noisy: set[int] = set()
    for e in tc:
        same = [o for o in tc if iou(e["bbox"], o["bbox"]) > 0.5]
        if len(same) >= 5 and max(o["t_ms"] for o in same) - min(o["t_ms"] for o in same) >= 0.5 * duration_ms:
            noisy.update(id(o) for o in same)
    return [e for e in events if id(e) not in noisy]


def drop_noise(events: list[dict]) -> list[dict]:
    """Not facts of the screen: a tile lighting up among the participants (the speakers pass reads that), and one or two
    characters at the cursor while it moves (the arrow read as "4")."""
    def glyph(e):
        pos = cursor_at(e["t_ms"])
        x, y, w, h = e["bbox"]
        k = CURSOR_SCALE or 1
        return pos is not None and len(norm(e.get("text") or "")) <= 2 and w <= 45 * k and h <= 70 * k and x - 20 <= pos[0] <= x + w + 20 and y - 20 <= pos[1] <= y + h + 20
    return [e for e in events if not ((PEOPLE and e["kind"] == "visual_change" and inside(e["bbox"], PEOPLE))
                                      or (e["kind"] in ("appear", "disappear") and e.get("bbox") and glyph(e)))]


def drop_repeating(events: list[dict]) -> list[dict]:
    """A visual change that keeps coming back at one place is an indicator (the speaking tile, a blinking caret), not a
    fact about what happened."""
    vis = [e for e in events if e["kind"] == "visual_change"]
    noisy = {id(e) for e in vis if sum(iou(e["bbox"], o["bbox"]) > 0.7 for o in vis) >= 3}
    return [e for e in events if id(e) not in noisy]


def collapse_typing(events: list[dict]) -> list[dict]:
    """Text growing in one field over a few seconds ("di", "diego@f", "diego@fab") is one typing event."""
    out: list[dict] = []
    for e in events:
        if e["kind"] in ("appear", "text_change", "disappear") and e.get("bbox") and e.get("text"):
            run = next((o for o in reversed(out) if o["kind"] == "type" and iou(o["bbox"], e["bbox"]) > 0.6 and e["t_ms"] - o["end_ms"] <= 3000), None)
            if run and e["kind"] == "disappear":
                continue  # the field flickered empty between keystrokes
            if run and norm(e["text"]).startswith(norm(run["text"])[:2]):
                run.update(text=e["text"], end_ms=e["t_ms"], evidence=run["evidence"][:1] + e["evidence"][-1:])
                continue
            prev = next((o for o in reversed(out) if o.get("bbox") and iou(o["bbox"], e["bbox"]) > 0.6 and e["t_ms"] - o["t_ms"] <= 3000 and o["kind"] in ("appear", "text_change")), None)
            cur_text, prev_text = norm(e.get("after") or e["text"]), norm((prev or {}).get("after") or (prev or {}).get("text") or "")
            if prev and e["kind"] != "disappear" and len(prev_text) >= 1 and cur_text.startswith(prev_text) and len(cur_text) > len(prev_text):
                out.remove(prev)
                out.append({**prev, "kind": "type", "text": e.get("after") or e["text"], "end_ms": e["t_ms"], "evidence": prev["evidence"][:1] + e["evidence"][-1:]})
                continue
        out.append(e)
    return out


FIELD_GAP_MS = 6000
CARET = re.compile(r"\s*[|]+\s*$|(?<=[^\w\s])I$")


def field_edits(events: list[dict]) -> list[dict]:
    """Typing that OCR reads badly: one single-line field whose text keeps changing by a character or two, emptied in
    between ("1", "", "H", "M1", ";|") is one typing event with the values read, in order. A caret read as "|" at the
    end (or "I" after a symbol) is left out. Digits alone changing ("12%" -> "34%") is a counter, not typing."""
    def value(e):
        v = "" if e["kind"] == "disappear" else (e.get("after") if e["kind"] == "text_change" else e.get("text")) or ""
        return CARET.sub("", v).strip()

    small = lambda b: b[3] <= max(60, 0.05 * REGION[3]) and b[2] <= 0.6 * REGION[2]
    runs: list[dict] = []
    for e in events:
        if e["kind"] not in ("appear", "disappear", "text_change", "type") or not e.get("bbox") or not small(e["bbox"]) or len(value(e)) > 60:
            continue
        r = next((r for r in reversed(runs) if e["t_ms"] - r["t1"] <= FIELD_GAP_MS and iou(r["box"], e["bbox"]) > 0.5), None)
        if r is None:
            runs.append({"box": e["bbox"], "t1": e["t_ms"], "evs": [e]})
        else:
            r["evs"].append(e)
            r["t1"] = e["t_ms"]
    drop: set[int] = set()
    out = list(events)
    for r in runs:
        evs = r["evs"]
        first = evs[0].get("before") if evs[0]["kind"] == "text_change" else evs[0]["text"] if evs[0]["kind"] == "disappear" else ""
        vals = [CARET.sub("", first or "").strip()] + [value(e) for e in evs]
        vals = [v for i, v in enumerate(vals) if i == 0 or v != vals[i - 1]]
        filled = [v for v in vals if v]
        if len(evs) < 3 or len(vals) < 4 or len({re.sub(r"\d", "#", v) for v in filled}) < 2:
            continue
        if any(Levenshtein.distance(a, b) > 3 or same(a, b) and len(a) > 3 for a, b in zip(filled, filled[1:])):
            continue  # a long text read differently each time it shows (a key-cast overlay) is not typing
        drop.update(id(e) for e in evs)
        out.append({"t_ms": evs[0]["t_ms"], "end_ms": evs[-1]["t_ms"], "kind": "type", "bbox": union([e["bbox"] for e in evs]), "text": filled[-1],
                    "values": vals, "source": "ocr", "id": evs[0]["id"], "visible": True, "evidence": evs[0]["evidence"][:1] + evs[-1]["evidence"][-1:]})
    return sorted((e for e in out if id(e) not in drop), key=lambda e: e["t_ms"])


def off_cursor(screen: dict) -> dict:
    """Texts of a state without the arrow itself, which OCR may read as a character ("4") where the cursor rests."""
    pos = cursor_at(key_ms(screen))
    if pos is None:
        return screen
    on = lambda b: b[0] <= pos[0] <= b[0] + b[2] and b[1] <= pos[1] <= b[1] + b[3]
    return {**screen, "texts": [t for t in screen["texts"] if not (len(norm(t["text"])) <= 2 and on(t["bbox"]))]}


def edges(box: list[int]) -> list[str] | None:
    """The right or bottom screen edge a new element of three lines or more reaches: a menu running into it may be cut
    off there (bars and notifications sit at the top). Something that spans the screen (a page, a panel) says nothing."""
    x0, y0, W, H = REGION
    x, y, w, h = box
    if w * h > 0.5 * W * H or w >= 0.9 * W or h >= 0.9 * H:
        return None
    hit = [n for n, ok in (("right", x + w >= x0 + W - 2), ("bottom", y + h >= y0 + H - 2)) if ok]
    return hit or None


def beside(screen: dict, box: list[int]) -> str | None:
    """The text on the same line right next to a small box with no text of its own: where a typed symbol OCR does not
    read went ('right of "return zero, key)"')."""
    x, y, w, h = box
    if w > 3 * h:
        return None
    best = None
    for t in screen["texts"]:
        bx, by, bw, bh = t["bbox"]
        if not y <= by + bh / 2 <= y + h or bh < 0.3 * h:
            continue
        gap = x - (bx + bw) if bx + bw <= x + w / 2 else bx - (x + w)
        if -w <= gap <= 2 * h and (best is None or gap < best[0]):
            best = (gap, t["text"], "right of" if bx + bw <= x + w / 2 else "left of")
    return best and f'{best[2]} "{best[1]}"'


def diff(screens: list[dict]) -> list[dict]:
    global TOUCH
    TOUCH = touch_screen(screens, REGION, CURSOR_SCALE)
    events = []
    screens = [off_cursor(s) for s in screens]

    def add(**e):
        e["id"] = f"p{len(events) + 1:03d}"
        e.setdefault("end_ms", None)
        e.setdefault("source", "ocr")
        e["visible"] = True
        events.append(e)

    for prev, cur in zip(screens, screens[1:]):
        t = cur["start_ms"]
        ev = [prev["frame"], cur["frame"]]
        added, removed = match_texts(prev["texts"], cur["texts"])
        cur_img, prev_img = img(cur), img(prev)
        areas = changed_areas(prev, cur)
        # another window came to the front
        fp, fc = front_window(prev_img, prev["texts"]), front_window(cur_img, cur["texts"])
        title_rows = [w["y"] for w in (fp, fc) if w]
        if fc and (not fp or not same(fp["title"], fc["title"]) or abs(fp["bbox"][0] - fc["bbox"][0]) > 20):
            add(t_ms=t, kind="window_change", bbox=fc["bbox"], text=fc["title"], before=fp and fp["title"], evidence=ev)
        churn = len(added) + len(removed)
        pp, pc = page_of(prev["texts"]), page_of(cur["texts"])
        new_slide = bool(pp and pc and pp[0] != pc[0])
        if new_slide or churn > 6 and (len(added) > SCREEN_CHANGE * max(len(cur["texts"]), 1) or content_changed(prev_img, cur_img) > SCREEN_AREA):
            add(t_ms=t, kind="screen_change", bbox=union(areas) if areas else None, text=reading(added), before=reading(removed), evidence=ev)
            continue
        # OCR read the same pixels differently (a dimmed backdrop, compression): not a change
        added = [c for c in added if moved_from(prev_img, cur_img, c["bbox"]) is None]
        removed = [p for p in removed if not alike(patch(prev_img, p["bbox"]), patch(cur_img, p["bbox"]))]
        # the cursor over a text makes OCR read it differently ("Delivered" -> "Delivered Li"): not a change
        boxes_c = [b for b in (cursor_box(cursor_at(key_ms(prev))), cursor_box(cursor_at(key_ms(cur)))) if b]
        under_cursor = lambda t: any(iou(t["bbox"], b) > 0 or inside(b, t["bbox"]) for b in boxes_c)
        garbled = [(c, p) for c in added for p in removed if iou(c["bbox"], p["bbox"]) > 0.3 and (under_cursor(c) or under_cursor(p)) and fuzz.ratio(norm(c["text"]), norm(p["text"])) >= 60]
        added = [c for c in added if not any(c is a for a, _ in garbled)]
        removed = [p for p in removed if not any(p is b for _, b in garbled)]
        # a text cut by the edge of something on top of it ("Supply_Agreement.docx" -> "Supply"): covered, not changed
        cut_pairs = [(c, p) for c in added for p in removed if abs(c["bbox"][0] - p["bbox"][0]) <= 6 and abs(c["bbox"][1] - p["bbox"][1]) <= 6 and (norm(p["text"]).startswith(norm(c["text"])) or norm(c["text"]).startswith(norm(p["text"])))]
        added = [c for c in added if not any(c is a for a, _ in cut_pairs)]
        removed = [p for p in removed if not any(p is b for _, b in cut_pairs)]
        used_removed: set[int] = set()
        boxes: list[list[int]] = []
        for box, ts in group(added, cur_img, [c for c in cur["texts"] if not any(c is a for a in added)]):
            boxes.append(box)
            # the same container held other text before: the text changed in place
            before = [p for p in removed if inside(p["bbox"], box, 4) and id(p) not in used_removed]
            members = [c for c in cur["texts"] if inside(c["bbox"], box)] if box not in (t_["bbox"] for t_ in ts) else ts
            if before and similarity(patch(prev_img, box), patch(cur_img, box)) < 0.4:
                used_removed.update(id(p) for p in before)  # a new element covers what was there
                before = []
            if before:
                used_removed.update(id(p) for p in before)
                add(t_ms=t, kind="text_change", bbox=box, text=reading(members), before=reading(before), after=reading(ts), evidence=ev)
            else:
                add(t_ms=t, kind="appear", bbox=box, text=reading(members), members=ts, evidence=ev)
        gone = [p for p in removed if id(p) not in used_removed]
        for box, ts in group(gone, prev_img, [p for p in prev["texts"] if not any(p is g for g in gone)]):
            if moved_from(cur_img, prev_img, box) is not None:  # the whole container is still there, moved
                continue
            boxes.append(box)
            add(t_ms=t, kind="disappear", bbox=box, text=reading(ts), members=ts, evidence=ev)
        # pixels changed where no text changed: an icon, a status mark, a colour. Not counted: content that only moved,
        # hover and press feedback under the cursor, title bars (the window change above), large areas (a dimmed backdrop)
        text_boxes = [x["bbox"] for x in added + removed]
        limit = MAX_CONTAINER * REGION[2] * REGION[3]
        for area in areas:
            if CURSOR_SCALE is None and tap_mark(area, prev_img, cur_img):
                cx, cy = area[0] + area[2] // 2, area[1] + area[3] // 2
                if not any(abs(e["at"][0] - cx) < 30 and abs(e["at"][1] - cy) < 30 and t - e["t_ms"] < 1500 for e in events if e["kind"] == "click"):
                    target = under_before(screens, prev["start_ms"], cx, cy, 1.0)
                    add(t_ms=t, kind="click", bbox=target["bbox"] if target else area, at=[cx, cy], text=target and target["text"], source="touch", evidence=ev)
                continue
            if any(iou(area, b) > 0 or inside(b, area) for b in text_boxes) or area[2] * area[3] > limit:
                continue
            if any(area[1] - 20 <= y <= area[1] + area[3] + 20 for y in title_rows):
                continue
            box = container(cur_img, area)
            # only a real move counts here: a colour change (a selected row) is "the same picture" up to brightness
            moved = [m for m in (moved_from(prev_img, cur_img, box), moved_from(cur_img, prev_img, area)) if m is not None and m != (0, 0)]
            if shifted(prev, cur, box) or moved:
                continue
            if near_cursor(box, (prev, cur)):
                # hover or press feedback: not a fact by itself, but it tells a click (see cursor_events), then dropped
                add(t_ms=t, kind="visual_change", bbox=box, text="", source="pixel", under_cursor=True, evidence=ev, look=look(prev_img, cur_img, box))
                continue
            if any(iou(box, b) > 0.3 or inside(box, b) or inside(b, box) for b in boxes):
                continue  # part of an element that appeared or changed at the same moment
            boxes.append(box)
            members = [c for c in cur["texts"] if inside(c["bbox"], box)]
            add(t_ms=t, kind="visual_change", bbox=box, text=reading(members), source="pixel", evidence=ev, look=look(prev_img, cur_img, box))

    events = field_edits(collapse_typing(drop_repeating(drop_noise(drop_meters(drop_ticking(events), screens[-1]["end_ms"])))))

    # how long an appeared element was shown: until the first state where most of its own text is gone
    for e in events:
        if e["kind"] != "appear":
            continue
        own = e["members"]
        for s in screens:
            if s["start_ms"] <= e["t_ms"]:
                continue
            left = sum(still_there(m, s["texts"]) for m in own)
            if left * 2 < len(own) or (len(own) == 1 and not left):
                e["end_ms"] = s["start_ms"]
                break
    events = drop_covered(events, screens)
    for e in events:
        if e["kind"] in ("appear", "screen_change") and e.get("bbox") and (e.get("text") or "").count(" | ") >= 2:
            e["edge"] = edges(e["bbox"])
        if e["kind"] == "visual_change" and not e.get("text") and not e.get("under_cursor"):
            s = next((s for s in screens if s["start_ms"] == e["t_ms"]), None)
            e["beside"] = s and beside(s, e["bbox"])
    raised = {e["t_ms"] for e in events if e["kind"] == "window_change"}
    events = [e for e in events if not (e["kind"] == "disappear" and e["t_ms"] in raised)]  # went behind the window
    for e in events:
        e.pop("members", None)
    return events


# --- cursor events ------------------------------------------------------------------------------------------------

CLICK_WITHIN_MS = 700  # the screen changed this soon after the cursor stopped
CLICK_AFTER_REST_MS = 5000  # or later, if what changed is right under the cursor
FAST = 12  # px per frame of a 1080p frame (times the cursor scale): faster is a move from one place to another
HOVER_PATH = 12  # px the cursor travels while staying over one thing
STILL_MS = 100  # no movement this long: the cursor stopped (a click can follow)
WIGGLE_GAP_MS = 250  # a hovering hand stops for a moment where it turns back
JUMP = 40  # px per frame: surely a move to somewhere else
HOVER_MS = 200


def wiggles(track: list[list], scale: float) -> list[dict]:
    """Hover episodes. The track is cut by pauses (WIGGLE_GAP_MS) and jumps (JUMP px per frame); in each piece the
    approach ends when the speed falls to a quarter of its peak, and what follows is a hover if the cursor keeps
    moving around one place - its path much longer than how far it got from where it settled."""
    frame = 1000 / 30  # speeds in px per 1/30 s, whatever the frame rate
    pts = [p for p in track if p[1] is not None]

    def speed(q, p):
        return ((p[1] - q[1]) ** 2 + (p[2] - q[2]) ** 2) ** 0.5 / max(1.0, (p[0] - q[0]) / frame)

    pieces, cur = [], []
    for p in pts:
        if cur and (p[0] - cur[-1][0] >= WIGGLE_GAP_MS or speed(cur[-1], p) > JUMP * scale):
            pieces.append(cur)
            cur = []
        cur.append(p)
    if cur:
        pieces.append(cur)
    out = []
    for ep in pieces:
        sp = [speed(a, b) for a, b in zip(ep, ep[1:])]
        if not sp:
            continue
        peak = max(range(len(sp)), key=lambda i: sp[i])
        start = 0
        if sp[peak] >= 4 * scale:
            start = next((i + 1 for i in range(peak, len(sp)) if sp[i] < 0.25 * sp[peak]), len(ep) - 1)
        ep = ep[start:]
        if len(ep) < 3:
            continue
        path = sum(((b[1] - a[1]) ** 2 + (b[2] - a[2]) ** 2) ** 0.5 for a, b in zip(ep, ep[1:]))
        net = ((ep[-1][1] - ep[0][1]) ** 2 + (ep[-1][2] - ep[0][2]) ** 2) ** 0.5
        if ep[-1][0] - ep[0][0] >= HOVER_MS and path >= HOVER_PATH * scale and path >= 1.8 * net:
            out.append({"start_ms": ep[0][0], "end_ms": ep[-1][0], "x": ep[0][1], "y": ep[0][2], "pts": ep})
    return out


def under_before(screens: list[dict], t: int, x: int, y: int, scale: float, back_ms: int = 1500) -> dict | None:
    """The text under a point at t, or in a state shortly before: the cursor or a touch mark may hide it from OCR."""
    for s in sorted((s for s in screens if s["start_ms"] <= t and s["end_ms"] >= t - back_ms), key=lambda s: -s["start_ms"]):
        u = under(s, x, y, scale)
        if u:
            return u
    return None


def under(screen: dict | None, x: int, y: int, scale: float) -> dict | None:
    """The text under or right next to the cursor tip."""
    if not screen:
        return None
    pad = round(12 * scale)
    best = None
    for t in screen["texts"]:
        bx, by, bw, bh = t["bbox"]
        if bx - pad <= x <= bx + bw + pad and by - pad <= y <= by + bh + pad:
            d = abs(x - (bx + bw / 2)) / max(bw, 1) + abs(y - (by + bh / 2)) / max(bh, 1)
            if best is None or d < best[0]:
                best = (d, t)
    return best and best[1]


def hover_looks(cursor_evs: list[dict], screen_events: list[dict]) -> None:
    """A hover keeps what it did to the element under it (the icon faded, the row got lighter): the feedback itself is
    dropped as a screen event, but how it looks can be the bug."""
    for h in cursor_evs:
        if h["kind"] != "point":
            continue
        x, y = h["at"]
        near = [e for e in screen_events if e["kind"] == "visual_change" and e.get("look")
                and h["t_ms"] - 300 <= e["t_ms"] <= (h["end_ms"] or h["t_ms"]) + 300 and inside([x, y, 0, 0], e["bbox"], 12)]
        words = [w for w in (look_words(e["look"]) for e in near) if w]
        if words:
            h["reaction"] = max(words, key=len)


def drop_under_hover(screen_events: list[dict], cursor_evs: list[dict], track: list[list]) -> list[dict]:
    """While the cursor wiggles over something, OCR and pixels along its path flicker ("Delivered" -> "Delivered Li"):
    small changes on that path during a hover are the cursor, not the screen."""
    pad = 40 * (CURSOR_SCALE or 1)
    zones = []
    for h in cursor_evs:
        if h["kind"] != "point":
            continue
        pts = [p for p in track if p[1] is not None and h["t_ms"] <= p[0] <= (h["end_ms"] or h["t_ms"])]
        if pts:
            xs, ys = [p[1] for p in pts], [p[2] for p in pts]
            zones.append((h["t_ms"], (h["end_ms"] or h["t_ms"]) + 400, min(xs) - pad, min(ys) - pad, max(xs) + pad, max(ys) + pad))
    def hit(e):
        b = e.get("bbox")
        if not b or e["kind"] not in ("appear", "disappear", "visual_change", "text_change") or b[2] * b[3] > MAX_CONTAINER * REGION[2] * REGION[3]:
            return False
        return any(t0 <= e["t_ms"] <= t1 and b[0] < x1 and x0 < b[0] + b[2] and b[1] < y1 and y0 < b[1] + b[3] for t0, t1, x0, y0, x1, y1 in zones)
    return [e for e in screen_events if not hit(e)]


def cursor_events(track: list[list], scale: float | None, screens: list[dict], screen_events: list[dict], duration_ms: int) -> list[dict]:
    if not scale or not track:
        return []
    out = []
    changes = sorted({e["t_ms"] for e in screen_events if not e.get("under_cursor")})
    by_t: dict[int, list[dict]] = {}
    for e in screen_events:
        if not e.get("under_cursor"):
            by_t.setdefault(e["t_ms"], []).append(e)

    def reaction(c: int, x: int, y: int) -> bool:
        """Something only went away (a toast timing out) - a click only if the cursor was on it (OK on a dialog)."""
        evs = by_t.get(c, [])
        if evs and all(e["kind"] == "disappear" for e in evs):
            pad = 20 * scale
            return any(e.get("bbox") and e["bbox"][0] - pad <= x <= e["bbox"][0] + e["bbox"][2] + pad and e["bbox"][1] - pad <= y <= e["bbox"][1] + e["bbox"][3] + pad for e in evs)
        return True

    def state_at(t: int):
        return next((s for s in screens if s["start_ms"] <= t < s["end_ms"]), None)

    # a click: the cursor stopped, and the screen changed soon after, with the cursor still not moving
    pts = track
    # rests: runs of steps of at most 2 px (an eased stop creeps by a pixel a frame) lasting STILL_MS
    stills = []
    i = 0
    while i < len(pts):
        if pts[i][1] is None:  # the cursor was lost: no rest through that
            i += 1
            continue
        j = i
        while j + 1 < len(pts) and pts[j + 1][1] is not None and max(abs(pts[j + 1][1] - pts[j][1]), abs(pts[j + 1][2] - pts[j][2])) <= 2 * scale:
            j += 1
        t_next = pts[j + 1][0] if j + 1 < len(pts) else duration_ms
        if t_next - pts[i][0] >= STILL_MS:
            stills.append((pts[i][0], pts[j][1], pts[j][2], t_next))
        i = j + 1
    clicked: list[int] = []
    for t0, x, y, t_next in stills:
        click_t = next((c for c in changes if t0 <= c <= min(t_next, t0 + CLICK_WITHIN_MS) and reaction(c, x, y)), None)
        if click_t is None:
            # after a longer rest: only a change right under the cursor (the control itself reacted)
            pad = 30 * scale
            # (feedback under a cursor that has been still a while is a press; a hover lights up when the cursor arrives)
            local = [e for e in screen_events if e["kind"] in ("appear", "text_change", "visual_change") and e.get("bbox") and e["bbox"][2] * e["bbox"][3] <= MAX_DIALOG * REGION[2] * REGION[3]
                     and not (e.get("under_cursor") and e["t_ms"] < t0 + STILL_MS)]
            click_t = next((e["t_ms"] for e in local if t0 <= e["t_ms"] <= min(t_next, t0 + CLICK_AFTER_REST_MS)
                            and e["bbox"][0] - pad <= x <= e["bbox"][0] + e["bbox"][2] + pad and e["bbox"][1] - pad <= y <= e["bbox"][1] + e["bbox"][3] + pad), None)
        if click_t is None:
            continue
        target = under_before(screens, t0, x, y, scale)
        # the press is right before the screen reacts; the cursor may have rested a while before it
        t_click = max(t0, click_t - round(1000 / FPS))
        out.append({"t_ms": t_click, "kind": "click", "bbox": target["bbox"] if target else [x - 4, y - 4, 8, 8], "at": [x, y], "text": target and target["text"], "source": "cursor", "stopped_at": t0, "cursor": shape_at(t_click)})
        clicked.append(t0)

    for r in wiggles(track, scale):
        t0 = r["start_ms"]
        tip = [r["x"] - 4, r["y"] - 4, 8, 8]
        # where it hovered: the text under most of the wiggle
        hits: dict[str, list] = {}
        shapes: dict[str | None, int] = {}
        for p in r["pts"]:
            u = under(state_at(t0), p[1], p[2], scale)
            if u:
                hits.setdefault(u["text"], [u, 0])[1] += 1
            k = p[3] if len(p) > 3 else None
            shapes[k] = shapes.get(k, 0) + 1
        u = max(hits.values(), key=lambda h: h[1])[0] if hits else None
        out.append({"t_ms": t0, "end_ms": r["end_ms"], "kind": "point", "bbox": u["bbox"] if u else tip, "at": [r["x"], r["y"]], "text": u and u["text"], "source": "cursor", "cursor": max(shapes, key=shapes.get)})
    for e in out:
        e.setdefault("end_ms", None)
        e.update(visible=True, evidence=[])
    return out


# --- motion events ------------------------------------------------------------------------------------------------

MOVE_MIN = 6  # px of the largest displacement (more on a large screen)
MOVE_PX = 150  # changed px of the small frame the moves explain, over the whole episode
SCROLL_AREA = 0.25  # share of the screen: content this large moving up or down was scrolled
JOIN_MS = 400  # moves of one thing this close in time are one episode (a drag that lags, wheel notches)


def touches(a: list[int], b: list[int], pad: int = 20) -> bool:
    return a[0] - pad < b[0] + b[2] and b[0] < a[0] + a[2] + pad and a[1] - pad < b[1] + b[3] and b[1] < a[1] + a[3] + pad


def episodes(moves: list[list]) -> list[dict]:
    """Frame moves -> episodes: the same area moving again within JOIN_MS; one step per frame, the largest move."""
    eps: list[dict] = []
    for t, x, y, w, h, dx, dy, px in sorted(moves, key=lambda m: (m[0], -m[7])):
        box = [x, y, w, h]
        ep = next((e for e in reversed(eps) if 0 < t - e["t1"] <= JOIN_MS and touches(e["last"], box)), None)
        if ep is None:
            if any(e["t1"] == t and touches(e["last"], box) for e in eps):
                continue  # a smaller piece of a move already taken in this frame
            ep = {"t0": t, "box": box, "first": box, "steps": []}
            eps.append(ep)
        ep["steps"].append((t, dx, dy, px))
        ep.setdefault("sizes", []).append((w, h))
        ep.update(t1=t, last=box, box=union([ep["box"], box]))
    return eps


def way(dx: int, dy: int) -> str:
    parts = [f"{abs(dx)} px {'right' if dx > 0 else 'left'}" if abs(dx) >= 3 else "", f"{abs(dy)} px {'down' if dy > 0 else 'up'}" if abs(dy) >= 3 else ""]
    return " and ".join(p for p in parts if p) or "a few px"


def follows(dx: int, dy: int, cx: int, cy: int) -> bool:
    """The cursor moved along with the content: its step along the move is about as long (a slider thumb follows
    only the horizontal part)."""
    d = (dx * dx + dy * dy) ** 0.5
    along = (cx * dx + cy * dy) / d if d else 0
    return 0.6 * d - 3 <= along <= 1.6 * d + 3 and along >= 2


def companion(eps: list[dict]) -> tuple[int, int] | None:
    """A cursor highlight drawn by the recorder (a halo around the arrow): one size of thing following the cursor all
    over the screen, in many episodes. -> its (w, h), or None. A slider thumb follows it too, but along one line."""
    fol = [e for e in eps if e["follow"] >= 0.3 * len(e["steps"]) and e["size"][0] * e["size"][1] < 0.02 * REGION[2] * REGION[3]]
    for e in fol:
        w, h = e["size"]
        same = [o for o in fol if abs(o["size"][0] - w) <= 0.25 * w and abs(o["size"][1] - h) <= 0.25 * h]
        xs = [o["box"][0] + o["box"][2] / 2 for o in same]
        ys = [o["box"][1] + o["box"][3] / 2 for o in same]
        if len(same) >= 5 and max(xs) - min(xs) >= 0.25 * REGION[2] and max(ys) - min(ys) >= 0.25 * REGION[3]:
            return w, h
    return None


def motion_events(motion: dict, screens: list[dict], screen_events: list[dict]) -> list[dict]:
    """Moves, scrolls and drags from the frame moves. A move that ends where it started is said so ("21 px right and
    back 33 ms later"); content that follows the cursor is a drag, with what changed after the drop. Content sliding
    in or out as it appears or goes is the appearing, not a move."""
    frame = 1000 / motion["fps"]
    side = max(REGION[2], REGION[3])
    least = max(MOVE_MIN, round(0.005 * side))
    pad = 30 * (CURSOR_SCALE or 1)
    shown = [e for e in screen_events if e["kind"] in ("appear", "disappear", "screen_change") and e.get("bbox")]

    def state_at(t: int) -> dict | None:
        return next((s for s in screens if s["start_ms"] <= t < s["end_ms"]), None)

    def before(t: int) -> dict | None:
        return next((s for s in reversed(screens) if s["start_ms"] < t), None)

    eps = []
    for ep in episodes(motion["moves"]):
        cum, path = [0, 0], []
        for _, dx, dy, _ in ep["steps"]:
            cum = [cum[0] + dx, cum[1] + dy]
            path.append(cum)
        ep["path"] = path
        ep["size"] = tuple(int(np.median([z[i] for z in ep["sizes"]])) for i in (0, 1))
        ep["peak_i"] = max(range(len(path)), key=lambda i: path[i][0] ** 2 + path[i][1] ** 2)
        peak = path[ep["peak_i"]]
        if (peak[0] ** 2 + peak[1] ** 2) ** 0.5 < least or sum(s[3] for s in ep["steps"]) < MOVE_PX:
            continue
        box = ep["box"]
        if any(e["t_ms"] - 400 <= ep["t1"] and ep["t0"] <= e["t_ms"] + 400 and inside(box, e["bbox"]) and e["bbox"][2] * e["bbox"][3] >= 0.5 * box[2] * box[3] for e in shown):
            continue
        ep["follow"] = 0
        if CURSOR_SCALE:
            for t, dx, dy, _ in ep["steps"]:
                a, b = cursor_at(round(t - frame)), cursor_at(t)
                if a and b and follows(dx, dy, b[0] - a[0], b[1] - a[1]) and touches(box, [b[0], b[1], 0, 0], pad):
                    ep["follow"] += 1
        eps.append(ep)
    halo = companion(eps)
    out = []
    for ep in eps:
        box, path, peak_i = ep["box"], ep["path"], ep["peak_i"]
        if halo and sum(abs(w - halo[0]) <= 0.3 * halo[0] and abs(h - halo[1]) <= 0.3 * halo[1] for w, h in ep["sizes"]) >= 0.5 * len(ep["sizes"]):
            continue
        peak, net = path[peak_i], path[-1]
        size = (peak[0] ** 2 + peak[1] ** 2) ** 0.5
        back = len(path) > 1 and (net[0] ** 2 + net[1] ** 2) ** 0.5 <= max(3, 0.25 * size)
        s0 = before(ep["t0"])
        texts = [t for t in (s0["texts"] if s0 else []) if inside(t["bbox"], box)]
        e = {"t_ms": ep["t0"], "end_ms": ep["t1"], "bbox": box, "text": reading(texts)[:200], "dx": net[0], "dy": net[1],
             "peak": peak, "back": back, "frames": len(path), "source": "pixel",
             "evidence": [x["frame"] for x in (s0, state_at(ep["t1"] + 1)) if x and x.get("frame")]}
        if back:
            e["back_ms"] = ep["t1"] - ep["steps"][peak_i][0]
        if len(path) >= 2 and ep["follow"] >= 0.5 * len(path):
            e["kind"] = "drag"
            start, end = cursor_at(round(ep["t0"] - frame)), cursor_at(ep["t1"])
            e["at"], e["to"] = list(start) if start else None, list(end) if end else None
            if start and s0:
                own = [t for t in s0["texts"] if inside(t["bbox"], ep["first"], 4)]
                what = min(own, key=lambda t: abs(t["bbox"][0] + t["bbox"][2] / 2 - start[0]) + abs(t["bbox"][1] + t["bbox"][3] / 2 - start[1]), default=None)
                e["text"] = (what or under(s0, start[0], start[1], CURSOR_SCALE) or {"text": ""})["text"]
            onto = end and under(s0, end[0], end[1], CURSOR_SCALE)
            e["onto"] = onto and onto["text"]
        elif box[2] * box[3] >= SCROLL_AREA * REGION[2] * REGION[3] and abs(peak[1]) >= 2 * abs(peak[0]):
            e["kind"] = "scroll"
        else:
            e["kind"] = "move"
        out.append(e)
    for e in out:
        if e["kind"] == "drag":
            after = [x for x in screen_events + out if x is not e and e["end_ms"] < x["t_ms"] <= e["end_ms"] + 1500 and x["kind"] not in ("click", "point") and not x.get("under_cursor")]
            e["after"] = "; ".join(f'{x["kind"]} "{(x.get("text") or "")[:60]}"' for x in after[:3])
        e["visible"] = True
    return out


FLICKER_BACK_MS = 400  # a look coming back this soon is a toggle, not a slow change (a caret blinks every 0.5 s)
FLICKER_GAP_MS = 700
FLICKER_MIN = 4  # toggles


def flicker_events(motion: dict, screens: list[dict]) -> list[dict]:
    """One place going back to how it looked a moment ago, again and again: one event with the count and the span.
    The cursor switching between two shapes the same way, some of the times while not moving, is one too (from the
    tracked shapes)."""
    k = CURSOR_SCALE or 1
    runs: list[dict] = []
    for t, x, y, w, h, back in motion["changes"]:
        if not 0 < back <= FLICKER_BACK_MS or min(w, h) < 6 * k:
            continue
        box = [x, y, w, h]
        r = next((r for r in reversed(runs) if t - r["t1"] <= FLICKER_GAP_MS and (iou(r["box"], box) > 0.3 or inside(box, r["box"]) or inside(r["box"], box))), None)
        if r is None:
            runs.append({"t0": t, "t1": t, "box": box, "n": 1})
            continue
        if t != r["t1"]:
            r["n"] += 1
        r.update(t1=t, box=union([r["box"], box]))
    out = []
    for r in runs:
        if r["n"] < FLICKER_MIN or r["box"][2] * r["box"][3] > MAX_DIALOG * REGION[2] * REGION[3]:
            continue
        s = next((s for s in reversed(screens) if s["start_ms"] <= r["t0"]), None)
        texts = [t for t in (s["texts"] if s else []) if inside(t["bbox"], r["box"])]
        out.append({"t_ms": r["t0"], "end_ms": r["t1"], "kind": "flicker", "bbox": r["box"], "text": reading(texts)[:200], "count": r["n"],
                    "source": "pixel", "evidence": [s["frame"]] if s and s.get("frame") else []})
    pts = [p for p in TRACK if p[1] is not None and len(p) > 3 and p[3]]
    flips = [(a[3], b) for a, b in zip(pts, pts[1:]) if b[3] != a[3]]
    groups: list[list] = []
    for f in flips:
        if groups and f[1][0] - groups[-1][-1][1][0] <= FLICKER_GAP_MS:
            groups[-1].append(f)
        else:
            groups.append([f])
    for g in groups:
        run = [b for _, b in g]
        seen = [g[0][0]] + [b[3] for b in run]
        kinds = sorted(set(seen), key=lambda x: -seen.count(x))
        if len(g) < 2 * FLICKER_MIN or sum(seen.count(x) for x in kinds[:2]) < 0.8 * len(seen):
            continue
        still = sum(abs(q[1] - p[1]) + abs(q[2] - p[2]) <= 4 * k for p, q in zip(run, run[1:]))
        if still < 3:
            continue  # moving over text and links changes the shape by itself
        out.append({"t_ms": run[0][0], "end_ms": run[-1][0], "kind": "flicker", "bbox": union([[p[1] - 4, p[2] - 4, 8, 8] for p in run]),
                    "text": "", "count": len(run), "cursor": kinds[:2], "still": still, "source": "cursor", "evidence": []})
    for e in out:
        e["visible"] = True
    return out


def jumps(screen_events: list[dict]) -> list[dict]:
    """A menu that jumps far away at once: at one moment its lines go away in one place and come up in another. The
    lines that went are explained by the move: one move event (the jump) instead of their disappearing."""
    out, gone = [], set()
    by_t: dict[int, list[dict]] = {}
    for e in screen_events:
        by_t.setdefault(e["t_ms"], []).append(e)
    for t, evs in by_t.items():
        for a in (e for e in evs if e["kind"] == "appear" and e.get("bbox") and e.get("text")):
            lines = [norm(x) for x in a["text"].split(" | ")]
            gone_here = [d for d in evs if d["kind"] == "disappear" and d.get("bbox") and d.get("text") and id(d) not in gone and not inside(d["bbox"], a["bbox"])]
            went_lines = [norm(x) for d in gone_here for x in d["text"].split(" | ")]
            went = [d for d in gone_here if any(fuzz.ratio(norm(x), ln) >= 80 for x in d["text"].split(" | ") for ln in lines)]
            kept = sum(any(fuzz.ratio(ln, w) >= 80 for w in went_lines) for ln in lines)
            # most lines of the new element, three or more, were there a moment ago: a file picked from a list and
            # shown in a chat is not the list moving (the new menu may show fewer lines: cut off by the screen edge)
            if kept < 3 or kept < 0.6 * len(lines):
                continue
            src = union([d["bbox"] for d in went])
            gone.update(id(d) for d in went)
            dx, dy = a["bbox"][0] - src[0], a["bbox"][1] - src[1]
            out.append({"t_ms": t, "end_ms": t, "kind": "move", "bbox": a["bbox"], "from": src, "text": a["text"], "dx": dx, "dy": dy, "peak": [dx, dy],
                        "back": False, "frames": 1, "source": "ocr", "visible": True, "evidence": a.get("evidence", [])})
    return [e for e in screen_events if id(e) not in gone] + out


def drop_flickering(screen_events: list[dict], flickers: list[dict]) -> list[dict]:
    """Events at a flickering place during the flicker are its toggles: the flicker event says it once."""
    def hit(e):
        b = e.get("bbox")
        return b and e["kind"] in ("appear", "disappear", "visual_change", "text_change") and any(
            f["source"] == "pixel" and f["t_ms"] - 100 <= e["t_ms"] <= f["end_ms"] + 100 and (inside(b, f["bbox"]) or iou(b, f["bbox"]) > 0.3) for f in flickers)
    return [e for e in screen_events if not hit(e)]
