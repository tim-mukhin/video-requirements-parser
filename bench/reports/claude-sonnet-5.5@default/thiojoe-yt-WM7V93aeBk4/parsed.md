# real/thiojoe-yt-WM7V93aeBk4

_claude-sonnet-5.5@default, 30 s; looked at: nothing_

The author demos a YouTube bug. Thumbnail progress overlays (Watch Later playlist, iOS app) show wrong watched time. A half-watched video (7:51 of 20:53) shows as 100% complete, and scrolling alone can change the overlays. He argues the fault is on the server side, and in some cases a UI bug. Users can't tell which videos they have finished, and creators' watch time suffers.

## YouTube thumbnail progress overlay shows wrong watched progress (often 100%) in playlists, while the player resumes at the correct position

Class: **wrong-data**

Environment: YouTube on iOS (the author says the official app) and a YouTube desktop/browser view of the Watch Later playlist (private, 193 videos), a Twitter/X thread on ThioJoe's account with replies, and a screen recording with commentary. The video does not show a reproduction on a clean account. A single speaker (Voice1) is heard.

Steps:

1. Open a video that was only partly watched. The player shows 7:51 / 20:53 and the true-progress overlay reads 'Only ~Half'. (00:19.2; p020, p022, p030)
2. Show the same video in the Watch Later playlist, where the thumbnail overlay shows it as completed ('Only half watched' versus the playlist thumbnail). (00:32.3; p068, u007)
3. Open the playlist (193 videos) and click into a video. The player opens at the correct position (1:43 / 36:05) even though the thumbnail overlay was wrong. (00:52.4; p076, p114, p123, u011)
4. On iOS, scrolling the playlist alone changes the overlays (the author's description of the UI-bug variant). (06:35.4; u082, u083)

Expected (implied): Thumbnail progress overlays should match the real watched position, for example about half for a half-watched video, and should not show 100% for unfinished videos.

Actual: Overlays show the wrong progress, often 100% complete, in the playlist and on thumbnails, and sometimes change when scrolling. The player itself resumes at the correct time, so only the overlay and the stored or served completion data are wrong.

Key events: p020, p022, p030, p068, p076, p123, u011, u080, u082

Missed by the author:

- The screen state when entering the playlist shows the overlay text for the first video as 'Watch later 2/193' with the clicked video at 1:43 / 36:05 [p123]. This is a concrete example of the true position versus the overlay.

Claims:

- "The wrong progress affects thumbnails only; the video itself always resumes at the correct position." [u080]: confirmed - After clicking into the playlist video the player shows a real resume time (1:43 / 36:05) [p123].
- "It is 100% a server-side bug in some cases, and a UI bug on iOS in others. It is not caused by DNS or network filtering because it also happens on cellular." [u088]: not shown - The cellular test and the server/UI attribution are the author's inference. The screen shows nothing about network or server behaviour.
- "Usually the bug can be fixed by refreshing the playlist, but not always." [u018]: not shown - The cross-check found nothing on screen supporting this.
- "Overlays show 100% completed until you take some further action." [u020]: not shown - The cross-check found nothing on screen supporting this.
- "Twitter users say it happens to them too, and one says autoplay or hovering marks videos as watched." [u071]: not shown - A reply from @shouse59 is displayed [p1347], but it is another person's claim, not a reproduction.
- "It is not just 100% that is wrong; other values are wrong too, and videos that were previously correct later become wrong after scrolling." [u038]: not shown - The author describes this; the parsed events do not independently verify it.
