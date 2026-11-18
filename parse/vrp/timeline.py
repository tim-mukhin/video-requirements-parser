"""Event timeline from evidence.json: lines for an agent (timeline.md) and a page with frames for a human (timeline.html).

Fully deterministic: the same facts give the same files. No model, assembly only.
"""
import html
import json
from pathlib import Path

import cv2

from .events import look_words, way
from .voices import label, summary

SHORT_MS = 1000  # appeared and disappeared faster than this - "flashed"
LABEL = {
    "appear": "APPEARED",
    "disappear": "DISAPPEARED",
    "text_change": "CHANGED",
    "visual_change": "ICON/COLOUR CHANGED",
    "screen_change": "SCREEN CHANGED",
    "window_change": "WINDOW TO FRONT",
    "click": "CLICK",
    "point": "HOVER",
    "key": "KEY",
    "type": "TYPED",
    "transient": "FOR A MOMENT",
    "move": "MOVED",
    "scroll": "SCROLLED",
    "drag": "DRAG",
    "flicker": "FLICKER",
}


SHAPE = {"hand": " (hand cursor)", "text": " (I-beam cursor)"}
NAMES = {"text": "I-beam"}  # the arrow is the default, not worth a word


def ts(ms: int) -> str:
    return f"{ms // 60000:02d}:{ms % 60000 / 1000:04.1f}"


def crops(evidence: dict, work: Path, pad: int = 16) -> None:
    """Cut-out of the event box from the frame after (for "disappeared" - from the frame before)."""
    out = work / "frames" / "crops"
    out.mkdir(parents=True, exist_ok=True)
    for f in out.glob("*.jpg"):
        f.unlink()
    cache: dict[str, object] = {}
    for e in evidence["events"]:
        if not e.get("bbox") or not e.get("evidence"):
            continue
        src = e["evidence"][0 if e["kind"] == "disappear" else -1]
        if src not in cache:
            cache[src] = cv2.imread(str(work / src))
        img = cache[src]
        if img is None:
            continue
        x, y, w, h = e["bbox"]
        H, W = img.shape[:2]
        x0, y0, x1, y1 = max(0, x - pad), max(0, y - pad), min(W, x + w + pad), min(H, y + h + pad)
        if x1 <= x0 or y1 <= y0:
            continue
        path = out / f"{e['id']}.jpg"
        cv2.imwrite(str(path), img[y0:y1, x0:x1], [cv2.IMWRITE_JPEG_QUALITY, 90])
        e["crop"] = path.relative_to(work).as_posix()


def rows(evidence: dict) -> list[dict]:
    """A timeline row: an utterance, or a moment when something happened on screen (events of one moment together)."""
    out = []
    for u in evidence["speech"]["utterances"]:
        out.append({"t": u["start_ms"], "kind": "speech", "who": label(u), "parts": u.get("parts", []), "text": u["text"], "end": u["end_ms"], "ids": [u["id"]]})
    moments: dict[int, list[dict]] = {}
    for e in evidence["events"]:
        moments.setdefault(e["t_ms"], []).append(e)
    for t, evs in moments.items():
        out.append({"t": t, "kind": "screen", "events": evs, "frame": next((e["evidence"][-1] for e in evs if e.get("evidence")), None), "ids": [e["id"] for e in evs]})
    return sorted(out, key=lambda r: (r["t"], r["kind"] != "screen"))


def span(e: dict) -> str:
    ms = e["end_ms"] - e["t_ms"]
    return "in one frame" if e.get("frames") == 1 else f"over {ms} ms" if ms < 1000 else f"over {ms / 1000:.1f} s"


