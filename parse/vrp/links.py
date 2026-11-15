"""Links: what a phrase in the speech refers to on the screen. No model; words with their times, cursor events and the
screen states.

- an action: a click, a hover or a window coming to the front while words are said -> those words are about its target;
- a pointing word ("this", "here", "that one") -> the text under the cursor at that moment, else the element that has
  just appeared; nothing on screen to point at -> unresolved (target None);
- a mention: words of the speech that match a text on the screen right then ("file unavailable") -> that text.
"""
import re

from rapidfuzz import fuzz

DEICTIC = {
    "en": {"this", "these", "those", "here", "there"},  # "it" and "that" are mostly not pointing ("sending it", "says that")
    "ru": {"это", "этот", "эта", "эти", "вот", "здесь", "тут", "там", "сюда", "туда"},
}
ACTION_BEFORE, ACTION_AFTER = 700, 500  # words this long before / after an action belong to it
RECENT_MS = 5000  # "this" with no pointing: the element that appeared this recently


def toks(s: str) -> list[str]:
    return re.sub(r"[^\w ]|_", " ", (s or "").lower().replace("ё", "е")).split()


def words_between(utts: list[dict], t0: int, t1: int) -> list[tuple[dict, dict]]:
    return [(u, w) for u in utts for w in u["words"] if w["end_ms"] >= t0 and w["start_ms"] <= t1]


def state_at(screens: list[dict], t: int) -> dict | None:
    return next((s for s in screens if s["start_ms"] <= t < s["end_ms"]), screens[-1] if screens else None)


def link(u: dict, ws: list[dict], target: dict | None, relation: str) -> dict:
    return {
        "utterance": u["id"],
        "phrase": " ".join(w["w"].strip() for w in ws),
        "start_ms": ws[0]["start_ms"],
        "end_ms": ws[-1]["end_ms"],
        "target": {"bbox": target["bbox"], "text": target.get("text") or ""} if target and target.get("bbox") else None,
        "relation": relation,
    }


def build(evidence: dict, lang: str) -> list[dict]:
    utts = evidence["speech"]["utterances"]
    screens = evidence["screens"]
    events = evidence["events"]
    out: list[dict] = []
    used: set[tuple[str, int]] = set()

    def take(pairs):
        for u, w in pairs:
            used.add((u["id"], w["start_ms"]))

    # 1. actions with the words said around them
    for e in events:
        if e["kind"] not in ("click", "point", "window_change"):
            continue
        t1 = e["end_ms"] if e["kind"] == "point" and e.get("end_ms") else e["t_ms"] + ACTION_AFTER
        pairs = words_between(utts, e["t_ms"] - ACTION_BEFORE, t1)
        if not pairs:
            continue
        # the utterance with the word closest to the action ("...that. Option C is..." - the hover belongs to the second)
        u = min(pairs, key=lambda p: abs(p[1]["start_ms"] - e["t_ms"]))[0]
        ws = [w for uu, w in pairs if uu is u]
        rel = {"click": "click", "point": "point", "window_change": "focus"}[e["kind"]]
        out.append(link(u, ws, e, rel))  # an icon has no text, but its place is known
        take(pairs)

    # 2. pointing words not covered by an action
    deictic = DEICTIC.get(lang, DEICTIC["en"])
    for u in utts:
        for w in u["words"]:
            if (u["id"], w["start_ms"]) in used or not set(toks(w["w"])) & deictic:
                continue
            t = (w["start_ms"] + w["end_ms"]) // 2
            target, rel = None, "mentions"
            # pointing is a hover or a click around the word; a cursor just parked somewhere is not
            act = [e for e in events if e["kind"] in ("point", "click") and e["t_ms"] - 400 <= t <= (e.get("end_ms") or e["t_ms"]) + 400]
            if act:
                target, rel = act[0], act[0]["kind"]
            if target is None:
                recent = [e for e in events if e["kind"] in ("appear", "text_change", "visual_change") and t - RECENT_MS <= e["t_ms"] <= t and e.get("text")]
                target = recent[-1] if recent else None
            out.append(link(u, [w], target, rel))
            used.add((u["id"], w["start_ms"]))

    # 3. words that say what is written on the screen
    for u in utts:
        s = state_at(screens, (u["start_ms"] + u["end_ms"]) // 2)
        if not s:
            continue
        ws = u["words"]
        for x in s["texts"]:
            tx = toks(x["text"])
            if not tx or (len(tx) == 1 and len(tx[0]) < 6):
                continue  # a single short word ("OK", "me") says too little
            n = len(tx)
            for i in range(len(ws) - n + 1):
                span = ws[i:i + n]
                if any((u["id"], w["start_ms"]) in used for w in span):
                    continue
                if fuzz.ratio(" ".join(toks(" ".join(w["w"] for w in span))), " ".join(tx)) >= 85:
                    out.append(link(u, span, x, "mentions"))
                    for w in span:
                        used.add((u["id"], w["start_ms"]))
                    break
    return sorted(out, key=lambda l: l["start_ms"])
