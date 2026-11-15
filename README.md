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
- `bug` - what the parser must find: bug class, expected and actual, critical moments, traps.
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
  10-speech.json    utterances and word timings (Whisper)
  30-screens.json   screen region, cursor track, stable screen states: time, key frame, OCR text (Apple Vision)
  60-events.json    what appeared, disappeared, changed, which window came to the front, clicks and hovers;
                    how long something was shown (a 0.3 s toast)
  70-links.json     what a phrase refers to on the screen ("this one", "right here", "I click send")
  80-speakers.json  meetings: participant tiles and the tile lit during each utterance
  90-slides.json    which slide was on screen when; how attached pdf/pptx differ from what was shown
  evidence.json     everything together, format in parse/vrp/format.py
  timeline.md       timeline for an agent: time, event, id, evidence frame
  timeline.html     the same with the video, a screen-state strip and cut-outs
```

```sh
cd parse
uv venv --python 3.12 .venv && uv pip install --python .venv/bin/python numpy opencv-python-headless ocrmac mlx-whisper httpx rapidfuzz
.venv/bin/python truth.py           # generator ground truth -> truth/evidence.json and ground-truth timelines
.venv/bin/python run.py [key ...]   # parse (--variant low, --no-speech to skip the speech model)
.venv/bin/python evaluate.py        # compare with ground truth
.venv/bin/python report.py          # out/index.html
```

What was seen stays apart from what was inferred: every event has a source (`ocr`, `pixel`, `cursor`, `touch`,
`model`) and evidence frames. What the passes do:

- **regions** - in a meeting recording the shared screen is found as the largest area that is not the dark, unchanging
  meeting window; only that area is scanned and read, the people tiles are left out;
- **cursor** - the arrow is found by template (scale and polarity once per video), then followed near its last place
  and where the frame moved; its area is left out of frame comparison, so small changes (a status turning into a check
  mark) split the screen state and cursor moves do not;
- **screen states** - a change scanner over every frame at half size, plus a comparison with the state's key frame for
  changes that happened under the cursor; OCR of every stable state;
- **elements** - text that appeared or disappeared is grouped by its container (flood fill of the background around it:
  a bubble, a dialog, a menu), so a new message is one event with all its lines; a same-text area whose pixels changed
  is a `visual_change` (an icon, a mark); content that only moved and OCR reading the same pixels differently (a dimmed
  backdrop) are not changes;
- **window** - the front window is the one with coloured title-bar buttons, its title is the text next to them;
- **clicks and hovers** - a click is the cursor at rest and the screen reacting: right after it stopped, or later if
  the control under it changed; a hover is the cursor wiggling over one place after its approach slowed down; on a
  phone a round touch mark is a tap;
- **links** - words said during a click, a hover or a window switch are about its target; a pointing word ("this",
  "here") goes to what is being pointed at, else to what has just appeared, else stays unresolved; words that repeat a
  text on the screen are a mention of it;
- **speakers** - in a meeting the speaking tile is outlined; the outline is followed over the video, each tile's
  caption is read once, every utterance gets the tile lit during it (a room tile gives the room; a person in it is named
  only when they introduce themselves);
- **slides** - the slide number on screen ("3 / 6", "Slide 3 of 6") gives which slide was shown when, returns
  included; the words of the slide (title down to the footer) are compared with each page of the attached pdf and pptx.

Next: recognising app screens and returns to them beyond slides, telling apart people in one room tile by voice.

Known limitations:

- **480p** - small text is read with errors and the cursor jitters, so clicks there are unreliable; 720p and up is the
  target.
- **People in one room tile** - only the one who introduces themselves gets a name; the others stay "the room".
- **Links that need meaning** - "here as well" that refers back to an earlier phrase, or "this one" said while clicking
  something else, are not resolved by the rules above.
- **Ground truth of icon buttons** - the generator records the label of an icon button (Attach, Send) as its text,
  though nothing is written on screen; screen text below 100% on such videos is mostly that.

The evaluator (`evaluate.py`) reports: critical moments of the scenario, recall and precision of screen changes,
clicks (time and place), hovers, screen text (share of on-screen texts read at the right moment, this is where facts
that never change show up, like a garbled file name), links, speakers, slides, attached files and the word error rate
of the speech.

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