def describe(e: dict) -> str:
    if e.get("edge"):
        return describe({**e, "edge": None}) + f' (its box reaches the {" and ".join(e["edge"])} edge of the screen: it may be cut off there, a guess)'
    lab = LABEL[e["kind"]]
    if e["kind"] == "flicker" and e["source"] == "cursor":
        shapes = " and ".join(NAMES.get(k, k) for k in e["cursor"])
        return (f'{lab} of the cursor: it switched between two shapes (tracked as {shapes}) {e["count"]} times {span(e)}, '
                f'{e["still"]} of them while it did not move')
    if e["kind"] == "flicker":
        what = f': "{e["text"]}"' if e.get("text") else ""
        return f'{lab}: the area at {e["bbox"]} went back to how it looked a moment before {e["count"]} times {span(e)}{what}'
    if e["kind"] == "type" and e.get("values"):
        seq = " → ".join(f'"{v}"' for v in e["values"])
        return f'{lab} (inferred: the text of one field changed in place {len(e["values"]) - 1} times {span(e)}, as OCR read it): {seq}'
    if e["kind"] in ("move", "scroll", "drag"):
        what = f'"{e["text"]}"' if e.get("text") else f"the area at {e['bbox']}"
        how = f'{way(*e["peak"])} and back {e["back_ms"]} ms later' if e.get("back") else f'{way(e["dx"], e["dy"])} {span(e)}'
        if e["kind"] == "scroll":
            return f'{lab}: content moved {how} (area {e["bbox"]}): {what}'
        if e["kind"] == "drag":
            onto = f' onto "{e["onto"]}"' if e.get("onto") else ""
            after = f'after the drop: {e["after"]}' if e.get("after") else "nothing changed on screen within 1.5 s after the drop"
            return (f'{lab} (inferred: the cursor moved and the content under it followed): {what} from {e.get("at")} to {e.get("to")}{onto}, '
                    f'{how}; {after}')
        if e.get("from"):
            return f'{lab} {how}, from {e["from"]} to {e["bbox"]}: {what}'
        return f'{lab} {how}: {what}' + (f" (area {e['bbox']})" if e.get("text") else "")
    text = (e.get("text") or "").strip()
    if e["kind"] == "appear" and e.get("end_ms") and e["end_ms"] - e["t_ms"] < SHORT_MS:
        return f'FLASHED for {(e["end_ms"] - e["t_ms"]) / 1000:.1f} s: "{text}"'
    if e["kind"] == "appear" and e.get("end_ms"):
        return f'{lab} for {(e["end_ms"] - e["t_ms"]) / 1000:.1f} s: "{text}"'
    if e["kind"] == "transient":
        n = e.get("frames", 1)
        what = f'"{text}"' if text else f"the area at {e['bbox']}"
        return f'SHOWN FOR {n} FRAME{"S" if n > 1 else ""} ({e["end_ms"] - e["t_ms"]} ms) between two changes: {what}'
    if e["kind"] == "text_change":
        return f'{lab}: "{e.get("before", "")}" → "{e.get("after", text)}"'
    if e["kind"] == "screen_change":
        return f"{lab}: {text[:300]}"
    if e["kind"] == "visual_change":
        how = look_words(e.get("look"))
        where = f" just {e['beside']}" if e.get("beside") else ""
        return (f'{lab} in: "{text}"' if text else f"{lab} at {e['bbox']}{where}") + (f" ({how})" if how else "")
    if e["kind"] == "point" and e.get("reaction"):
        return describe({**e, "reaction": None}) + f" - the element under it: {e['reaction']}"
    if e["kind"] in ("click", "point"):
        lab += SHAPE.get(e.get("cursor"), "")
        if not text:
            return f"{lab} at {e.get('at')}"
    if e["kind"] == "point" and e.get("end_ms"):
        return f'{lab} for {(e["end_ms"] - e["t_ms"]) / 1000:.1f} s: "{text}"'
    return f'{lab}: "{text}"'


def link_text(ln: dict) -> str:
    rel = {"click": "clicked", "point": "pointed at", "focus": "brought to front", "mentions": "refers to"}[ln["relation"]]
    tgt = (f'"{ln["target"]["text"]}"' if ln["target"]["text"] else f"the element at {ln['target']['bbox']}") if ln["target"] else "nothing on screen (unresolved)"
    return f'↳ "{ln["phrase"]}" {rel} {tgt}'


CHECK = {"unmentioned": "ERROR NOBODY MENTIONS", "revert": "WENT BACK BY ITSELF", "covered": "CHANGED BEHIND THE FRONT WINDOW", "claim": "CLAIM NOT SHOWN"}


