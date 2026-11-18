"""Text reading: RapidOCR (PaddleOCR models on ONNX Runtime) on any system, Apple Vision (ocrmac) as an option on a Mac.

VRP_OCR=rapidocr|vision picks the engine. read(img, lang) -> [(text, [x, y, w, h])] in the image's pixels, top-left origin.
RapidOCR: the multilingual PP-OCRv6 detector finds the lines, a PP-OCRv5 recognizer per language reads them (en: English
letters only, so an icon is not read as a CJK character; ru: East Slavic, Cyrillic and Latin). Its boxes are padded by a
few pixels around the line; they are shrunk to the ink inside, as tight as Vision's, since later passes compare the
pixels inside a text's box (a typed field: "diego@fa" keeps its pixels while "b" is added next to it).
"""
import hashlib
import os
import time

import numpy as np
from PIL import Image

ENGINE = SPLIT = None
VISION_LANGS = {"en": ["en-US"], "ru": ["ru-RU", "en-US"]}
REC = {"en": "en", "ru": "eslav"}
THREADS = 0  # ONNX threads per engine, 0 = all; set by the workers of screen.ocr_all
CACHE = 20000  # remembered line readings
INK = 48  # grey levels from the box's background that count as text
spent = 0.0  # seconds inside the engine, for run.json

_engines: dict = {}


def _rapid(lang: str):
    if lang not in _engines:
        from rapidocr import RapidOCR
        from rapidocr.utils.typings import LangRec, ModelType, OCRVersion

        # max_side_len: a wide region enlarged for small text is not shrunk back before detection
        r = RapidOCR(params={"Global.log_level": "error", "Global.max_side_len": 4096, "Rec.ocr_version": OCRVersion.PPOCRV5, "Rec.lang_type": LangRec(REC[lang]), "Rec.model_type": ModelType.MOBILE, **({"EngineConfig.onnxruntime.intra_op_num_threads": THREADS} if THREADS else {})})
        r.recognize_txt = _remembering(r.recognize_txt)
        _engines[lang] = r
    return _engines[lang]


def _remembering(recognize):
    """Recognition of each cut-out line, remembered by its pixels: between two states of a screen most lines are the
    same pixels, and reading a line is most of the time of reading a frame (1.1 of 1.3 s on a 1080p screen)."""
    from rapidocr.ch_ppocr_rec.typings import TextRecOutput

    seen: dict[bytes, tuple] = {}

    def run(imgs):
        if not imgs:
            return recognize(imgs)
        keys = [hashlib.blake2b(np.ascontiguousarray(im).tobytes(), digest_size=16, key=repr(im.shape).encode()).digest() for im in imgs]
        first: dict[bytes, int] = {}
        for i, k in enumerate(keys):
            if k not in seen:
                first.setdefault(k, i)
        todo = list(first.values())
        if todo:
            res = recognize([imgs[i] for i in todo])
            for i, t, sc, w in zip(todo, res.txts, res.scores, res.word_results):
                seen[keys[i]] = (t, sc, w)
            if len(seen) > CACHE:
                for k in list(seen)[: len(seen) - CACHE]:
                    del seen[k]
        got = [seen[k] for k in keys]
        return TextRecOutput(imgs=imgs, txts=tuple(g[0] for g in got), scores=[g[1] for g in got], word_results=tuple(g[2] for g in got), elapse=0.0)

    return run


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
