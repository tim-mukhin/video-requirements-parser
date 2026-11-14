"""Reference voice for OmniVoice from a long recording: a clip up to a sentence end, no longer than max_sec, and its text.

python synth/tools/make_ref.py <recording.wav> <out.wav> [max_sec] [lang]
out.txt is written next to out.wav.
"""
import sys
from pathlib import Path

import mlx_whisper
import numpy as np
from mlx_audio.audio_io import read, write

src, dst = Path(sys.argv[1]), Path(sys.argv[2])
max_sec = float(sys.argv[3]) if len(sys.argv) > 3 else 10.0
lang = sys.argv[4] if len(sys.argv) > 4 else "en"
r = mlx_whisper.transcribe(str(src), path_or_hf_repo="mlx-community/whisper-large-v3-turbo", language=lang,
                           word_timestamps=True, condition_on_previous_text=False)
words = [w for s in r["segments"] for w in s.get("words", [])]
cut = None
for i, w in enumerate(words):
    if w["end"] > max_sec:
        break
    if w["word"].strip().endswith((".", "!", "?")):
        cut = i
if cut is None:
    sys.exit(f"no sentence end within {max_sec} s")
start = max(0.0, words[0]["start"] - 0.1)
end = words[cut]["end"] + 0.15
a, sr = read(str(src))
a = np.asarray(a, dtype=np.float32)
if a.ndim > 1:
    a = a.mean(axis=1)
dst.parent.mkdir(parents=True, exist_ok=True)
write(str(dst), a[int(start * sr):int(end * sr)], sr)
text = "".join(w["word"] for w in words[:cut + 1]).strip()
dst.with_suffix(".txt").write_text(text)
print(f"{dst} {end - start:.1f} s: {text}")
