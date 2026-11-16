"""Text reading: RapidOCR (PaddleOCR models on ONNX Runtime) on any system, Apple Vision (ocrmac) as an option on a Mac.

VRP_OCR=rapidocr|vision picks the engine. read(img, lang) -> [(text, [x, y, w, h])] in the image's pixels, top-left origin.
RapidOCR: the multilingual PP-OCRv6 detector finds the lines, a PP-OCRv5 recognizer per language reads them (en: English
letters only, so an icon is not read as a CJK character; ru: East Slavic, Cyrillic and Latin). Its boxes are padded by a
few pixels around the line; they are shrunk to the ink inside, as tight as Vision's, since later passes compare the
pixels inside a text's box (a typed field: "diego@fa" keeps its pixels while "b" is added next to it).
"""
import os
import time

import numpy as np
from PIL import Image

ENGINE = SPLIT = None
VISION_LANGS = {"en": ["en-US"], "ru": ["ru-RU", "en-US"]}
REC = {"en": "en", "ru": "eslav"}
INK = 48  # grey levels from the box's background that count as text
spent = 0.0  # seconds inside the engine, for run.json

_engines: dict = {}


def _rapid(lang: str):
    if lang not in _engines:
        from rapidocr import RapidOCR
        from rapidocr.utils.typings import LangRec, ModelType, OCRVersion

        # max_side_len: a wide region enlarged for small text is not shrunk back before detection
        _engines[lang] = RapidOCR(params={"Global.log_level": "error", "Global.max_side_len": 4096, "Rec.ocr_version": OCRVersion.PPOCRV5, "Rec.lang_type": LangRec(REC[lang]), "Rec.model_type": ModelType.MOBILE})
    return _engines[lang]


def use(name: str) -> None:
    global ENGINE, SPLIT
    ENGINE = name
    SPLIT = name == "vision"  # read a wide region also in two halves: Vision drops columns of sparse lists


use(os.environ.get("VRP_OCR", "rapidocr"))


def tight(gray: np.ndarray, b: list[float]) -> list[float]:
    """The box shrunk to the ink inside it; the background is the median of its border."""
    x0, y0 = max(0, int(b[0])), max(0, int(b[1]))
    x1, y1 = min(gray.shape[1], int(np.ceil(b[0] + b[2]))), min(gray.shape[0], int(np.ceil(b[1] + b[3])))
    p = gray[y0:y1, x0:x1]
    if p.shape[0] < 3 or p.shape[1] < 3:
        return b
    ys, xs = np.nonzero(np.abs(p - np.median(np.concatenate([p[0], p[-1], p[:, 0], p[:, -1]]))) > INK)
    if not len(xs):
        return b
    return [float(x0 + xs.min()), float(y0 + ys.min()), float(xs.max() - xs.min() + 1), float(ys.max() - ys.min() + 1)]


def read(img: Image.Image, lang: str) -> list[tuple[str, list[float]]]:
    global spent
    t0 = time.time()
    W, H = img.size
    if ENGINE == "vision":
        from ocrmac import ocrmac

        res = ocrmac.OCR(img, language_preference=VISION_LANGS[lang], recognition_level="accurate").recognize()
        out = [(t.strip(), [x * W, (1 - y - h) * H, w * W, h * H]) for t, c, (x, y, w, h) in res if c >= 0.3 and t.strip()]
    else:
        rgb = img.convert("RGB")
        r = _rapid(lang)(rgb)
        gray = np.asarray(rgb.convert("L"), dtype=np.int16)
        out = []
        for t, q in zip(r.txts or (), r.boxes if r.boxes is not None else ()):
            x0, y0 = q.min(0)
            x1, y1 = q.max(0)
            if t.strip():
                out.append((t.strip(), tight(gray, [float(x0), float(y0), float(x1 - x0), float(y1 - y0)])))
    spent += time.time() - t0
    return out
