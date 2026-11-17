# video-requirements-parser

Turn work videos - a screen recording of a bug repro, a meeting with slides - into facts an agent can reason about:
what was on screen and when, what popped up, what was said and by whom, what "this one" pointed at. Facts first, with
time and evidence frames; conclusions (a bug report, requirements) are a separate step on top.

The repo has two parts:

- `synth/` - a **generator of synthetic test videos with ground truth**. Every fact in a generated video is known in
  advance, so the parser can be measured instead of eyeballed.
- `parse/` - the **parser**: video → facts in one format → a timeline for an agent and a page with frames for a human.

An index of all generated videos with links and scores: `out/index.html`.

## Why synthetic videos

To check a parser you need videos where you know exactly what happens: which windows, where each button is, when an
error flashed, what "right here" refers to, what a meeting decided versus only proposed. Hand-labelling real recordings
is slow and imprecise. Here it is the other way round: the video is rendered from a scenario, so every fact is known.

One scenario produces:

- a video: HTML apps in windows, a cursor, clicks, typing (Remotion);
- voices: narration and meeting participants, cloned voices (OmniVoice), word timings from Whisper;
- files shown in a meeting: `pptx` and `pdf` from the same slide description;
- ground truth in the same format the parser outputs;
- quality variants (resolution, frame rate, compression, noise) with the same ground truth;
- every scenario in two languages: English and Russian.

## Scenario format

`scenarios/*.ts`, type `Scenario` in `synth/format/scenario.ts`. A scenario is a function of the language;
`t('English', 'Russian')` picks the string.

```ts
steps: [
  { say: t('Diego asked for the report. I click the [paperclip](click:a/attach) and pick the file.', '…') },
  { act: { click: 'a/file:q3' } },
  { say: t("The file is attached, I'm [sending](click:a/send#send) it.", '…') },
  { sys: 'b', op: { incoming: { /* … */ blocked } }, at: 'send', delay: 1.6, name: 'arrive' },
  { say: t('I try to [open](click:b/msg:r1#open) it.', '…') },
]
```

- `say` - a spoken line (`who` - speaker, `name` - to reference it from the ground truth). Markup
  `[phrase](kind:target#name)` ties an action to words: the click happens on the first word of the phrase, so the
  scenario survives a faster or slower voice. Kinds: `click`, `focus` (bring a window forward), `point` (the cursor
  moves over an element while the phrase lasts), `ref` (speech refers to an element without an action), `ref:?` (a
  reference the video cannot resolve: the right answer is `unresolved`).
- `act` - a silent user action: `click`, `focus`, `point`, `key` (only its effect is visible, e.g. a slide change),
  `type` (typing character by character).
- `sys` - a system reaction: what changed on screen without the user (a toast, a status, an incoming message, a setting
  silently reverting). `at` - the anchor the delay counts from, `ms` - when the effect goes away.
- `bug` - what the parser must find: bug class, expected and actual, critical moments, traps, and `checks` - what the
  cross-checks must flag (`unmentioned`, `revert`, `covered`, `claim` at a step name).
- `requirements` - for meetings: requirements with status `stated`, `proposed`, `decided`, `rejected`,
  `open_question`, who proposed, who decided, which utterances they rest on.
- `decks`, `attachments` - slides and files attached to the video; `overrides` makes an attached file differ from what
  was shown.
- `difficulty` - axes: speech (explicit, deictic, contradicting the screen, silent, vague - the way people really talk:
  no context, pauses, guesses), error signal (modal, a 0.3 s toast, an inline change, nothing), number of windows,
  occlusion, distractors, attempts.

Surfaces:

- **desktop** - app windows on a desktop, a cursor;
- **browser** - `browser` on a window: tabs (windows of one `group`), an address bar, DevTools with console and network
  (`sys` ops `devtools`, `console`, `network`);
- **phone** - `device: 'phone'`: a portrait screen, status bar, mobile layout, touch marks instead of a cursor;
- **meeting recording** - `recording`: the presenter's screen fitted into the frame, people in a strip on top or a
  column on the right; a tile per person or a meeting room with drawn figures, the speaking tile is highlighted. Only
  the screen is meant to be parsed: its region is in `manifest.json` → `regions`.

