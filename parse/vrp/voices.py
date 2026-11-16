"""Voices: who speaks when, as voice ids (Voice1, Voice2 ...), never as names.

pyannote speaker-diarization-community-1 (the ungated pyannote-community copy, CC-BY-4.0, no token needed) finds the
voices and gives each a centroid embedding. Its own turns misplace whole utterances when voices are alike, so every
Whisper utterance is embedded on its own (the same WeSpeaker model) and takes the nearest centroid; when the turns show
a second voice inside an utterance for at least MIN_PART_MS, each part is embedded and assigned the same way, and the
utterance keeps its parts. The margin to the second-nearest centroid is kept as a measure of doubt. A voice that never
wins an utterance stays only in the turns. Runs on CUDA, Apple MPS (same turns as the CPU, ~9x faster) or the CPU
(VRP_VOICES_DEVICE=cpu|cuda|mps); the audio is decoded by PyAV and passed in memory, so torchcodec and an ffmpeg
library are not needed.

Names are facts with their source, never a verdict: the person introduced themselves ("This is Lukas"), was addressed
by name and a voice answered ("Lukas, are you there?"), or a tile with a caption was lit. Who is who is left to the
reader of the timeline.
"""
import os
import re
import time
from functools import cache
from pathlib import Path

from rapidfuzz import fuzz

from .speech import _audio

MODEL = "pyannote-community/speaker-diarization-community-1"
ENGINE = "pyannote-community-1"
NEAR_MS = 500  # a word outside every turn takes the nearest turn this close
MIN_PART_MS = 1000  # a voice part shorter than this inside an utterance is not a second voice
MIN_EMB_MS = 1000  # shorter audio is widened around its middle before embedding
DOUBT = 0.1  # margin to the second-nearest voice below this: the voice is in doubt
ANSWER_MS = 6000  # an answer to a call by name starts this soon after it
INTRO = re.compile(r"(?:^|[.!?,]\s+)(?i:this is|it's|it is|i'm|i am|my name is)\s+([A-Z][a-z]+)(?=\s*(?:[,.!?]|$|\s+(?:from|here|speaking)\b))")
CALL = re.compile(r"(?:^|[.!?]\s+)([A-Z][a-z]+),\s+[^.!?]*\?|,\s+([A-Z][a-z]+)\?")


def device() -> str:
    import torch

    return os.environ.get("VRP_VOICES_DEVICE") or ("cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu")


@cache
def pipeline(dev: str):
    import torch
    from pyannote.audio import Pipeline

    return Pipeline.from_pretrained(MODEL).to(torch.device(dev))


def voice_at(turns: list[dict], a: int, b: int) -> str | None:
    """The turn overlapping [a, b] most; with no overlap, the nearest turn within NEAR_MS."""
    best = max(turns, key=lambda t: min(b, t["end_ms"]) - max(a, t["start_ms"]), default=None)
    return best["voice"] if best and min(b, best["end_ms"]) - max(a, best["start_ms"]) > -NEAR_MS else None


def split(u: dict, turns: list[dict]) -> list[dict]:
    """Runs of words with one voice; a run shorter than MIN_PART_MS joins its longer neighbour."""
    words = u["words"] or [{"w": u["text"], "start_ms": u["start_ms"], "end_ms": u["end_ms"]}]
    runs: list[dict] = []
    for w in words:
        v = voice_at(turns, w["start_ms"], w["end_ms"])
        if runs and runs[-1]["voice"] == v:
            runs[-1]["end_ms"], runs[-1]["words"] = w["end_ms"], runs[-1]["words"] + [w["w"]]
        else:
            runs.append({"voice": v, "start_ms": w["start_ms"], "end_ms": w["end_ms"], "words": [w["w"]]})
    while len(runs) > 1:
        i = min(range(len(runs)), key=lambda k: runs[k]["end_ms"] - runs[k]["start_ms"] if runs[k]["voice"] else -1)
        r = runs[i]
        if r["voice"] and r["end_ms"] - r["start_ms"] >= MIN_PART_MS:
            break
        j = i - 1 if i == len(runs) - 1 or (i > 0 and runs[i - 1]["end_ms"] - runs[i - 1]["start_ms"] >= runs[i + 1]["end_ms"] - runs[i + 1]["start_ms"]) else i + 1
        n = runs[j]
        a, b = (n, r) if j < i else (r, n)
        runs[min(i, j)] = {"voice": n["voice"], "start_ms": a["start_ms"], "end_ms": b["end_ms"], "words": a["words"] + b["words"]}
        del runs[max(i, j)]
        k = 1
        while k < len(runs):
            if runs[k]["voice"] == runs[k - 1]["voice"]:
                runs[k - 1] = {**runs[k - 1], "end_ms": runs[k]["end_ms"], "words": runs[k - 1]["words"] + runs[k]["words"]}
                del runs[k]
            else:
                k += 1
    return [{"voice": r["voice"], "start_ms": r["start_ms"], "end_ms": r["end_ms"], "text": " ".join(r["words"])} for r in runs]


