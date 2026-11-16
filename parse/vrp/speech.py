"""Speech: Whisper large-v3-turbo with per-word timings. Every utterance is Person1 here; the voices pass tells speakers apart.

VRP_ASR=mlx|faster-whisper picks the engine: mlx-whisper on Apple Silicon, faster-whisper (CTranslate2; CUDA when
present, else CPU; VRP_ASR_DEVICE=cpu forces the CPU) elsewhere. Greedy decoding (temperature 0) keeps the output
deterministic. Whisper invents phrases on silence and noise; such segments are dropped by its own signals: low word
probability or far too many words for the segment length.
"""
import os
import platform
import subprocess
import sys
from pathlib import Path

ENGINE = os.environ.get("VRP_ASR") or ("mlx" if sys.platform == "darwin" and platform.machine() == "arm64" else "faster-whisper")
MODEL = {"mlx": "mlx-community/whisper-large-v3-turbo", "faster-whisper": "large-v3-turbo"}
MIN_WORD_PROB = 0.3
MAX_WORDS_PER_SEC = 7


def hallucinated(seg: dict) -> bool:
    words = seg.get("words", [])
    if not words:
        return True
    prob = sum(w.get("probability", 0) for w in words) / len(words)
    dur = max(seg["end"] - seg["start"], 0.05)
    return prob < MIN_WORD_PROB or len(words) / dur > MAX_WORDS_PER_SEC


def _mlx(video: Path, work: Path, lang: str | None) -> list[dict]:
    import mlx_whisper

    wav = work / "audio.wav"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(video), "-ac", "1", "-ar", "16000", str(wav)], check=True)
    r = mlx_whisper.transcribe(str(wav), path_or_hf_repo=MODEL["mlx"], language=lang, word_timestamps=True, condition_on_previous_text=False, temperature=0.0)
    return r["segments"]


def _audio(video: Path):
    """16 kHz mono float samples through PyAV, no ffmpeg binary (faster_whisper.decode_audio breaks on PyAV 19)."""
    import av
    import numpy as np

    rs = av.AudioResampler(format="s16", layout="mono", rate=16000)
    with av.open(str(video)) as c:
        chunks = [f.to_ndarray() for frame in c.decode(audio=0) for f in rs.resample(frame)]
    chunks += [f.to_ndarray() for f in rs.resample(None)]
    return np.concatenate(chunks, axis=1).reshape(-1).astype(np.float32) / 32768.0


def _faster_whisper(video: Path, lang: str | None) -> list[dict]:
    from faster_whisper import WhisperModel

    audio = _audio(video)
    model = WhisperModel(MODEL["faster-whisper"], device=os.environ.get("VRP_ASR_DEVICE", "auto"), compute_type="default")
    segs, _ = model.transcribe(audio, language=lang, beam_size=1, best_of=1, temperature=0.0, word_timestamps=True, condition_on_previous_text=False, vad_filter=False, multilingual=lang is None)
    return [{"start": s.start, "end": s.end, "text": s.text, "words": [{"word": w.word, "start": w.start, "end": w.end, "probability": w.probability} for w in s.words or []]} for s in segs]


def transcribe(video: Path, work: Path, lang: str | None) -> dict:
    """lang None: detect the language (faster-whisper per segment, so mixed speech keeps both languages)."""
    import av

    with av.open(str(video)) as c:
        if not any(s.type == "audio" for s in c.streams):  # screen recordings often have no sound at all
            return {"speakers": [], "utterances": [], "no_audio": True}
    segments = _mlx(video, work, lang) if ENGINE == "mlx" else _faster_whisper(video, lang)
    utts = []
    for i, s in enumerate(segments):
        words = [{"w": w["word"].strip(), "start_ms": round(w["start"] * 1000), "end_ms": round(w["end"] * 1000)} for w in s.get("words", [])]
        text = s["text"].strip()
        if not text or hallucinated(s):
            continue
        utts.append({"id": f"u{i + 1:03d}", "speaker": "Person1", "start_ms": round(s["start"] * 1000), "end_ms": round(s["end"] * 1000), "text": text, "words": words})
    return {"speakers": [{"id": "Person1", "name": None, "tile": None}] if utts else [], "utterances": utts}