The apps are fictional: Relay (messenger, desktop and mobile), Vault (file storage), Relay Meet (meetings), Deck (a
slide editor: normal view with ribbon, thumbnails and notes, or a full-screen slide show). Each app is a model (state
and a reducer for clicks, keys, typing and system events) plus an HTML view; UI labels live in `synth/i18n.ts`.
Elements are addressed as `<window>/<element>` (the `data-el` attribute). Coordinates are never written by hand: before
rendering, Remotion walks every screen state and reads boxes, text, role and visibility (`visible`, `occluded`,
`out_of_view`) from the DOM. The cursor moves along the same boxes.

## Building the videos

```sh
npm install
synth/tools/all.sh                            # every English scenario (LANGS=en,ru for both): voice, video, variants, ground truth
synth/tools/all.sh en/b1-xtenant-file         # one scenario, key = <lang>/<id>
npm run stills en/m3-meeting-long-room 12 42  # quick frames without rendering a video
npm run studio                                # Remotion Studio (after a build)
```

Step by step: `npm run lines <key>` (narration text) → `python synth/tools/voice.py <key>` (voice) →
`npm run build <key>`. Without voice `build` still works: word timings are estimated from text length and the video is
silent.

Voices are configured in `voices.local.json` (not in git), see `voices.example.json`. If a voice has `source`, its
reference clip is cut from that recording automatically (`synth/tools/make_ref.py`). The voicing Python needs `mlx-audio` and
`mlx-whisper` (Apple Silicon); point `VOICE_PY` at it in `.env.local`. `all.sh` runs in two lanes: voicing in one pass under a shared heavy-model lock
`VOICE_LOCK` (default `/tmp/dad-render.lock`), video builds in their own queue `BUILD_LOCK` as soon as a scenario's
voice is ready. Both wait for 40% free memory. Logs: `out/_logs/`.

Finished videos sit flat in `out/<lang>/` so it is easy to switch between them; everything intermediate is in
`out/<lang>/<id>/`:

```
out/<lang>/<id>.mp4                master with audio
out/<lang>/<id>.<variant>.mp4      quality variants (low, small)
out/<lang>/<id>/
  attachments/                     pptx and pdf "attached" to the video
  manifest.json                    difficulty, environment, variants, box scale, screen/people regions, traps
  truth/transcript.json            utterances, speakers, word timings
  truth/speakers.json              who speaks: tile, name if it is said in the video, otherwise Person1, Person2
  truth/ui-states.json             screen snapshots: windows, elements, boxes, visibility
  truth/timeline.json              actions, system reactions, UI changes, speech - on one axis
  truth/links.json                 "right here" → element or unresolved
  truth/report.json                bug report: steps, expected, actual, critical moments with durations
  truth/requirements.json          meeting requirements with status and evidence
  truth/slides.json                which slide was on screen when, how attached files differ from what was shown
  truth/evidence.json              all of the above in the parser format (parse/truth.py)
```

## Parser

Every pass writes its own file, no LLM involved; deterministic code assembles them into one story. A pass is
recomputed only when the video or the pass version changes.

```
out/<lang>/<id>/parsed/
  run.json          video hash, pass versions, timings
  10-speech.json    utterances and word timings (Whisper large-v3-turbo: mlx-whisper on a Mac, faster-whisper elsewhere)
  30-screens.json   screen region, cursor track (position and shape), stable screen states: time, key frame, OCR text (RapidOCR or Vision)
  50-motion.json    every frame against the one before: areas that moved (dx, dy), areas that went back to a look
                    they had up to a second ago
  60-events.json    what appeared, disappeared, changed, which window came to the front, clicks and hovers, typing;
                    how long something was shown (a 0.3 s toast); moves, scrolls, drags and flicker
  70-links.json     what a phrase refers to on the screen ("this one", "right here", "I click send")
  80-speakers.json  meetings: participant tiles and the tile lit during each utterance
  85-voices.json    who speaks when as voice ids (pyannote diarization), the voice of each utterance
  90-slides.json    which slide was on screen when; how attached pdf/pptx differ from what was shown
  95-checks.json    cross-checks: an error nobody mentions, a value that went back, a change behind the front window,
                    claims the video does not show
  evidence.json     everything together, format in parse/vrp/format.py
  timeline.md       timeline for an agent: cross-checks first, then time, event, id, evidence frame
  timeline.html     the same with the video, a screen-state strip and cut-outs
```