def diarize(video: Path, utterances: list[dict]) -> dict:
    """-> {engine, device, seconds, turns: [{start_ms, end_ms, voice}], utterances: {id: {voice, margin, parts?}}},
    voices numbered by first appearance in speech."""
    if not utterances:  # no speech, or no audio track at all
        return {"engine": ENGINE, "device": None, "seconds": 0.0, "turns": [], "utterances": {}}
    import numpy as np
    import torch

    audio = _audio(video)
    t0 = time.time()
    pipe = pipeline(device())
    out = pipe({"waveform": torch.from_numpy(audio)[None], "sample_rate": 16000})
    labels = out.speaker_diarization.labels()
    cent = np.nan_to_num(np.asarray(out.speaker_embeddings, dtype=np.float32)[: len(labels)])
    cent /= np.linalg.norm(cent, axis=1, keepdims=True) + 1e-9
    turns = [{"start_ms": round(t.start * 1000), "end_ms": round(t.end * 1000), "voice": spk} for t, _, spk in out.exclusive_speaker_diarization.itertracks(yield_label=True)]

    def nearest(a: int, b: int) -> tuple[str, float]:
        c = (a + b) // 2
        a, b = min(a, c - MIN_EMB_MS // 2), max(b, c + MIN_EMB_MS // 2)
        e = np.nan_to_num(pipe._embedding(torch.from_numpy(audio[max(0, a * 16):b * 16])[None, None])[0])  # the pipeline's own WeSpeaker model
        sim = cent @ (e / (np.linalg.norm(e) + 1e-9))
        k = np.argsort(sim)[::-1]
        return labels[k[0]], round(float(sim[k[0]] - sim[k[1]]) if len(k) > 1 else 1.0, 2)

    raw: dict[str, list[dict]] = {}
    for u in utterances if labels else []:
        parts: list[dict] = []
        for p in split(u, turns):
            v, m = nearest(p["start_ms"], p["end_ms"])
            if parts and parts[-1]["voice"] == v:
                parts[-1].update(end_ms=p["end_ms"], text=parts[-1]["text"] + " " + p["text"], margin=min(m, parts[-1]["margin"]))
            else:
                parts.append({**p, "voice": v, "margin": m})
        raw[u["id"]] = parts
    names: dict[str, str] = {}
    for v in [p["voice"] for ps in raw.values() for p in ps] + [t["voice"] for t in sorted(turns, key=lambda t: t["start_ms"])]:
        names.setdefault(v, f"Voice{len(names) + 1}")
    for t in turns:
        t["voice"] = names[t["voice"]]
    utts = {}
    for uid, parts in raw.items():
        dur: dict[str, int] = {}
        for p in parts:
            p["voice"] = names[p["voice"]]
            dur[p["voice"]] = dur.get(p["voice"], 0) + p["end_ms"] - p["start_ms"]
        utts[uid] = {"voice": max(dur, key=dur.get), "margin": min(p["margin"] for p in parts), **({"parts": parts} if len(parts) > 1 else {})}
    return {"engine": ENGINE, "device": device(), "seconds": round(time.time() - t0, 1), "turns": turns, "utterances": utts}


def on_screen(name: str, words: set[str]) -> str | None:
    """The spelling of a heard name seen on screen ("Lucas" heard, "Lukas" shown), if any."""
    best = max(words, key=lambda w: fuzz.ratio(name.lower(), w.lower()), default=None)
    return best if best and fuzz.ratio(name.lower(), best.lower()) >= 80 else None


def facts(evidence: dict, assigned: dict, tiles: dict) -> None:
    """Puts on every utterance its voice, the lit tile and name facts with their source; sums them up per voice.
    tiles: {utterance id: tile caption} from the speakers pass."""
    utts = evidence["speech"]["utterances"]
    seen = {w for s in evidence["screens"] for t in s.get("texts", []) for w in re.findall(r"[A-Z][a-z]{2,}", t["text"])}
    seen |= {w for c in tiles.values() for w in re.findall(r"[A-Z][a-z]{2,}", c or "")}
    for u in utts:
        a = assigned.get(u["id"]) or {"voice": None}
        u["voice"] = a["voice"]
        u["speaker"] = a["voice"] or "unknown"
        if a["voice"] and a["margin"] < DOUBT:
            u["voice_doubt"] = a["margin"]
        if a.get("parts"):
            u["parts"] = a["parts"]
        if tiles.get(u["id"]):
            u["tile"] = tiles[u["id"]]
        u["names"] = []
    known: set[str] = set(seen)
    for u in utts:
        for m in INTRO.finditer(u["text"]):
            voice = next((p["voice"] for p in u.get("parts", []) if m.group(1) in p["text"]), u["voice"])
            f = {"name": m.group(1), "source": "introduced", "voice": voice}
            if (s := on_screen(m.group(1), seen)) and s != m.group(1):
                f["on_screen"] = s
            u["names"].append(f)
            known.add(m.group(1))
    for i, u in enumerate(utts):
        for m in CALL.finditer(u["text"]):
            name = m.group(1) or m.group(2)
            if not any(fuzz.ratio(name.lower(), k.lower()) >= 80 for k in known):
                continue
            caller = u.get("parts", [{}])[-1].get("voice") or u["voice"]
            ans = next((v for v in utts[i + 1:] if v["start_ms"] - u["end_ms"] <= ANSWER_MS and v["voice"] and v["voice"] != caller), None)
            if ans:
                ans["names"].append({"name": name, "source": "addressed", "voice": ans["voice"], "by": u["id"]})
    voices: dict[str, dict] = {}
    for u in utts:
        for p in u.get("parts") or [{"voice": u["voice"], "start_ms": u["start_ms"], "end_ms": u["end_ms"]}]:
            v = voices.setdefault(p["voice"] or "unknown", {"id": p["voice"] or "unknown", "utterances": 0, "seconds": 0.0, "tiles": {}, "names": []})
            v["seconds"] = round(v["seconds"] + (p["end_ms"] - p["start_ms"]) / 1000, 1)
        v = voices[u["voice"] or "unknown"]
        v["utterances"] += 1
        if u.get("tile"):
            v["tiles"][u["tile"]] = v["tiles"].get(u["tile"], 0) + 1
        for f in u["names"]:
            voices[f["voice"] or "unknown"]["names"].append({k: x for k, x in {**f, "utterance": u["id"]}.items() if k != "voice"})
    shared = {}
    for v in voices.values():
        for t in v["tiles"]:
            shared.setdefault(t, []).append(v["id"])
    for v in voices.values():
        v["shares_tile"] = {t: [o for o in shared[t] if o != v["id"]] for t in v["tiles"] if len(shared[t]) > 1}
    evidence["speech"]["speakers"] = sorted(voices.values(), key=lambda v: (v["id"] == "unknown", len(v["id"]), v["id"]))


def label(u: dict) -> str:
    """SAID Voice2 (tile "Room 4", introduced as "Lucas", shown as "Lukas")."""
    bits = [f'voice in doubt, margin {u["voice_doubt"]:.2f}'] if "voice_doubt" in u else []
    bits += [f'tile "{u["tile"]}"'] if u.get("tile") else []
    for f in u.get("names", []):
        how = f'introduced as "{f["name"]}"' if f["source"] == "introduced" else f'addressed as "{f["name"]}" in {f["by"]}'
        who = f'{f["voice"]} ' if u.get("parts") else ""
        bits.append(who + how + (f' (on screen "{f["on_screen"]}")' if f.get("on_screen") else ""))
    who = " then ".join(dict.fromkeys(p["voice"] or "unknown" for p in u["parts"])) if u.get("parts") else u["speaker"]
    return who + (f" ({', '.join(bits)})" if bits else "")


def summary(evidence: dict) -> list[str]:
    """One line per voice for the head of the timeline."""
    out = []
    for v in evidence["speech"].get("speakers", []):
        if "seconds" not in v:
            continue
        bits = [f'{v["utterances"]} utterances, {v["seconds"]:.0f} s']
        if v["tiles"]:
            bits.append("lit tile " + ", ".join(f'"{t}" {n}×' for t, n in v["tiles"].items()))
        for t, others in v["shares_tile"].items():
            bits.append(f'tile "{t}" also lit for {", ".join(others)}')
        names = [f'{"introduced as" if f["source"] == "introduced" else "addressed as"} "{f["name"]}" [{f["utterance"]}]' + (f' (on screen "{f["on_screen"]}")' if f.get("on_screen") else "") for f in v["names"]]
        bits.append("; ".join(names) if names else "name unknown")
        out.append(f'{v["id"]}: ' + "; ".join(bits))
    return out
