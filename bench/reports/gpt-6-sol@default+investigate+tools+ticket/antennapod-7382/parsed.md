# real/antennapod-7382

_gpt-6-sol@default, 40 s; looked at: frames/0000.0.jpg, frames/0021.0.jpg, frames/0027.0.jpg, frames/moments/p016.jpg, frames/moments/p018.jpg, frames/moments/p005.jpg, frames/moments/p014.jpg, frames/moments/p015.jpg, frames/0026.5.jpg, frames/000260.jpg, frames/crops/p019.jpg, frames/crops/p020.jpg, frames/0028.0.jpg, frames/0005.5.jpg_

The reporter describes podcast audio skipping near 42:23, but the video does not establish whether audio was omitted. The player advances normally through that point, so the reported audible problem remains unconfirmed rather than refuted.

## Reported audio skips during podcast playback without a visible position jump

Class: **silent-fail**

Environment: AntennaPod playing Strictly Stalking, episode “242. Danger With A Stranger: Stalking Robin,” at 1.00×. The ticket reports version 3.4.1 from Google Play on a Samsung Galaxy S23 with Android 14; those details are not visible in the video.

Steps:

1. With the episode already playing, let playback continue toward 42:23; the action that started playback is not visible. (00:01.1; u001)
2. Continue playback through the displayed 42:23 point. (00:26.5; u005, p019)

Expected (implied): Podcast audio plays continuously without omitting content.

Actual: The displayed position progresses from 41:56 through 42:23 without a visible jump. Playback is subsequently paused at 42:25 [p019, p020]. The transcript does not establish whether an audible skip occurred.

Key events: u001, u004, u005, p019, p020

Missed by the author:

- The player shows 1.00× speed and a fixed 56:38 duration while the displayed position advances normally through 42:23 [u005, p019].
- The touch at the central playback control is followed by a paused player at 42:25, not a rewind [p019, p020].
- The timeline's brief battery-text change and clock-area flickers are status-bar rendering changes in their moment strips, not playback-position jumps [p005, p014, p015, p018].

Claims:

- "Playback skips at random points, including around 42:23." [ticket.md: “It will just start skipping at random points ... see 42:23 in screen recording below.”]: not shown - The position advances normally through 42:23; the recognized speech does not establish whether audio was omitted.
- "Rewinding reproduces the skip." [ticket.md: “If i try to rewind to listen to what was skipped, it reproduces the skip.”]: not shown - No rewind is shown.
- "Skips shorten the end of the episode." [ticket.md: “the end of the podcast will be shortened depending on how many skips occured.”]: not shown - The recording ends well before the displayed 56:38 episode duration.
- "The issue happens on all podcasts." [ticket.md: “This issue happens on all my podcasts.”]: not shown - Only one episode is shown.