```sh
cd parse
uv venv --python 3.12 .venv && uv pip install --python .venv/bin/python -r pyproject.toml
.venv/bin/python truth.py           # generator ground truth -> truth/evidence.json and ground-truth timelines
.venv/bin/python run.py [key ...]   # parse (--variant low, --no-speech skips speech, --tag x -> parsed-x)
.venv/bin/python evaluate.py        # compare with ground truth (--variant, --tag as for run.py)
.venv/bin/python report.py          # out/index.html
```

### Windows and Linux

Nothing in the parser needs macOS. Text is read by RapidOCR (PaddleOCR models on ONNX Runtime) everywhere, speech by
faster-whisper (the same large-v3-turbo) off the Mac, pdf text by pypdfium2. On a Mac `--ocr vision` (Apple Vision) and
mlx-whisper stay available; `VRP_OCR=rapidocr|vision`, `VRP_ASR=mlx|faster-whisper` and `VRP_ASR_DEVICE=cpu|cuda`
set the same from the environment. No ffmpeg binary is needed: OpenCV's wheel decodes the video, PyAV inside
faster-whisper the audio (mlx-whisper on a Mac still calls `ffmpeg`).

Windows (PowerShell), Python 3.12:

```powershell
winget install --id=astral-sh.uv -e      # or: pip install uv
cd parse
uv venv --python 3.12 .venv
uv pip install --python .venv\Scripts\python.exe -r pyproject.toml
.venv\Scripts\python.exe run.py en/b1-xtenant-file
.venv\Scripts\python.exe evaluate.py en/b1-xtenant-file
```

The first run downloads the OCR models (about 20 MB, from modelscope.cn, into the rapidocr package) and Whisper
(about 1.6 GB, from Hugging Face, into the user cache). Speech runs on the CPU unless CTranslate2 finds CUDA; with an
NVIDIA card but no cuBLAS/cuDNN 9 installed, set `VRP_ASR_DEVICE=cpu` (or `uv pip install nvidia-cublas-cu12
nvidia-cudnn-cu12`). Keep the repository on a path of Latin letters: OpenCV does not open files under a path like
`C:\Users\Артём\...` on Windows. Linux is the same with `.venv/bin/python`; it was checked in a `python:3.12-slim`
container.
Voices need `pyannote.audio` 4 (pip on all systems, CPU torch is enough); its model (31 MB) comes from the ungated
`pyannote-community/speaker-diarization-community-1` copy on Hugging Face, no token or licence click. The audio is
handed to it in memory, so torchcodec's FFmpeg libraries are not needed. `VRP_VOICES_DEVICE=cpu|cuda|mps` picks the
device (default CUDA, then MPS, then CPU).

Measured against the same ground truth, Apple Vision + mlx-whisper (before) and RapidOCR + faster-whisper (now):

| | 21 masters, before | 21 masters, now | 10 at 720p, before | 10 at 720p, now |
|---|---|---|---|---|
| critical moments | 54/54 | 54/54 | 26/26 | 26/26 |
| screen changes: recall / precision | 93.5% / 78.8% | 94.2% / 85.1% | 95.5% / 74.8% | 95.0% / 76.2% |
| clicks / click precision | 100% / 100% | 99.2% / 100% | 98.2% / 100% | 98.2% / 100% |
| hovers | 100% | 100% | 91.7% | 91.7% |
| screen text | 95.4% | 95.7% | 95.0% | 95.5% |
| links | 52/57 | 51/57 | - | - |
| speakers, slides, attached files | 100% | 100% | 100% | 100% |
| cross-checks | 23/25 | 23/25 | 3/3 | 3/3 |
| speech WER | 1.4% (0-5) | 1.4% (0-5) | - | - |

The one click lost is R3: after the press on "Restricted" the label under the cursor reads garbled; Vision reads it
as different text, which is what marked the press, RapidOCR as the same word. The link lost is the same click.
faster-whisper gives the same words as mlx-whisper on all 21 videos (punctuation and segment breaks differ) and the
same word timings (median difference 0 ms); on Linux its transcripts are byte-identical to the Mac's. So RapidOCR is
the default on every system and Vision is only an option. RapidOCR needed three things the later passes rely on:
its line boxes are shrunk to the ink (they come padded), a one- or two-character "text" under the resting cursor is
the arrow itself, and a text with the same pixels in the same place has not moved however it was read.


What was seen stays apart from what was inferred: every event has a source (`ocr`, `pixel`, `cursor`, `touch`,
`model`) and evidence frames. What the passes do:

