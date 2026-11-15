"""Checks across passes: facts that show only when speech, screen and windows are put side by side.

- unmentioned: an error text appeared on the screen and nobody said anything like it;
- revert: a value went back to what it was a moment ago with no click before it;
- covered: something changed in a window partly covered by the front one;
- claim: a statement about the past, other places, other people's words or a guess, with nothing on screen showing it.
No model: word lists, event history, title-bar buttons.
"""
import re
from pathlib import Path

import cv2
import numpy as np
from rapidfuzz import fuzz

ERROR = {
    "en": r"\b(errors?|fail(ed|ure|s)?|couldn'?t|could not|can'?t|cannot|unable|unavailable|not (sent|delivered|found|allowed)|denied|forbidden|block(s|ed)|no access|won'?t open)\b",
    "ru": r"(ошибк|не удалось|не отправлен|не доставлен|недоступ|запрещ|заблокир|отказ|нет доступа|не открыва)",
}
CLAIM = {
    "en": [
        r"\b(maybe|perhaps|probably|i think|i guess|i suppose|must be|might be)\b",
        r"\b(used to|normally|usually|always|every (other )?time|already (checked|tried))\b",
        r"\bbefore\b(?!\s+\w)",
        r"\bon (the|my|his|her|their|a) (computer|laptop|desktop|phone|mac|pc|browser)\b",
        r"\b(he|she|they) (says|said|writes|wrote)\b|\b(says|said|writes|wrote),? (he|she|they)\b|\b\w+ (says|writes|said|wrote) that\b",
    ],
    "ru": [
        r"(может быть|может,|наверное|возможно|кажется|по-моему|видимо|должно быть)",
        r"(раньше|обычно|всегда|каждый (второй )?раз|через раз|уже проверял|уже пробовал)",
        r"(с компьютера|на компьютере|с ноутбука|с телефона)",
        r"((он|она|они) (говорит|пишет|сказал|написал)|(говорит|пишет), что)",
    ],
}
STOP = {"that", "this", "there", "here", "what", "with", "from", "have", "just", "says", "said", "writes", "wrote", "they", "their",
        "then", "it's", "okay", "well", "like", "some", "the", "and", "but", "was", "were", "maybe", "think", "guess", "probably"}
NEAR_SPEECH_MS = (3000, 12000)  # an error counts as mentioned if words like it are said this long before / after it
REVERT_MS = 15000


def norm(s: str) -> str:
    return (s or "").lower().replace("’", "'").replace("ё", "е")


def words(s: str) -> list[str]:
    return [w for w in re.findall(r"[\w']+", norm(s)) if len(w.strip("'")) >= 4 and w not in STOP and not w.isdigit()]


def shares(a: list[str], b: list[str]) -> int:
    return sum(1 for w in set(a) if any(fuzz.ratio(w, x) >= 85 for x in b))


def shown_text(e: dict) -> str:
    return e.get("after") if e["kind"] == "text_change" else e.get("text") or ""


def unmentioned(ev: dict, lang: str) -> list[dict]:
    rx = re.compile(ERROR.get(lang, ERROR["en"]))
    utts = ev["speech"]["utterances"]
    out = []
    for e in ev["events"]:
        if e["kind"] not in ("appear", "text_change"):
            continue
        text = shown_text(e)
        m = rx.search(norm(text))
        if not m:
            continue
        near = [u for u in utts if u["end_ms"] >= e["t_ms"] - NEAR_SPEECH_MS[0] and u["start_ms"] <= e["t_ms"] + NEAR_SPEECH_MS[1]]
        if any(rx.search(norm(u["text"])) or shares(words(text), words(u["text"])) >= 2 for u in near):
            continue
        dur = f" for {(e['end_ms'] - e['t_ms']) / 1000:.1f} s" if e.get("end_ms") else ""
        out.append({"kind": "unmentioned", "t_ms": e["t_ms"], "refs": [e["id"]],
                    "text": f'error text on screen{dur}: "{text}"'})
    return out


def area_text(screen: dict, box: list[int]) -> list[str]:
    x, y, w, h = box
    return [t["text"] for t in screen["texts"]
            if y <= t["bbox"][1] + t["bbox"][3] / 2 <= y + h and t["bbox"][0] < x + w and t["bbox"][0] + t["bbox"][2] > x]


def has(value: list[str], texts: list[str]) -> bool:
    bag = [w for t in texts for w in re.findall(r"[\w']+", norm(t))]
    return bool(value) and all(any(fuzz.ratio(w, b) >= 85 for b in bag) for w in value)