def input_line(evidence: dict) -> list[str]:
    """What the video lets us see of the user's own actions: no CLICK before a change is not "it happened by itself"."""
    i = evidence.get("input")
    if not i:
        return []
    unseen = ("A change with no CLICK or TAP right before it was still caused by something: most likely a click, tap or key "
              "the video does not show, not the app acting by itself.")
    device = f" Looks like a phone or tablet ({i['touch_screen']}), a guess." if i.get("touch_screen") else ""
    if i["cursor_share"] == 0 and not i["touch"]:
        return [f"User input: no mouse cursor and no touch marks are visible in this video, so clicks, taps and keys are not seen.{device} {unseen}"]
    if i["cursor_share"] == 0:
        return [f"User input: no mouse cursor; {i['touch']} taps are seen as touch marks, but only where the recorder draws them.{device} {unseen}"]
    lost = ", ".join(f"{ts(a)}-{ts(b)}" for a, b in i["cursor_lost"][:6])
    return [f"User input: the cursor is followed through {i['cursor_share']:.0%} of the video"
            + (f"; it is not found {lost}, and clicks there are not seen" if lost else "")
            + ". Clicks are inferred (the cursor stopped, then the screen reacted); keys are not seen."]


def render_md(evidence: dict, title: str) -> str:
    v = evidence["video"]
    lines = [
        f"# {title}",
        "",
        f"Video `{v['file']}`, {v['width']}×{v['height']}, {v['duration_ms'] / 1000:.1f} s. "
        f"Screen states: {len(evidence['screens'])}, events: {len(evidence['events'])}, utterances: {len(evidence['speech']['utterances'])}.",
        "Time is from the start of the video. Square brackets hold event ids from evidence.json, then the evidence frame;"
        " \"moment\" is a strip of every frame around a short event, cropped to it and enlarged.",
        *(["The video has no audio track: nothing was said, every fact comes from the screen."] if evidence["speech"].get("no_audio") else []),
        *input_line(evidence),
        "",
    ]
    if evidence.get("checks"):
        lines += ["## Cross-checks", "", "Facts that show only when speech, screen and windows are put side by side.", ""]
        lines += [f'{ts(c["t_ms"])}  {CHECK[c["kind"]]}: {c["text"]}  [{", ".join(c["refs"])}]' for c in evidence["checks"]]
        lines.append("")
    if voices := summary(evidence):
        lines += ["## Voices", "", "Voice ids come from the sound (diarization); tiles and names are facts with their source, not a verdict.", ""]
        lines += voices + [""]
    lines += ["## Timeline", ""]
    by_utt: dict[str, list[dict]] = {}
    for ln in evidence.get("links", []):
        by_utt.setdefault(ln["utterance"], []).append(ln)
    for r in rows(evidence):
        if r["kind"] == "speech":
            lines.append(f'{ts(r["t"])}  SAID {r["who"]}: "{r["text"]}"  [{r["ids"][0]}]')
            for pt in r["parts"]:
                lines.append(f'         ↳ {pt["voice"] or "unknown"} from {ts(pt["start_ms"])}: "{pt["text"]}"')
            for ln in by_utt.get(r["ids"][0], []):
                lines.append(f'         {link_text(ln)}')
            continue
        evs = r["events"]
        gone = [e for e in evs if e["kind"] == "disappear"]
        rest = [e for e in evs if e["kind"] != "disappear"]
        frame = f"  frame {r['frame']}" if r["frame"] else ""
        first = True
        for e in rest:
            lines.append(f"{ts(r['t']) if first else ' ' * 7}  {describe(e)}  [{e['id']}]{frame if first else ''}" + (f"  moment {e['moment']}" if e.get("moment") else ""))
            first = False
        if gone:
            names = ", ".join(f'"{(e.get("text") or "").strip()}"' for e in gone[:12]) + (f" and {len(gone) - 12} more" if len(gone) > 12 else "")
            lines.append(f"{ts(r['t']) if first else ' ' * 7}  DISAPPEARED: {names}  [{gone[0]['id']}…{gone[-1]['id']}]{frame if first else ''}")
    if evidence.get("slides"):
        lines += ["", "## Slides on screen", ""]
        for sl in evidence["slides"]:
            lines.append(f'{ts(sl["start_ms"])}-{ts(sl["end_ms"])}  slide {sl["index"]}: "{sl["title"]}"')
    for a in evidence.get("attachments") or []:
        lines += ["", f'## Attached file {a["file"]} ({a["pages"]} pages)', ""]
        if not a["differs_from_screen"]:
            lines.append("Says the same as the slides that were shown.")
        for d in a["differs_from_screen"]:
            lines.append(f'Slide {d["index"]} differs. On screen, not in the file: {", ".join(d["not_in_file"]) or "-"}. In the file, not on screen: {", ".join(d["not_on_screen"]) or "-"}.')
    lines += ["", "## Screen states", ""]
    for s in evidence["screens"]:
        top = " | ".join(b["text"] for b in sorted(s["texts"], key=lambda b: (b["bbox"][1], b["bbox"][0]))[:6])
        lines.append(f"{s['id']}  {ts(s['start_ms'])}-{ts(s['end_ms'])}  frame {s['frame']}  {top}")
    return "\n".join(lines) + "\n"


