# real/antennapod-7382

_claude-sonnet-5.5@default, 36 s; looked at: frames, frames/0000.0.jpg, frames/0005.0.jpg, frames/0010.0.jpg, frames/0015.0.jpg, frames/0020.0.jpg, frames/0025.0.jpg, frames/0030.5.jpg, frames/0027.0.jpg, frames/0028.5.jpg, frames/0026.0.jpg, frames/0029.5.jpg_

The reporter says AntennaPod 3.4.1 randomly skips forward in podcast episodes and points to 42:23 in the recording. The 30 s clip shows continuous playback from 41:56 to 42:25 and no visible skip. The reported bug is not demonstrated.

## Random skipping during playback (not visible in the recording)

Class: **intermittent**

Environment: AntennaPod full-screen player on an Android phone (Samsung S23, Android 14 and app 3.4.1 per the ticket, not visible in the video). Episode '242. Danger With A Stranger: Stalking Robin' from Strictly Stalking, 56:38 long, speed 1.00, rewind 10 s, forward 30 s. Wi-Fi and LTE are on, battery 58%, phone clock 07:44. No account is shown.

Steps:

1. The player is already open and playing the episode at 41:56. This is the start of the clip, so the earlier steps (opening the episode, pressing play) are not shown. (00:00.0; 0000.0)
2. Let it play. The position advances in real time (42:01, 42:06, 42:11, 42:16 at 5 s intervals) with no jump. (00:05.0; 0005.0, 0010.0, 0015.0, 0020.0)
3. Playback passes 42:21, 42:22 and 42:23 (the time the ticket cites) at 1 s per second, with no skip, rewind or stall. The status bar network icon changes around 25 s, which may be a Wi-Fi/data indicator change. (00:25.0; 0025.0, 0026.0, 0027.0)
4. At 42:25 playback is paused. I infer a tap on the pause button or the end of the recording, because a grey touch dot appears near the top right at 30.5 s. (00:29.5; 0028.5, 0029.5, 0030.5)

Expected (implied): Playback continues smoothly with no jumps forward. The ticket asks for the skipping to be fixed or explained.

Actual: In the 30.7 s clip, no skip is visible. The position moves 41:56 to 42:25 in about 29 s at normal speed, and the end time stays at 56:38. If a skip happens, it is not captured, or it is only audible (there is no sound in the frames).

Key events: 0000.0, 0020.0, 0025.0, 0027.0, 0029.5

Missed by the author:

- The network status icon changes at about 25 s (0025.0), when the Wi-Fi icon gains an activity arrow. This may point to streaming or buffering as the cause (unconfirmed).
- The phone is on mute (0000.0) and a Bluetooth icon is shown, so any audio skip may involve a Bluetooth output (unconfirmed).

Claims:

- "Playback randomly skips ahead, and rewinding to the skipped part repeats the skip." [It will just start skipping at random points during the podcast... If i try to rewind to listen to what was skipped, it reproduces the skip.]: not shown - The position counter advances continuously from 41:56 to 42:25 with no jump. No rewind is performed in the clip.
- "The problem is visible at 42:23 in the recording." [see 42:23 in screen recording below]: not shown - The clip is only 30 s long. It shows 42:22 to 42:25 playing normally, so the skip may be audio-only or may have been cut.
