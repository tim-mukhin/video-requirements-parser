"""Voice a scenario's lines: OmniVoice (mlx-audio) one line at a time, Whisper checks the text and gives word timings.

python synth/tools/voice.py <lang>/<scenario-id> [l01,l02]
Needs out/<lang>/<id>/lines.json (npm run lines <lang>/<id>) and voices.local.json with reference voices.
"""
import difflib
import json
import re
import sys
from pathlib import Path

import mlx.core as mx
import mlx_whisper
import numpy as np
from mlx_audio.audio_io import write
from mlx_audio.tts.utils import load_model

ROOT = Path(__file__).resolve().parents[2]
SID = sys.argv[1]
ONLY = set(sys.argv[2].split(",")) if len(sys.argv) > 2 else set()
OUT = ROOT / "out" / SID / "voice"
OUT.mkdir(parents=True, exist_ok=True)
LINES = json.loads((ROOT / "out" / SID / "lines.json").read_text())
LANG = LINES[0]["lang"] if LINES else "en"
VOICES = json.loads((ROOT / "voices.local.json").read_text())
WHISPER = "mlx-community/whisper-large-v3-turbo"
# Whisper hallucinations on trailing silence
JUNK = re.compile(r"(Продолжение следует|Субтитры|Редактор субтитров|Спасибо за просмотр|Thank you for watching|Thanks for watching|Subtitles by)[^.]*\.*", re.I)


def norm(w):
    return re.sub(r"[^a-zа-я0-9]", "", w.lower().replace("ё", "е"))


def trim(a, sr, db=-45, pad=0.05):
    fr = int(sr * 0.01)
    e = np.array([np.sqrt(np.mean(a[i:i + fr] ** 2) + 1e-12) for i in range(0, len(a) - fr, fr)])
    on = np.where(20 * np.log10(e) > 20 * np.log10(e.max()) + db)[0]
    if not len(on):
        return a
    return a[max(0, on[0] * fr - int(pad * sr)):min(len(a), (on[-1] + 1) * fr + int(pad * sr))]


def hear(a, sr):
    tmp = OUT / "_check.wav"
    write(str(tmp), a, sr)
    r = mlx_whisper.transcribe(str(tmp), path_or_hf_repo=WHISPER, language=LANG, word_timestamps=True,
                               condition_on_previous_text=False)
    words = [w for s in r["segments"] for w in s.get("words", [])]
    words = [w for w in words if not JUNK.search(w["word"])]
    return JUNK.sub("", r["text"]).strip(), words


def align(text_words, heard, dur):
    # word timings of the script from Whisper's words; unmatched words are interpolated between neighbours
    a = [norm(w) for w in text_words]
    b = [norm(w["word"]) for w in heard]
    times = [None] * len(a)
    for blk in difflib.SequenceMatcher(None, a, b, autojunk=False).get_matching_blocks():
        for k in range(blk.size):
            h = heard[blk.b + k]
            times[blk.a + k] = (h["start"], h["end"])
    known = [i for i, t in enumerate(times) if t]
    for i, t in enumerate(times):
        if t:
            continue
        lo = max([k for k in known if k < i], default=None)
        hi = min([k for k in known if k > i], default=None)
        s = times[lo][1] if lo is not None else 0.0
        e = times[hi][0] if hi is not None else dur
        n = (hi if hi is not None else len(a)) - (lo if lo is not None else -1) - 1
        j = i - (lo if lo is not None else -1) - 1
        times[i] = (s + (e - s) * j / n, s + (e - s) * (j + 1) / n)
    return [{"start": round(s, 3), "end": round(e, 3)} for s, e in times], len(known) / max(1, len(a))


def score(text, said):
    return difflib.SequenceMatcher(None, " ".join(map(norm, text.split())), " ".join(map(norm, said.split())), autojunk=False).ratio()


vj = OUT / "voice.json"
done = json.loads(vj.read_text()) if vj.exists() else {}
# lines shifted (new ones inserted in the middle): audio with the same text moves to the new line id
by_text = {(v["text"], v.get("voice")): k for k, v in done.items() if v.get("text")}
moved = {}
for l in LINES:
    k = by_text.get((l["text"], l["voice"]))
    if k and k != l["id"] and done.get(l["id"], {}).get("text") != l["text"]:
        moved[l["id"]] = ((OUT / f"{k}.wav").read_bytes(), done[k])
for lid, (wav, entry) in moved.items():
    (OUT / f"{lid}.wav").write_bytes(wav)
    done[lid] = entry
ids = {l["id"] for l in LINES}
for k in [k for k in done if k not in ids]:
    del done[k]
    (OUT / f"{k}.wav").unlink(missing_ok=True)
if moved:
    vj.write_text(json.dumps(done, ensure_ascii=False, indent=1))
    print(f"reused lines: {len(moved)}", flush=True)

# a line is voiced again if its text or its voice changed
stale = lambda l: l["id"] not in done or done[l["id"]].get("text", l["text"]) != l["text"] or done[l["id"]].get("voice", l["voice"]) != l["voice"]
todo = [l for l in LINES if (l["id"] in ONLY) or (not ONLY and stale(l))]
if not todo:
    print("everything is voiced")
    sys.exit(0)

model = load_model("mlx-community/OmniVoice-bf16")
# without a limit the MLX cache grows with every line up to ~100 GB
mx.set_cache_limit(2 << 30)
mx.set_memory_limit(32 << 30)

for line in todo:
    v = VOICES[line["voice"]]
    kw = dict(language=LANG, num_steps=64, ref_audio=v["ref_audio"], ref_text=Path(v["ref_text"]).read_text().strip())
    text = line["text"]
    best = None
    for seed in range(42, 46):
        mx.random.seed(seed)
        parts, sr = [], None
        for r in model.generate(text=text, seed=seed, **kw):
            parts.append(np.asarray(r.audio, dtype=np.float32).reshape(-1))
            sr = r.sample_rate
        a = trim(np.concatenate(parts), sr)
        said, heard = hear(a, sr)
        sc = score(text, said)
        slow = len(a) / sr > 2.0 * len(text) / 14
        if not slow and (best is None or sc > best[0]):
            best = (sc, a, heard)
        print(f"[{line['id']}] seed {seed}: {sc:.2f}{' SLOW' if slow else ''} | {said}", flush=True)
        if sc >= 0.9 and not slow:
            break
    if best is None:
        best = (sc, a, heard)
    sc, a, heard = best
    dur = len(a) / sr
    words, matched = align(line["words"], heard, dur)
    write(str(OUT / f"{line['id']}.wav"), a, sr)
    mx.clear_cache()
    done[line["id"]] = {"text": text, "voice": line["voice"], "dur": round(dur, 3), "score": round(sc, 3), "matched_words": round(matched, 2), "words": words}
    vj.write_text(json.dumps(done, ensure_ascii=False, indent=1))
    print(f"{line['id']} {dur:.1f}s score {sc:.2f} words {matched:.0%}", flush=True)

(OUT / "_check.wav").unlink(missing_ok=True)
print(f"VODONE {len(done)} lines, {sum(d['dur'] for d in done.values()):.0f} s", flush=True)