CSS = """
*{box-sizing:border-box} body{margin:0;font:14px/1.45 -apple-system,Inter,sans-serif;background:#0f1115;color:#e5e7eb}
header{padding:14px 20px;border-bottom:1px solid #262a33} header h1{margin:0 0 4px;font-size:18px} header p{margin:0;color:#9ca3af}
main{display:grid;grid-template-columns:minmax(420px,46%) 1fr;height:calc(100vh - 70px)}
#left{padding:14px;border-right:1px solid #262a33;overflow:auto} video{width:100%;border-radius:8px;background:#000}
#screens{display:flex;flex-wrap:wrap;gap:8px;margin-top:12px} .scr{width:150px;cursor:pointer;color:#9ca3af;font-size:12px}
.scr img{width:150px;border-radius:4px;border:2px solid transparent;display:block} .scr.on img{border-color:#22c55e}
#feed{overflow:auto;padding:8px 14px 80px} .row{display:grid;grid-template-columns:64px 1fr;gap:10px;padding:8px;border-radius:8px;cursor:pointer}
.row:hover{background:#171a21} .row.on{background:#1e293b} .t{color:#60a5fa;font-variant-numeric:tabular-nums}
.speech .who{color:#f59e0b;font-weight:600;margin-right:6px} .speech .txt{color:#f3f4f6}
.ev{margin:2px 0} .b{display:inline-block;font-size:11px;font-weight:700;padding:1px 6px;border-radius:4px;margin-right:6px;background:#374151}
.b.appear{background:#065f46} .b.visual_change{background:#6d28d9} .b.click,.b.point{background:#0e7490} .b.flash{background:#b91c1c} .b.disappear{background:#4b5563} .b.text_change{background:#92400e}
.b.screen_change,.b.window_change{background:#1d4ed8} .id{color:#6b7280;font-size:11px;margin-left:6px}
.crops{display:flex;flex-wrap:wrap;gap:6px;margin-top:6px} .crops img{max-height:90px;max-width:360px;border-radius:4px;border:1px solid #374151}
.gone{color:#9ca3af;font-size:12px} .key img{max-width:260px;border-radius:4px;margin-top:6px;border:1px solid #374151}
label{color:#9ca3af;font-size:12px} .link{color:#a5b4fc;font-size:12px;margin-top:2px}
#extra h3{font-size:13px;margin:16px 0 6px;color:#e5e7eb} #extra div{font-size:12px;color:#9ca3af;cursor:pointer} #extra .diff{color:#fca5a5}
"""

JS = """
const v=document.querySelector('video'),rows=[...document.querySelectorAll('[data-t]')],scr=[...document.querySelectorAll('.scr')];
const auto=document.getElementById('auto');
document.addEventListener('click',e=>{const r=e.target.closest('[data-t]');if(r){v.currentTime=r.dataset.t/1000;v.play();}});
v.addEventListener('timeupdate',()=>{const t=v.currentTime*1000;let cur=null;
 for(const r of rows){if(r.classList.contains('row')&&+r.dataset.t<=t)cur=r;}
 rows.forEach(r=>r.classList.toggle('on',r===cur));
 scr.forEach(s=>s.classList.toggle('on',+s.dataset.t<=t&&t<+s.dataset.end));
 if(cur&&auto.checked)cur.scrollIntoView({block:'center',behavior:'smooth'});});
"""