- **regions** - in a meeting recording the shared screen is found as the largest area that is not the dark, unchanging
  meeting window; only that area is scanned and read, the people tiles are left out;
- **cursor** - its sprites are learnt from the video itself: where only a small area moves over three frames, the
  middle frame shows the cursor; cut-outs are grouped by shape and the pixels that stay the same over many backgrounds
  become a template per shape (arrow, hand, I-beam), so any theme, size and recorder works, a 10 px arrow too. The
  drawn arrow template (scale and polarity once per video) stays for the generated videos; portrait (phone) videos
  learn nothing. The cursor is followed near its last place and where the frame moved, and its shape goes into the
  track, clicks and hovers ("hand cursor" over a link); its area is left out of frame comparison, so small changes (a
  status turning into a check mark) split the screen state and cursor moves do not;
- **screen states** - a change scanner over every frame at half size, plus a comparison with the state's key frame for
  changes that happened under the cursor; OCR of every stable state;
- **elements** - text that appeared or disappeared is grouped by its container (flood fill of the background around it:
  a bubble, a dialog, a menu), so a new message is one event with all its lines; a same-text area whose pixels changed
  is a `visual_change` (an icon, a mark); content that only moved and OCR reading the same pixels differently (a dimmed
  backdrop) are not changes;
- **motion** - stable states miss what settles fast: a menu that jumps, a page that shifts for one frame. Every frame
  is compared with the one before at small size, the cursor left out; each changed area gets the shift that explains
  most of its changed pixels (phase correlation, a clear peak only, so text lines that merely look alike do not
  count). Moves of one area close in time are one episode: `move` ("21 px right and back 33 ms later", "14 px right
  in one frame"), `scroll` (a quarter of the screen or more moving up or down), `drag` (the content follows the
  cursor: from, to, what was under the end point, what changed in 1.5 s after the drop, or "nothing changed"). Content
  sliding in as it appears is the appearing, not a move; a highlight the recorder draws around the cursor (one size
  of thing following it all over the screen) is left out. Content that only moved is still not a change of content.
  A menu that jumps far at once (its lines go in one place and three or more of them come up in another at the same
  moment) is a `move` from one box to the other, its lines are not "disappeared". A new element of three lines or more
  whose box reaches the right or bottom edge of the screen says so, as a guess that it is cut off there; an icon or
  colour change with no text of its own names the text right next to it on the same line (a typed backtick OCR does
  not read: 'just right of "return zero, key)"');
- **flicker** - one place going back to how it looked a moment ago (within 0.4 s) four or more times is one `flicker`
  event with the count and the span, and the appear/disappear/change events it made there are dropped; the cursor
  switching between two tracked shapes the same way, some of the times without moving, is a cursor flicker;
- **typing** - text growing in one field is one `type` event; OCR reads typed symbols and the caret badly, so a
  single-line field whose text keeps changing by a character or two (emptied in between, a trailing caret "|" left
  out) is typing too, with the values read in order; digits alone changing is a counter, not typing;
- **window** - the front window is the one with coloured title-bar buttons, its title is the text next to them;
- **clicks and hovers** - a click is the cursor at rest and the screen reacting: right after it stopped, or later if
  the control under it changed; a hover is the cursor wiggling over one place after its approach slowed down; on a
  phone a round touch mark is a tap;
- **links** - words said during a click, a hover or a window switch are about its target; a pointing word ("this",
  "here") goes to what is being pointed at, else to what has just appeared, else stays unresolved; words that repeat a
  text on the screen are a mention of it;
- **speakers** - in a meeting the speaking tile is outlined; the outline is followed over the video, each tile's
  caption is read once, every utterance gets the tile lit during it (a room tile gives the room, not the person);
