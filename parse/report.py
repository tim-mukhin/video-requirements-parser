"""Index page out/index.html: every video in every language, links to the parser and ground-truth timelines, evaluation.

python report.py   (after run.py and evaluate.py)
"""
import html
import json
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "out"
LANG_NAMES = {"en": "English", "ru": "Russian"}


def pct(x):
    return "-" if x is None else f"{x * 100:.0f}%"


ev = {r["id"]: r for r in json.loads((OUT / "_eval.json").read_text())} if (OUT / "_eval.json").exists() else {}
sections = []
for lang in sorted({p.parts[-3] for p in OUT.glob("*/*/manifest.json")}):
    rows = []
    for man in sorted(OUT.glob(f"{lang}/*/manifest.json")):
        key = f"{lang}/{man.parent.name}"
        m = json.loads(man.read_text())
        r = ev.get(key, {})
        variants = " ".join(f'<a href="{lang}/{html.escape(v["file"][3:])}">{v["id"]}</a>' for v in m["variants"])
        parsed = man.parent / "parsed"
        links = [
            f'<a href="{key}/parsed/timeline.html">parser</a>' if (parsed / "timeline.html").exists() else "",
            f'<a href="{key}/truth/timeline.html">ground truth</a>' if (man.parent / "truth" / "timeline.html").exists() else "",
            f'<a href="{key}/parsed/timeline.md">agent timeline</a>' if (parsed / "timeline.md").exists() else "",
        ]
        crit = f"{r['critical_found']}/{r['critical_total']}" if r else "-"
        d = m["difficulty"]
        rows.append(
            f"<tr><td><b>{man.parent.name}</b><br><span>{html.escape(m['title'])}</span></td><td>{m.get('device', 'desktop')}<br>{d['speech']}, {d['signal']['kind']}</td>"
            f"<td>{variants}</td><td>{' · '.join(filter(None, links))}</td><td>{crit}</td><td>{pct(r.get('recall'))}</td><td>{pct(r.get('precision'))}</td><td>{pct(r.get('clicks'))}</td><td>{pct(r.get('hovers'))}</td><td>{pct(r.get('screen_text'))}</td><td>{pct(r.get('links'))}</td><td>{pct(r.get('speakers'))}</td><td>{pct(r.get('slides'))}</td><td>{pct(r.get('files'))}</td><td>{pct(r.get('wer'))}</td></tr>"
        )
    sections.append(
        f"<h2>{LANG_NAMES.get(lang, lang)}</h2><table><tr><th>Scenario</th><th>Kind</th><th>Video</th><th>Timelines</th><th>Critical</th><th>Recall</th><th>Precision</th><th>Clicks</th><th>Hovers</th><th>Screen text</th><th>Links</th><th>Speakers</th><th>Slides</th><th>Files</th><th>WER</th></tr>{''.join(rows)}</table>"
    )

page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>video-requirements-parser</title><style>
body{{font:14px/1.45 -apple-system,Inter,sans-serif;background:#0f1115;color:#e5e7eb;margin:24px}} table{{border-collapse:collapse;width:100%;margin-bottom:32px}}
td,th{{border-bottom:1px solid #262a33;padding:8px;text-align:left;vertical-align:top}} th{{color:#9ca3af;font-weight:500}} td span{{color:#9ca3af;font-size:12px}}
a{{color:#60a5fa;text-decoration:none}} a:hover{{text-decoration:underline}}</style></head><body>
<h1>Synthetic test videos and parser results</h1>
<p>Critical - critical moments of the scenario found by the parser; recall and precision - over screen changes; clicks and hovers - found from the cursor track; screen text - share of on-screen texts read at the right moment; WER - word error rate of the speech.</p>
{''.join(sections)}</body></html>
"""
(OUT / "index.html").write_text(page)
print(OUT / "index.html")
