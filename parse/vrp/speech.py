"""Speech: Whisper with per-word timings. Speakers are not separated yet - every utterance is Person1.

Greedy decoding (temperature 0) keeps the output deterministic. Whisper invents phrases on silence and noise; such
segments are dropped by its own signals: low word probability or far too many words for the segment length.
"""
import subprocess
from pathlib import Path

import mlx_whisper

MODEL = "mlx-community/whisper-large-v3-turbo"
MIN_WORD_PROB = 0.3
MAX_WORDS_PER_SEC = 7


def hallucinated(seg: dict) -> bool:
    words = seg.get("words", [])
    if not words:
        return True
    prob = sum(w.get("probability", 0) for w in words) / len(words)
    dur = max(seg["end"] - seg["start"], 0.05)
    return prob < MIN_WORD_PROB or len(words) / dur > MAX_WORDS_PER_SEC


def transcribe(video: Path, work: Path, lang: str) -> dict:
    wav = work / "audio.wav"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(video), "-ac", "1", "-ar", "16000", str(wav)], check=True)
    r = mlx_whisper.transcribe(str(wav), path_or_hf_repo=MODEL, language=lang, word_timestamps=True, condition_on_previous_text=False, temperature=0.0)
    utts = []
    for i, s in enumerate(r["segments"]):
        words = [{"w": w["word"].strip(), "start_ms": round(w["start"] * 1000), "end_ms": round(w["end"] * 1000)} for w in s.get("words", [])]
        text = s["text"].strip()
        if not text or hallucinated(s):
            continue
        utts.append({"id": f"u{i + 1:03d}", "speaker": "Person1", "start_ms": round(s["start"] * 1000), "end_ms": round(s["end"] * 1000), "text": text, "words": words})
    return {"speakers": [{"id": "Person1", "name": None, "tile": None}] if utts else [], "utterances": utts}