- **voices** - who speaks when, from the sound: pyannote `speaker-diarization-community-1` finds the voices and their
  centroid embeddings, then every utterance is embedded on its own and takes the nearest centroid (Voice1, Voice2 ...);
  where the diarization turns show a second voice inside an utterance for a second or more, each part is assigned the
  same way and the utterance keeps its parts. A small margin to the second-nearest voice is marked "voice in doubt".
  Names are facts with their source, next to the voice: introduced themselves ("This is Lucas"), addressed by name and
  answered ("Lucas, are you in the meeting room?" and the next other voice), the lit tile; a heard name is matched
  fuzzily against names on screen ("Lucas" heard, "Lukas" shown). A voice with none of these is "name unknown"; a tile
  lit for several voices is said so. Who is who is the agent's call: `SAID Voice2 (tile "Room 4", introduced as
  "Lucas")`;
- **slides** - the slide number on screen ("3 / 6", "Slide 3 of 6") gives which slide was shown when, returns
  included; the words of the slide (title down to the footer) are compared with each page of the attached pdf and pptx;
- **cross-checks** - what no single pass sees: an error text on screen with nothing like it said around it (a 0.3 s
  toast, a 403 in DevTools); a short value that went back to what it was a moment ago with no click since it changed
  (access "link" → "private"); a change in a window partly covered by the front one (found by the title-bar buttons:
  coloured on the front window, grey on the others); a sentence with a claim marker ("maybe", "used to", "he says",
  "on the computer") that no text on screen around it backs. Claims are skipped in meetings, where "maybe" is a proposal.

Voices on the 21 English masters (`run.py --tag voices`, `evaluate.py --tag voices`). The metric is per utterance:
each true utterance gets the predicted speaker overlapping it most, predicted and true speakers are paired one to one
(best mapping), and only utterances on a pair count, so a room tile or a merged voice is credited to one person only.
The old tile metric (`spkr`) gave 100% everywhere because it credited the room tile to both people in it.

| | tiles (before) | pyannote turns alone | voices (now) |
|---|---|---|---|
| 14 bug videos, 1 voice each | - | a second voice in 5 of 14 (r1: half the utterances) | 100%, 1 voice in all 14 |
| M1, M2, M4, 2 voices | 100%, 2/2 | 100%, 2/2 | 100%, 2/2 |
| M3, 4 voices, 2 of them in one room tile | 88%, 3/4 found | 80%, 4/4 found | 100%, 4/4 found |
| M3 name facts | none ("This is" missed) | - | 3/3 right: introduced and twice addressed as "Lucas" |

pyannote's own turns misplace whole utterances when voices are alike (an 11 s reply of one person given to another);
embedding each Whisper utterance and taking the nearest pyannote centroid fixes all of these here. The voices pass
takes 1-16 s per master on Apple MPS (M3, 5.5 minutes of audio: 16 s); the CPU gives the same turns (checked on M1)
but was not timed on a quiet machine (155 s for 100 s of audio while the Mac was saturated by other jobs). Real
recordings, no ground truth: the Rocket.Chat bug video (52 s, one narrator) gives one voice; the Wikidata bug triage
(41 minutes, an Indonesian host, an English-speaking product manager and a few participants) gives two voices that
match host and manager, the participants who speak briefly are folded into them (Whisper 91 s, voices 117 s on MPS).

Next: recognising app screens and returns to them beyond slides.

### Agent on top

The parser stops at facts. `parse/agent.py` turns them into a bug report (summary, class, minimal repro steps citing
event ids, expected and actual, claims with a verdict, what the author missed) or meeting requirements (status, who
proposed, who decided). The agent is GitHub Copilot CLI in headless mode, run inside the parsed folder with only its
file viewer: it reads `timeline.md`, opens frames when a doubt needs one (the click in B6 lands on a clock icon that has
no text), cannot run commands or reach the ground truth. Its answer is JSON against a schema.

```sh
.venv/bin/python agent.py --model claude-sonnet-5.5 [--effort low] [key ...]   # -> parsed/agent/<model>@<effort>.json, .md
.venv/bin/python agent_eval.py [--detail <model>@<effort>]                      # ids and times against the ground truth
.venv/bin/python judge.py --report <model>@<effort> --judge gpt-6-sol            # a second model grades the text
```

`agent_eval.py` needs no model: bug class, critical moments covered by the cited events, claims and unmentioned
errors from `bug.checks`, meeting requirements found and their status. `judge.py` grades what ids cannot: repro steps,
actual result, verdict (meetings: coverage, status, attribution), 0-2 each, and lists invented statements; it does not
take points for details the video never shows (a text cut off by an ellipsis).

21 English masters, two judges of different families (GPT-6 Sol and Claude Sonnet 5.5), Copilot premium requests per
video:

| model @ effort | critical | claims | missed errors | meeting status | judges (Sol / Sonnet) | invented per video (Sol / Sonnet) | s per video | requests |
|---|---|---|---|---|---|---|---|---|
| Claude Opus 5.5 | 58/59 | 15/16 | 5/5 | 29/35 | 89% / 88% | 0.7 / 1.9 | ~35 | 15 |
| Claude Opus 5.5 @ low | 59/59 | 15/16 | 4/5 | 24/35 | 89% / 87% | 0.7 / 2.2 | 21 | 15 |
| Claude Sonnet 5.5 | 58/59 | 15/16 | 5/5 | 26/35 | 92% / 91% | 0.6 / 2.2 | 18 | 1 |
| Claude Sonnet 5.5 @ low | 58/59 | 15/16 | 5/5 | 26/35 | 87% / 88% | 0.7 / 2.1 | 17 | 1 |
| Claude Haiku 5.5 | 59/59 | 14/16 | 5/5 | 27/35 | 89% / 90% | 0.8 / 1.9 | 30 | 1 |
| Claude Haiku 5.5 @ high | 59/59 | 14/16 | 5/5 | 23/35 | 87% / 90% | 0.8 / 1.7 | 49 | 1 |
| GPT-6 Sol | 58/59 | 15/16 | 5/5 | 32/35 | 88% / 90% | 0.3 / 1.0 | 21 | 1 |
| GPT-6 Luna | 58/59 | 15/16 | 5/5 | 30/34 | 84% / 83% | 0.3 / 0.7 | 29 | 1 |
| GPT-6 Luna @ low | 58/59 | 14/16 | 5/5 | 29/35 | 85% / 79% | 0.3 / 1.0 | 15 | 1 |
| Gemini 3.8 Flash | 56/59 | 15/16 | 5/5 | 35/35 | 93% / 89% | 0.7 / 1.2 | 80 | 14 |
| Gemma 4 E4B, local (Ollama) | 46/59 | 2/16 | 5/5 | 17/24 | 55% / 52% | 1.9 / 2.7 | 66 | 0 |
| Qwen3-VL 8B, local (Ollama) | 48/59 | 15/16 | 4/5 | 13/21 | 53% / 47% | 2.0 / 2.8 | 221 | 0 |
| Mistral Small 3.2 24B, local (Ollama) | 47/59 | 15/16 | 5/5 | 10/16 | 54% / 48% | 1.5 / 2.4 | 108 | 0 |

Local models run through the same Copilot CLI (`agent.py --local`: Ollama on this machine, 32k context). At 8B they
are not enough: they never open a frame, drop steps and requirements, and get half the judges' score. Mistral Small 3.2
24B does open frames (6 per video) but scores the same half and ends 2 of 21 videos without an answer: on this machine
the local models are a fallback for privacy, not a match for the cheapest hosted ones.

What it says: the timeline carries the facts well enough that a small hosted model finds them - Haiku and Luna at low effort
cover the same critical moments, claims and missed errors as Opus; more effort does not help. The models differ in
judgement, not in facts: meeting statuses (proposed or still open) and who proposed what. Where every model loses
points the cause is mostly upstream: two people in one room tile are not told apart (M3), and whether a block by an
organization policy is a bug or the policy working (B1, P1) is a judgement the ground truth makes one way and most
models the other. Class labels are a weak signal for the same reason (a 0.3 s toast is "error-shown" to some models,
"silent-fail" to the ground truth).

Known limitations:

- **Russian** - the parser targets English. The Russian scenarios are rendered, but the parser is not measured on
  them: PP-OCRv6 has no Cyrillic, and the PP-OCRv5 East Slavic model turns Latin words inside Russian text into
  look-alike Cyrillic ("Contoso" -> "Соптоsо"), so Russian would need both recognizers per line.
- **480p** - small text is read with errors and the cursor jitters, so clicks there are unreliable; 720p and up is the
  target. RapidOCR loses more there than Vision: in B3 at 480p its detector does not find the bold file name on the
  blue "Sending…" bubble at all.
- **Voices** - voices are told apart by sound (see "Voices" above), names stay facts. Weak spots: a short reply glued
  to the previous speaker's utterance by Whisper ("About" of the next speaker, M3 u017) is split at the wrong word and
  marked in doubt; a person addressed by a name nobody else confirms (not introduced, not on screen) gets no name fact;
  the name rules are English only; on a quiet machine the CPU speed is not measured yet (Windows/Linux without CUDA).
- **Speech against an icon** - "I click Send" while the clock icon next to it is clicked (B6): the button has no text on
  screen, so no cheap check sees the mismatch; the evidence frame of the click is there for a model to look at.
- **Claims without a marker** - "the connection is fine, websites open" is a claim about something off screen, but it
  has no word that gives it away; a word list does not find it.
- **Links that need meaning** - "here as well" that refers back to an earlier phrase, or "this one" said while clicking
  something else, are not resolved by the rules above.
- **Ground truth of icon buttons** - the generator records the label of an icon button (Attach, Send) as its text,
  though nothing is written on screen; screen text below 100% on such videos is mostly that.

The evaluator (`evaluate.py`) reports: critical moments of the scenario, recall and precision of screen changes,
clicks (time and place), hovers, screen text (share of on-screen texts read at the right moment, this is where facts
that never change show up, like a garbled file name), links, speakers, slides, attached files, cross-checks (marks in
the scenario's `bug.checks` found, plus flags with no mark) and the word error rate of the speech.

Ground-truth markup that does not change the video (`bug.checks`, `critical`, names of steps) is rewritten without
rendering: `node --experimental-strip-types synth/tools/truth.ts <key> ...` takes the DOM snapshot from `props.json`
and refuses if the scenario's timing no longer matches the rendered video.

## Scenarios

Each exists in `en` and `ru`.

| id | What | What makes it hard |
|---|---|---|
| `b1-xtenant-file` | A file from Contoso arrives at Fabrikam with a lock, opening it says "File unavailable" | easy: explicit speech, modal dialog |
| `b2-xtenant-toast` | The file never arrives, the sender sees "sent", the error is a 0.3 s toast | deictic speech, overlapping windows, a calendar notification, "here" without a referent |
| `b3-xtenant-mojibake` | A non-ASCII file name turns into mojibake on the recipient side | no error at all: only comparing the text of two windows shows it |
| `b4-upload-stuck` | The first file goes through, the second one in a row hangs at 99% | intermittent, "every other time" is only claimed |
| `b5-share-revert` | "Anyone with the link" silently reverts after "Save" | the access icon in the list changes for a second, nobody says it |
| `b6-wrong-button` | "I click Send", but "Schedule send" is clicked | not a bug: speech contradicts the screen |
| `b7-hidden-error` | An invitation to an external user fails, the error is in a covered window | three windows, the error is truncated and behind another window |
| `w1-web-share-403` | Vault in a browser: "saved", but DevTools shows PATCH 403 | the cause is only in the console and network panel, never spoken |
| `w2-web-tabs-duplicate` | Relay in a browser, two tabs: the recipient gets the file twice | one window whose content depends on the tab; the second copy arrives in a hidden tab |
| `p1-phone-blocked-file` | Recipient's phone: a file with a lock, a "File unavailable" alert | portrait video, touches instead of a cursor, a notification banner |
| `p2-phone-send-retry` | Phone: "Not sent", "Retry", fails again | a retry, claims that are not shown |
| `r1-live-no-access` | Live speech: "he says it won't open", only the sender's window is visible | that the recipient is external is only visible in a banner; the error is the recipient's text |
| `r2-live-resend` | Live speech: "it went out on my side", an error flashes twice and the author misses it | 0.3 s toasts never mentioned, a guess "something on their side" |
| `r3-live-share-fumble` | Live speech: wrong file first, hovering without clicks, "I set this thing", access reverts | extra actions are not repro steps, the mode is never named |
| `r4-live-name-not-found` | Live speech: "he can't find the file", the recipient's file name is garbled | the author does not see the cause and names a wrong one |
| `r5-live-wrong-chat` | Live speech: "Diego didn't get it", the file went to the team chat | not a bug: the user error is visible only in the chat header |
| `r6-phone-wrong-hypothesis` | Phone: "the file must be too big", but the bigger file goes through | the author's conclusion is refuted by sizes on screen |
| `m1-meeting-requirements` | A meeting with 2 voices and 6 slides: a table, "this column here", a return to slide 2 | proposals vs decisions, open questions |
| `m2-meeting-stale-pdf` | The same meeting, but the attached `pdf` has an old slide without the "Status" column | what was shown differs from what was attached |
| `m3-meeting-long-room` | A 5-minute meeting: 4 voices, a meeting room with two people, a full-screen slide show, people on top | one slide stays for 2.5 minutes, decisions override the slides, rejected and postponed items, an unnamed Person1 |
| `m4-meeting-editor-share` | Meeting M1 shared as the whole screen with a slide editor, people on the right | ribbon and thumbnails around the slide; the notes say "decided", the meeting keeps it open |

All organizations, people and apps are fictional.
