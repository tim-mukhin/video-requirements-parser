"""Slides: which slide was on screen when (by its page number, "3 / 6" or "Slide 3 of 6"), and whether a file attached
to the video (pdf, pptx) says the same as what was shown. No model: text of the screen against text of the file.
"""
import re
import subprocess
import zipfile
from pathlib import Path

from rapidfuzz import fuzz

PAGE = [re.compile(r"(?<![\d/])(\d{1,2})\s*/\s*(\d{1,2})\s*$"), re.compile(r"slide\s+(\d{1,2})\s+(?:of|из)\s+(\d{1,2})", re.I)]


def toks(s: str) -> list[str]:
    return re.sub(r"[^\w ]|_", " ", (s or "").lower().replace("ё", "е")).split()


def page_of(texts: list[dict]) -> tuple[int, dict | None] | None:
    """Slide number shown on the screen and the text that holds it (the footer of the slide, if it is a slide)."""
    for rx in PAGE:
        for t in texts:
            m = rx.search(t["text"])
            if m and 0 < int(m.group(1)) <= int(m.group(2)) <= 99:
                return int(m.group(1)), (t if rx is PAGE[0] else None)
    return None


def slide_texts(texts: list[dict], footer: dict | None) -> tuple[str, list[dict]]:
    """Title and the texts on the slide itself. The footer row (deck name ... page number) gives the slide's left and
    right edges; the title is the topmost of the large texts above it. A slide editor's ribbon, thumbnails and notes
    fall outside."""
    if footer is None:
        return max(texts, key=lambda t: t["bbox"][3])["text"], texts
    fy = footer["bbox"][1] + footer["bbox"][3] / 2
    row = [t for t in texts if abs(t["bbox"][1] + t["bbox"][3] / 2 - fy) < footer["bbox"][3]]
    x0, x1 = min(t["bbox"][0] for t in row) - 60, footer["bbox"][0] + footer["bbox"][2] + 60
    above = [t for t in texts if x0 <= t["bbox"][0] and t["bbox"][0] + t["bbox"][2] <= x1 and t["bbox"][1] < footer["bbox"][1] and t not in row]
    if not above:
        return footer["text"], row
    tall = max(t["bbox"][3] for t in above)
    title = min((t for t in above if t["bbox"][3] >= 0.75 * tall), key=lambda t: t["bbox"][1])
    top = title["bbox"][1] - 40
    return title["text"], [t for t in above if t["bbox"][1] >= top] + row


def shown(screens: list[dict]) -> tuple[list[dict], dict[int, set[str]]]:
    """-> slides on screen [{index, title, start_ms, end_ms}], words seen on each slide."""
    out: list[dict] = []
    words: dict[int, set[str]] = {}
    for s in screens:
        p = page_of(s["texts"]) if s["texts"] else None
        if not p:
            continue
        idx, footer = p
        title, on_slide = slide_texts(s["texts"], footer)
        words.setdefault(idx, set()).update(w for t in on_slide for w in toks(t["text"]) if t is not footer)
        if out and out[-1]["index"] == idx:
            out[-1]["end_ms"] = s["end_ms"]
        else:
            out.append({"index": idx, "title": title, "start_ms": s["start_ms"], "end_ms": s["end_ms"]})
    return out, words


def file_pages(path: Path) -> list[set[str]]:
    if path.suffix == ".pdf":
        text = subprocess.run(["pdftotext", "-layout", str(path), "-"], capture_output=True, text=True, check=True).stdout
        return [set(toks(p)) for p in text.split("\f") if p.strip()]
    if path.suffix == ".pptx":
        with zipfile.ZipFile(path) as z:
            names = sorted((n for n in z.namelist() if re.fullmatch(r"ppt/slides/slide\d+\.xml", n)), key=lambda n: int(re.findall(r"\d+", n)[-1]))
            return [set(toks(" ".join(re.findall(r"<a:t>([^<]*)</a:t>", z.read(n).decode("utf-8"))))) for n in names]
    return []


def has(word: str, bag: set[str]) -> bool:
    return word in bag or any(fuzz.ratio(word, b) >= 85 for b in bag)


def compare(files: list[Path], words: dict[int, set[str]]) -> list[dict]:
    """For every attached file: slides whose text differs from what was on the screen (OCR slack per word)."""
    out = []
    for f in files:
        pages = file_pages(f)
        diffs = []
        for idx, seen in sorted(words.items()):
            if idx > len(pages):
                continue
            page = pages[idx - 1]
            distinct = lambda ws: {w for w in ws if len(w) >= 4 and not w.isdigit()}
            not_in_file = sorted(w for w in distinct(seen) if not has(w, page))
            not_on_screen = sorted(w for w in distinct(page) if not has(w, seen))
            if len(not_in_file) >= 2 or len(not_on_screen) >= 2:
                diffs.append({"index": idx, "not_in_file": not_in_file, "not_on_screen": not_on_screen})
        out.append({"file": f.name, "pages": len(pages), "differs_from_screen": diffs})
    return out