def reverts(ev: dict) -> list[dict]:
    """A short value changed back to one it had a moment ago, and no click came before the change."""
    clicks = [e["t_ms"] for e in ev["events"] if e["kind"] == "click"]
    screens = ev["screens"]
    out = []
    for e in ev["events"]:
        if e["kind"] != "text_change":
            continue
        back = [w for w in re.findall(r"[\w']+", norm(e.get("after"))) if len(w) >= 3]
        gone = [w for w in re.findall(r"[\w']+", norm(e.get("before"))) if len(w) >= 3]
        if not back or not gone or len(back) > 4 or back == gone:
            continue
        prior = [s for s in screens if s["end_ms"] <= e["t_ms"] and s["end_ms"] >= e["t_ms"] - REVERT_MS]
        since = None
        for s in reversed(prior):
            texts = area_text(s, e["bbox"])
            if has(gone, texts) and not has(back, texts):
                since = s["start_ms"]
                continue
            if since is not None and has(back, texts) and not has(gone, texts) and not any(since < c <= e["t_ms"] for c in clicks):
                out.append({"kind": "revert", "t_ms": e["t_ms"], "refs": [e["id"]],
                            "text": f'"{e["before"]}" went back to "{e["after"]}" after {(e["t_ms"] - since) / 1000:.1f} s, no click before it'})
            break
    return out


def dots(image: np.ndarray) -> list[dict]:
    """Title-bar buttons: three round dots of one size in a row, coloured on the front window, grey on the others."""
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    coloured = (hsv[..., 1] > 110) & (hsv[..., 2] > 140)
    bar = cv2.dilate(gray, np.ones((1, 41), np.uint8)).astype(np.int16)  # the title bar is the brightest thing around
    grey = (hsv[..., 1] < 30) & (gray.astype(np.int16) < bar - 20) & (gray > 150)
    out = []
    for mask, front in ((coloured, True), (grey, False)):
        n, _, st, cen = cv2.connectedComponentsWithStats(mask.astype(np.uint8))
        blobs = [(cx, cy, w) for (x, y, w, h, a), (cx, cy) in zip(st[1:], cen[1:]) if 5 <= w <= 18 and abs(w - h) <= 2 and a >= 0.6 * w * h]
        for cx, cy, w in blobs:
            row = sorted((b for b in blobs if abs(b[1] - cy) <= 2 and abs(b[2] - w) <= 2 and b[0] > cx), key=lambda b: b[0])
            if len(row) >= 2 and 1.2 * w <= row[0][0] - cx <= 3 * w and abs((row[1][0] - row[0][0]) - (row[0][0] - cx)) <= 2:
                out.append({"x": cx, "y": cy, "d": w, "front": front})
    return out


def window_box(image: np.ndarray, d: dict) -> list[int]:
    """Window around its title-bar buttons: left and top edges next to them, the right edge where the title bar colour
    ends, the bottom where the left border ends."""
    g = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY).astype(np.int16)
    H, W = g.shape
    cx, cy, r = round(d["x"]), round(d["y"]), int(d["d"])
    xs = cx - round(1.3 * r)  # plain title bar between the window edge and the first button
    ref = int(np.median(g[cy - 2:cy + 3, xs]))
    x0 = xs
    while x0 > 0 and abs(g[cy, x0 - 1] - ref) < 12:
        x0 -= 1
    y0 = cy
    while y0 > 0 and abs(g[y0 - 1, xs] - ref) < 12:
        y0 -= 1
    # right edge: the first column after the buttons where most of the title bar's height has a step in brightness
    # (title letters and a cursor cover only part of it)
    band = g[y0 + 2:max(y0 + 3, 2 * cy - y0 - 2)]
    step = np.abs(band[:, 2:] - band[:, :-2]) >= 10
    tall = np.flatnonzero(step.mean(axis=0) >= 0.7) + 1
    tall = tall[tall > cx + 3 * r]
    below = g[min(H - 1, 2 * cy - y0):min(H, 2 * cy - y0 + 150)]  # a border goes on down, a cursor or a letter does not
    edge = [x for x in tall if x + 1 < W and below.size and (np.abs(below[:, x + 1] - below[:, x - 1]) >= 10).mean() >= 0.5]
    x1 = int(edge[0]) if edge else int(tall[0]) if len(tall) else W - 1  # covered below: the title bar alone
    y1, miss = cy, 0
    while y1 < H - 1 and miss < 40:
        y1 += 1
        edge = x0 >= 3 and x0 + 3 < W and abs(g[y1, x0 + 2] - g[y1, x0 - 3]) >= 8
        miss = 0 if edge else miss + 1
    y1 -= miss
    return [x0, y0, x1 - x0, y1 - y0]


