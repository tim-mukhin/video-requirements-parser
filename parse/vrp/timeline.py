"""Event timeline from evidence.json: lines for an agent (timeline.md) and a page with frames for a human (timeline.html).

Fully deterministic: the same facts give the same files. No model, assembly only.
"""
import html
import json
from pathlib import Path

import cv2

SHORT_MS = 1000  # appeared and disappeared faster than this - "flashed"
LABEL = {
    "appear": "APPEARED",
    "disappear": "DISAPPEARED",
    "text_change": "CHANGED",
    "screen_change": "SCREEN CHANGED",
    "window_change": "WINDOW TO FRONT",
    "click": "CLICK",
    "point": "HOVER",
    "key": "KEY",
    "type": "TYPED",
}


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
        e["crop"] = str(path.relative_to(work))


def rows(evidence: dict) -> list[dict]:
    """A timeline row: an utterance, or a moment when something happened on screen (events of one moment together)."""
    out = []
    for u in evidence["speech"]["utterances"]:
        out.append({"t": u["start_ms"], "kind": "speech", "who": u["speaker"], "text": u["text"], "end": u["end_ms"], "ids": [u["id"]]})
    moments: dict[int, list[dict]] = {}
    for e in evidence["events"]:
        moments.setdefault(e["t_ms"], []).append(e)
    for t, evs in moments.items():
        out.append({"t": t, "kind": "screen", "events": evs, "frame": next((e["evidence"][-1] for e in evs if e.get("evidence")), None), "ids": [e["id"] for e in evs]})
    return sorted(out, key=lambda r: (r["t"], r["kind"] != "screen"))


def describe(e: dict) -> str:
    lab = LABEL[e["kind"]]
    text = (e.get("text") or "").strip()
    if e["kind"] == "appear" and e.get("end_ms") and e["end_ms"] - e["t_ms"] < SHORT_MS:
        return f'FLASHED for {(e["end_ms"] - e["t_ms"]) / 1000:.1f} s: "{text}"'
    if e["kind"] == "appear" and e.get("end_ms"):
        return f'{lab} for {(e["end_ms"] - e["t_ms"]) / 1000:.1f} s: "{text}"'
    if e["kind"] == "text_change":
        return f'{lab}: "{e.get("before", "")}" → "{e.get("after", text)}"'
    if e["kind"] == "screen_change":
        return f"{lab}: {text[:300]}"
    return f'{lab}: "{text}"'


def render_md(evidence: dict, title: str) -> str:
    v = evidence["video"]
    lines = [
        f"# {title}",
        "",
        f"Video `{v['file']}`, {v['width']}×{v['height']}, {v['duration_ms'] / 1000:.1f} s. "
        f"Screen states: {len(evidence['screens'])}, events: {len(evidence['events'])}, utterances: {len(evidence['speech']['utterances'])}.",
        "Time is from the start of the video. Square brackets hold event ids from evidence.json, then the evidence frame.",
        "",
        "## Timeline",
        "",
    ]
    for r in rows(evidence):
        if r["kind"] == "speech":
            lines.append(f'{ts(r["t"])}  SAID {r["who"]}: "{r["text"]}"  [{r["ids"][0]}]')
            continue
        evs = r["events"]
        gone = [e for e in evs if e["kind"] == "disappear"]
        rest = [e for e in evs if e["kind"] != "disappear"]
        frame = f"  frame {r['frame']}" if r["frame"] else ""
        first = True
        for e in rest:
            lines.append(f"{ts(r['t']) if first else ' ' * 7}  {describe(e)}  [{e['id']}]{frame if first else ''}")
            first = False
        if gone:
            names = ", ".join(f'"{(e.get("text") or "").strip()}"' for e in gone[:12]) + (f" and {len(gone) - 12} more" if len(gone) > 12 else "")
            lines.append(f"{ts(r['t']) if first else ' ' * 7}  DISAPPEARED: {names}  [{gone[0]['id']}…{gone[-1]['id']}]{frame if first else ''}")
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
.b.appear{background:#065f46} .b.flash{background:#b91c1c} .b.disappear{background:#4b5563} .b.text_change{background:#92400e}
.b.screen_change,.b.window_change{background:#1d4ed8} .id{color:#6b7280;font-size:11px;margin-left:6px}
.crops{display:flex;flex-wrap:wrap;gap:6px;margin-top:6px} .crops img{max-height:90px;max-width:360px;border-radius:4px;border:1px solid #374151}
.gone{color:#9ca3af;font-size:12px} .key img{max-width:260px;border-radius:4px;margin-top:6px;border:1px solid #374151}
label{color:#9ca3af;font-size:12px}
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
    for r in rows(evidence):
        if r["kind"] == "speech":
            feed.append(f'<div class="row speech" data-t="{r["t"]}"><div class="t">{ts(r["t"])}</div><div><span class="who">{esc(r["who"])}</span><span class="txt">{esc(r["text"])}</span><span class="id">{r["ids"][0]}</span></div></div>')
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
        imgs = [e["crop"] for e in evs if e.get("crop") and e["kind"] != "disappear"][:6]
        crop_html = f'<div class="crops">{"".join(f"<img src=\"{esc(i)}\" loading=lazy>" for i in imgs)}</div>' if imgs else ""
        key = f'<div class="key"><img src="{esc(r["frame"])}" loading=lazy></div>' if r["frame"] and any(e["kind"] == "screen_change" for e in evs) else ""
        feed.append(f'<div class="row" data-t="{r["t"]}"><div class="t">{ts(r["t"])}</div><div>{"".join(parts)}{crop_html}{key}</div></div>')
    strip = "".join(
        f'<div class="scr" data-t="{s["start_ms"]}" data-end="{s["end_ms"]}"><img src="{esc(s["frame"])}" loading=lazy>{s["id"]} · {ts(s["start_ms"])}-{ts(s["end_ms"])}</div>'
        for s in evidence["screens"]
        if s.get("frame")
    )
    meta = f"{v['width']}×{v['height']} · {v['duration_ms'] / 1000:.1f} s · states {len(evidence['screens'])} · events {len(evidence['events'])} · utterances {len(evidence['speech']['utterances'])}"
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{esc(title)}</title><style>{CSS}</style></head><body>
<header><h1>{esc(title)}</h1><p>{meta} · <label><input type="checkbox" id="auto" checked> follow the video</label></p></header>
<main><div id="left"><video src="{esc(video_src)}" controls></video><div id="screens">{strip}</div></div><div id="feed">{"".join(feed)}</div></main>
<script>{JS}</script><script type="application/json" id="evidence">{json.dumps(evidence, ensure_ascii=False).replace("</", "<\\/")}</script></body></html>
"""