def render_html(evidence: dict, title: str, video_src: str) -> str:
    esc = html.escape
    v = evidence["video"]
    feed = []
    by_utt: dict[str, list[dict]] = {}
    for ln in evidence.get("links", []):
        by_utt.setdefault(ln["utterance"], []).append(ln)
    for r in rows(evidence):
        if r["kind"] == "speech":
            lk = "".join(f'<div class="link">↳ {esc(pt["voice"] or "unknown")} from {ts(pt["start_ms"])}: {esc(pt["text"])}</div>' for pt in r["parts"])
            lk += "".join(f'<div class="link">{esc(link_text(ln))}</div>' for ln in by_utt.get(r["ids"][0], []))
            feed.append(f'<div class="row speech" data-t="{r["t"]}"><div class="t">{ts(r["t"])}</div><div><span class="who">{esc(r["who"])}</span><span class="txt">{esc(r["text"])}</span><span class="id">{r["ids"][0]}</span>{lk}</div></div>')
            continue
        evs = r["events"]
        gone = [e for e in evs if e["kind"] == "disappear"]
        parts = []
        for e in evs:
            if e["kind"] == "disappear":
                continue
            flash = e["kind"] == "appear" and e.get("end_ms") and e["end_ms"] - e["t_ms"] < SHORT_MS
            cls = "flash" if flash else e["kind"]
            parts.append(f'<div class="ev"><span class="b {cls}">{"FLASHED" if flash else LABEL[e["kind"]]}</span>{esc(describe(e).split(": ", 1)[-1])}<span class="id">{e["id"]}</span></div>')
        if gone:
            parts.append(f'<div class="ev gone"><span class="b disappear">DISAPPEARED</span>{esc(", ".join((e.get("text") or "") for e in gone[:10]))}{" …" if len(gone) > 10 else ""}</div>')
        imgs = ([e["moment"] for e in evs if e.get("moment")] + [e["crop"] for e in evs if e.get("crop") and not e.get("moment") and e["kind"] != "disappear"])[:6]
        crop_html = f'<div class="crops">{"".join(f"<img src=\"{esc(i)}\" loading=lazy>" for i in imgs)}</div>' if imgs else ""
        key = f'<div class="key"><img src="{esc(r["frame"])}" loading=lazy></div>' if r["frame"] and any(e["kind"] == "screen_change" for e in evs) else ""
        feed.append(f'<div class="row" data-t="{r["t"]}"><div class="t">{ts(r["t"])}</div><div>{"".join(parts)}{crop_html}{key}</div></div>')
    strip = "".join(
        f'<div class="scr" data-t="{s["start_ms"]}" data-end="{s["end_ms"]}"><img src="{esc(s["frame"])}" loading=lazy>{s["id"]} · {ts(s["start_ms"])}-{ts(s["end_ms"])}</div>'
        for s in evidence["screens"]
        if s.get("frame")
    )
    extra = ""
    if voices := summary(evidence):
        extra += "<h3>Voices</h3>" + "".join(f"<div>{esc(v)}</div>" for v in voices)
    if evidence.get("checks"):
        extra += "<h3>Cross-checks</h3>" + "".join(f'<div class="sl" data-t="{c["t_ms"]}">{ts(c["t_ms"])} · <b>{CHECK[c["kind"]]}</b> {esc(c["text"])}</div>' for c in evidence["checks"])
    if evidence.get("slides"):
        extra += "<h3>Slides on screen</h3>" + "".join(f'<div class="sl" data-t="{sl["start_ms"]}">{ts(sl["start_ms"])}-{ts(sl["end_ms"])} · slide {sl["index"]}: {esc(sl["title"])}</div>' for sl in evidence["slides"])
    for a in evidence.get("attachments") or []:
        extra += f'<h3>{esc(a["file"])}</h3>'
        extra += "".join(f'<div class="diff">Slide {d["index"]} differs. On screen, not in the file: {esc(", ".join(d["not_in_file"]) or "-")}. In the file, not on screen: {esc(", ".join(d["not_on_screen"]) or "-")}.</div>' for d in a["differs_from_screen"]) or "<div>Says the same as the slides that were shown.</div>"
    meta = f"{v['width']}×{v['height']} · {v['duration_ms'] / 1000:.1f} s · states {len(evidence['screens'])} · events {len(evidence['events'])} · utterances {len(evidence['speech']['utterances'])}"
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{esc(title)}</title><style>{CSS}</style></head><body>
<header><h1>{esc(title)}</h1><p>{meta} · <label><input type="checkbox" id="auto" checked> follow the video</label></p></header>
<main><div id="left"><video src="{esc(video_src)}" controls></video><div id="screens">{strip}</div><div id="extra">{extra}</div></div><div id="feed">{"".join(feed)}</div></main>
<script>{JS}</script><script type="application/json" id="evidence">{json.dumps(evidence, ensure_ascii=False).replace("</", "<\\/")}</script></body></html>
"""
