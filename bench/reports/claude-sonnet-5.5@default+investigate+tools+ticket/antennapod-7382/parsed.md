# real/antennapod-7382

_claude-sonnet-5.5@default, 24 s; looked at: nothing_

The reporter says AntennaPod randomly skips ahead and points to 42:23 in the recording. The 30.7 s clip shows no skip. The position counter runs steadily from 41:57 to about 42:25 and the total stays 56:38. The reported bug is not demonstrated.

## Random skipping during playback (not visible in the recording)

Class: **intermittent**

Environment: AntennaPod full-screen player on a portrait phone (1080×2340). Episode from Strictly Stalking, total 56:38. Status bar shows 07:44, 58% battery, LTE and Bluetooth. The ticket says app 3.4.1, Android 14 and Samsung S23; none of that is visible in the video. No account is shown.

Steps:

1. The recording starts with the player open and the episode already playing at 41:57. Opening the episode and pressing play are not shown. (00:01.0; p001)
2. Playback continues with no visible jump, rewind or stall. The position reads 42:22 at 25.5 s. (00:25.5; p019)
3. The pause/play button area is tapped. The position reads 42:25 at 29.5 s, then the recording ends. (00:28.9; p020)

Expected (implied): Continuous playback with no forward jumps. The reporter asks for the skipping to be fixed or explained.

Actual: No skip is visible. The position advances at about 1 s per second and the end time does not shorten. The 30 s clip does not include a rewind to check whether the skip repeats. A skip may be audible only, or may not occur in this clip.

Key events: p019, p020

Missed by the author:

- The status bar network indicators change around 5.4 s, 20.9 s and 21.8 s (p003–p018). They could point to a network or streaming change but are unconfirmed.
- The speech heard (a person talking about a courtroom, u001–u005) is podcast or background audio and unrelated to the app. It is not a narration of the bug. The audio does not show a skip.

Claims:

- "Playback randomly skips forward during episodes." []: not shown - The position counter is continuous across the clip, from 41:57 to 42:25.
- "Something is visible at 42:23 in the recording." []: not shown - Playback passes 42:23 normally. The ticket's 42:23 may refer to the episode position rather than the recording time, or the skip is audio-only.
- "Rewinding to the skipped part reproduces the skip." []: not shown - No rewind is performed in the clip.
- "The end of the episode is shortened by the skips." []: not shown - The total duration stays at 56:38 throughout.
- "All podcasts are affected." []: not shown - Only one episode appears.
