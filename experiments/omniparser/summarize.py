"""Summarize runs/results_*.json: hit rate, caption verdicts, timings."""
import json
import statistics
import sys
from collections import Counter
from pathlib import Path

for path in sys.argv[1:]:
    r = json.loads(Path(path).read_text())
    cases = r["cases"]
    print(f"\n=== {Path(path).name}  detector={r.get('detector')} device={r['device']} size={r['size']} wall={r['wall_s']}s")
    icon = [c for c in cases if not c.get("control") and c["res"]["full_before"] is not None]
    act = [c for c in icon if c["gt_role"] == "button"]
    other = [c for c in icon if c["gt_role"] != "button"]
    ctrl = [c for c in cases if c.get("control")]
    print(f"clicks without text: {len(icon)} (icon buttons {len(act)}, other {len(other)}), control with text: {len(ctrl)}")
    for mode in ("full_before", "full_at", "cropdet_before", "cropdet_at", "cropcap_before", "cropcap_at"):
        res = [c["res"][mode] for c in act]
        hit = sum(1 for x in res if x.get("hit", "inside") != "none")
        v = Counter(x.get("verdict") or "no box" for x in res)
        det = [x["t_detect_ms"] for x in res if "t_detect_ms" in x]
        cap = [x["t_caption_ms"] for x in res if "t_caption_ms" in x]
        print(f"  {mode:15s} box {hit}/{len(res)}  right {v['right']}  ambiguous {v['ambiguous']}  wrong {v['wrong']}"
              f"  no box {v['no box']}  | detect {statistics.median(det) if det else '-'} ms, caption {statistics.median(cap) if cap else '-'} ms")
    print("  per action (full_before / cropdet_at / cropcap_at right):")
    for a in sorted({c["gt_text"] for c in act}):
        cs = [c for c in act if c["gt_text"] == a]
        f = lambda m: sum(1 for c in cs if c["res"][m].get("verdict") == "right")
        print(f"    {a:14s} n={len(cs):2d}  {f('full_before')} / {f('cropdet_at')} / {f('cropcap_at')}")
    print("  captions (gt | full_before | full_at | cropdet_at | cropcap_at):")
    for c in act + other + ctrl:
        g = lambda m: c["res"][m].get("caption", "-")
        tag = "ctrl" if c.get("control") else ("icon" if c in act else "notext")
        print(f"    [{tag}] {c['video'][:14]:14s} {str(c['gt_text'])[:28]:28s} | {g('full_before')} | {g('full_at')} | {g('cropdet_at')} | {g('cropcap_at')}")
    for p in r["pipeline"]:
        print(f"  full pipeline {Path(p['frame']).parent.parent.parent.name}: {p['n_boxes']} boxes, detect {p['t_detect_ms']} ms, caption all {p['t_caption_all_ms']} ms")
