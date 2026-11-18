---
name: video-bug-report
description: Turn a bug video (screen recording, often with a ticket) into a report a developer can act on, then reproduce the bug and go back to the video with specific questions when the repro does not match. Use when a ticket comes with a screen recording, or someone sends a video of a bug.
---

# Video bug report

A screen recording of a bug holds the exact steps, the moment it breaks and things the reporter did not write down.
This workflow gets them out with a deterministic parser and two model passes, then uses the video as evidence while
you reproduce the bug. Install once: `README.md` of this repository, section "Agent on top" (Python 3.12 venv in
`parse/`, `copilot` CLI signed in; works on macOS, Windows and Linux).

## 1. Report from the video and the ticket

```
parse/bin/vrp report path/to/video.mp4 --ticket path/to/ticket.md      # vrp.cmd on Windows
```

Save the ticket text to a file first (title, description, the reporter's own follow-ups). Without a ticket the report
comes from the video alone, which is weaker: on 54 real bug recordings the judges scored 83% with the ticket and 52%
without it (the ticket alone, without the video: 38%).

What it does, a few minutes per video:
1. **Parser** (no model): speech, screen states, cursor, clicks, hovers, what appeared, moved, flickered or flashed,
   cross-checks; written as `parsed/timeline.md` (for models) and `parsed/timeline.html` (for people, with frames).
2. **Watcher** (model, frames only): what looks wrong and when, without the parser's view.
3. **Investigator** (model): checks each of the watcher's points against the timeline and the frames, asks the video
   itself with the `vrp` commands below, and writes the report: steps with times, what happens, the moment that proves
   it, where the video and the ticket disagree, what stays unclear.

Output: `<video>.report.md` next to the video; the evidence is in `parsed/`.

## 2. Reproduce

Read the report, then try the steps in the app or against the code. Note the environment the report names (app,
version, account, settings seen on screen). The video is evidence of what happened, not of why: a setting, an account
or a step before the recording may matter.

## 3. When the repro does not match

Do not guess. Turn the difference into a question about a moment of the video and ask it, in `parsed/`:

```
vrp events --near 12.5 --window 1          what the timeline has around a moment
vrp look --from 4.0 --to 4.4 --box x,y,w,h --scale 3   every frame of a short span, cropped and enlarged (sheet.jpg)
vrp diff --box x,y,w,h --at 4.0 --to 4.4   how an area differs between two moments: brightness, drawing kept or new,
                                           text before and after, the two crops side by side
vrp ocr --at 4.2 --box x,y,w,h             the text in an area at a moment
vrp find --text "Connecting" --from 3 --to 6   every frame searched for a text: finds a state that lasts one frame
```

Typical questions:
- "Was the setting X on?" - `vrp ocr` or `vrp look` on the settings panel when it is on screen.
- "What exactly was clicked at 7 s?" - `vrp events --near 7`, then `vrp look` around it with the box of the target.
- "The error I get differs" - `vrp find --text` for the reporter's error text; compare word by word.
- "It works for me" - look for what differs before the first step: the account, the window size, the data on screen.

Re-read the ticket after each round: a detail that looked like noise may be the condition.

## 4. Stop

- **Reproduced** with the same symptom as the video: add a "Reproduction" section to the report (environment, steps,
  what you saw) and go on with the fix.
- **Not reproduced after three rounds** with no new fact from the video: stop and write what is known, what was tried
  and the questions for the reporter, each tied to a moment of the video ("at 0:12 the panel shows X - which build
  was this?").
- **The video contradicts the ticket**: say so with both, and ask the reporter before fixing either version.

## What it cannot see

Sound other than speech, anything off screen (other windows, devices, the server), keys pressed (inferred from what
changes, marked as a guess), a state shorter than one frame of the recording, and cause - only effects.
