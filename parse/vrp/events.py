"""Neighbouring screen states -> events: appeared, disappeared, text changed, the whole screen changed."""
import re

from rapidfuzz import fuzz


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.lower().replace("ё", "е")).strip()


def same(a: str, b: str) -> bool:
    return fuzz.ratio(norm(a), norm(b)) >= 88


def iou(a, b) -> float:
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    ix, iy = max(0, min(ax + aw, bx + bw) - max(ax, bx)), max(0, min(ay + ah, by + bh) - max(ay, by))
    inter = ix * iy
    return inter / (aw * ah + bw * bh - inter) if inter else 0.0


def merge_same(screens: list[dict]) -> list[dict]:
    """Neighbouring states with the same text (the cursor moved, a participant tile blinked) are merged."""
    out = []
    for s in screens:
        if out:
            p = out[-1]
            a, b = sorted(norm(t["text"]) for t in p["texts"]), sorted(norm(t["text"]) for t in s["texts"])
            if a == b:
                p["end_ms"] = s["end_ms"]
                continue
        out.append(s)
    return out


def diff(screens: list[dict]) -> list[dict]:
    events = []

    def add(**e):
        e["id"] = f"p{len(events) + 1:03d}"
        e.setdefault("end_ms", None)
        e.update(visible=True, source="ocr")
        events.append(e)

    for prev, cur in zip(screens, screens[1:]):
        t = cur["start_ms"]
        ev = [prev["frame"], cur["frame"]]
        changes, used = [], set()
        for cb in cur["texts"]:
            if any(same(cb["text"], pb["text"]) for pb in prev["texts"]):
                continue
            near = max(prev["texts"], key=lambda pb: iou(pb["bbox"], cb["bbox"]), default=None)
            if near and iou(near["bbox"], cb["bbox"]) >= 0.5:
                used.add(id(near))
                changes.append(dict(t_ms=t, kind="text_change", bbox=cb["bbox"], text=cb["text"], before=near["text"], after=cb["text"], evidence=ev))
            else:
                changes.append(dict(t_ms=t, kind="appear", bbox=cb["bbox"], text=cb["text"], evidence=ev))
        for pb in prev["texts"]:
            if id(pb) not in used and not any(same(pb["text"], cb["text"]) for cb in cur["texts"]):
                changes.append(dict(t_ms=t, kind="disappear", bbox=pb["bbox"], text=pb["text"], evidence=ev))
        if len(changes) > 6 and len(changes) > 0.6 * max(len(cur["texts"]), 1):
            # the whole screen changed: the event text holds everything new, top to bottom, so no detail is lost
            new = sorted((c for c in changes if c["kind"] != "disappear"), key=lambda c: (c["bbox"][1], c["bbox"][0]))
            add(t_ms=t, kind="screen_change", bbox=None, text=" | ".join(c["text"] for c in new), evidence=ev)
        else:
            for c in changes:
                add(**c)

    # how long an appeared element was shown: until the first state without its text
    for e in events:
        if e["kind"] != "appear":
            continue
        later = [s for s in screens if s["start_ms"] > e["t_ms"]]
        gone = next((s for s in later if not any(same(e["text"], b["text"]) for b in s["texts"])), None)
        e["end_ms"] = gone["start_ms"] if gone else None
    return events
