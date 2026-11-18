# real/antennapod-7382

_claude-sonnet-5.5@default, 21 s; looked at: nothing_

During playback of any podcast in AntennaPod 3.4.1, the audio skips ahead at random points, so parts of the episode are never heard and the episode ends early. Rewinding to the skipped part skips it again, so the user can't listen to that content. The ticket has no logs, and its recording isn't available.

## Playback randomly skips ahead on all podcasts; rewinding to the skipped part skips it again

Class: **intermittent**

Environment: AntennaPod 3.4.1 from Google Play; Samsung Galaxy S23; Android 14. Reporter says it happens on all their podcasts and first occurred at least a year ago. No podcast URL, account or settings are given.

Steps:

1. Press play on any podcast episode. (00:00.0; )
2. Listen. At random points playback skips ahead, and the episode ends earlier by the amount skipped. (00:00.0; )
3. Rewind to hear the skipped part. The same skip happens again. (00:00.0; )
4. The reporter says the problem is visible at 42:23 in their screen recording. The recording isn't available here. (00:00.0; )

Expected (implied): Playback continues without skipping any content, and rewinding replays the audio that was passed over.

Actual: Playback jumps over parts of the audio at seemingly random points. Rewinding to a skipped part skips it again, and the episode finishes early by the total skipped time.

Key events: 

Claims:

- "Happens on all podcasts" [This issue happens on all my podcasts]: not shown - No video or podcast list is available. Only the reporter's statement supports it.
- "The skip is reproducible at the same position after rewinding" [If i try to rewind to listen to what was skipped, it reproduces the skip.]: not shown - This is only in the text. It may point to the audio file or a decoder issue at that position, not a random one.
- "The episode end is shortened by the number of skips" [the end of the podcast will be shortened depending on how many skips occured]: not shown - No measurements are given.