def inside(box: list[int], win: list[int]) -> bool:
    cx, cy = box[0] + box[2] / 2, box[1] + box[3] / 2
    return win[0] <= cx <= win[0] + win[2] and win[1] <= cy <= win[1] + win[3]


def overlap(a: list[int], b: list[int]) -> bool:
    return a[0] < b[0] + b[2] and b[0] < a[0] + a[2] and a[1] < b[1] + b[3] and b[1] < a[1] + a[3]


def title_at(screen: dict, d: dict, box: list[int]) -> str:
    row = [t for t in screen["texts"] if abs(t["bbox"][1] + t["bbox"][3] / 2 - d["y"]) < 14 and box[0] < t["bbox"][0] < box[0] + box[2]]
    return " ".join(t["text"] for t in sorted(row, key=lambda t: t["bbox"][0])) or "a window"


def covered(ev: dict, work: Path) -> list[dict]:
    """A change inside a window that the front window partly covers."""
    by_start = {s["start_ms"]: s for s in ev["screens"]}
    cache: dict[str, list] = {}
    out = []
    for e in ev["events"]:
        if e["kind"] not in ("appear", "text_change", "visual_change") or not e.get("evidence"):
            continue
        frame = e["evidence"][-1]
        if frame not in cache:
            image = cv2.imread(str(work / frame))
            cache[frame] = [] if image is None else [{**d, "box": window_box(image, d)} for d in dots(image)]
        wins = cache[frame]
        front = [w for w in wins if w["front"]]
        fx, fy, fw, fh = front[0]["box"] if len(front) == 1 else (0, 0, 0, 0)
        # touching the front window: its own shadow or dimming, not the window behind
        if len(front) != 1 or overlap(e["bbox"], [fx - 10, fy - 10, fw + 20, fh + 20]):
            continue
        back = [w for w in wins if not w["front"] and inside(e["bbox"], w["box"]) and overlap(w["box"], front[0]["box"])]
        if not back:
            continue
        screen = by_start.get(e["t_ms"]) or max((s for s in ev["screens"] if s["start_ms"] <= e["t_ms"]), key=lambda s: s["start_ms"])
        out.append({"kind": "covered", "t_ms": e["t_ms"], "refs": [e["id"]],
                    "text": f'changed in "{title_at(screen, back[0], back[0]["box"])}", partly covered by "{title_at(screen, front[0], front[0]["box"])}": "{shown_text(e) or "icon"}"'})
    return out


def claims(ev: dict, lang: str) -> list[dict]:
    """Sentences with a claim marker; each is checked against texts that appeared on screen around it."""
    rxs = [re.compile(r) for r in CLAIM.get(lang, CLAIM["en"])]
    shown = [e for e in ev["events"] if e["kind"] in ("appear", "text_change")]
    out = []
    for u in ev["speech"]["utterances"]:
        for sent in re.split(r"(?<=[.!?;])\s+", u["text"]):
            if not any(r.search(norm(sent)) for r in rxs):
                continue
            ws = words(sent)
            seen = [e for e in shown if u["start_ms"] - 15000 <= e["t_ms"] <= u["end_ms"] + 3000
                    and ws and shares(ws, words(shown_text(e))) >= min(2, len(ws))]
            if seen:
                continue
            out.append({"kind": "claim", "t_ms": u["start_ms"], "end_ms": u["end_ms"], "refs": [u["id"]],
                        "text": f'"{sent.strip()}" - nothing on screen around it shows this'})
    return out


def build(ev: dict, work: Path, lang: str, speech: bool = True) -> list[dict]:
    """speech=False: the speech pass was skipped, only the checks that need no speech."""
    # in a meeting "maybe" is a proposal, not a claim; a meeting has people tiles or slides
    meeting = any(r["id"] == "people" for r in ev["regions"]) or bool(ev.get("slides")) or any(u.get("tile") for u in ev["speech"]["utterances"])
    out = reverts(ev) + covered(ev, work)
    if speech:
        out += unmentioned(ev, lang) + ([] if meeting else claims(ev, lang))
    return sorted(out, key=lambda c: c["t_ms"])
