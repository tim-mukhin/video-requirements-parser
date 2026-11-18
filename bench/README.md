# bench: real bug videos, labels and every judgement

The test set behind the "How well it works on real bug videos" table in the main README. The videos themselves are
not here (attachments of public bug trackers and YouTube, private testing only); `source.json` has the URL of each.

- `real/<id>/source.json` - where the recording comes from, the issue's expected report, difficulty.
- `real/<id>/ticket.md` - the ticket as the reporter filed it: title, opening post, the reporter's own follow-ups
  before anyone else replied (49 tickets for 55 recordings; several recordings can share one issue).
- `real/<id>/visible[-<stem>].json` - what the frames of that recording show, labelled frame by frame: control or
  not, shows the bug yes / partly / no, visible steps with times, the decisive moment, what the ticket says that the
  video does not show.
- `judgements.json` - every judge verdict: `"<run>|<agent configuration>|<truth>"` -> recording -> judge -> steps,
  actual, verdict (and video in the ticket setting), notes, invented statements. Runs: `current` (the files in `out/`
  when this was saved), `real-v1`..`real-v6` (no ticket, the parser rounds of 17 Nov), `invtt-v1`..`v4` (ticket +
  watcher + investigator with `vrp`, prompt and evidence variants), `syn-*` (synthetic masters).
- `reports/<configuration>/<recording>.md` - the agent's reports for the main configurations.

## Results (Claude Sonnet 5.5 as the agent, GPT-6 Sol and Claude Sonnet 5.5 as judges, 2026-11-18)

Ticket + video, judged on steps, actual, verdict and what the video added (0-2 each):

| agent input | score |
|---|---|
| the ticket alone | 38% |
| ticket + parser timeline | 69% |
| ticket + frames (watcher) | 77% |
| ticket + watcher + investigator with `vrp` | 83% |
| the same on GPT-6 Sol | 83% (half the invented statements, 47 s instead of 31 s) |

Video alone, judged against what the frames show: parser timeline 41%, frames 42%, both at once 44%, watcher +
investigator 47%, with `vrp` 52%.

What did not move the score (full set, one run each; the run-to-run spread is about ±2 points on the full set and
±5 on a group of 10-15): rules for minimal steps and certainty (82%), strips of frames around short events in the
timeline (83%), every frame around short events among the watcher's frames (79%, worse), another model (83%).

Found and fixed on the way: the parser counted time as frame number / fps, and 31 of 55 recordings write frames
unevenly - times were off by up to 3.9 s; a status shown for one frame (25 ms) was merged into the next screen state.
The rerun with both fixed (`current` in `judgements.json`): 83%, the same; on the 31 re-timed recordings 80 -> 82%,
within the spread - the investigator takes its times mostly from the watcher's frames, which always used the real
time. The scheme stays at 82-83% across prompt, evidence, model and timing changes.

Two lessons for anyone measuring an agent this way:
- A subset picked because it failed improves on a rerun without any change (regression to the mean): 14 failing
  recordings went 68 -> 74% while the other 40 went 89 -> 84%. Compare on the full set.
- Judges favour their own family by about 2 points; two judges of different families cancel it out.
