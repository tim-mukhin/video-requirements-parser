# real/newpipe-14015

_claude-sonnet-5.5@default, 25 s; looked at: frames/0012.0.jpg, frames/0020.0.jpg, frames/0015.0.jpg, frames/0023.5.jpg, frames/0017.0.jpg_

A video is shared from the regular YouTube app to NewPipe and plays after a long load of about 7 s. No error or failure is visible in this recording. The ticket's 'YouTube Kids video cannot play' is not shown here and may be in the other two recordings.

## YouTube Kids video cannot play (not reproduced in this recording)

Class: **not-a-bug**

Environment: Android phone with Vietnamese UI, screen recorded with Mobizen. Source app is the regular YouTube app (home feed, 'Tất cả' tab), not YouTube Kids. Target is NewPipe, which the ticket gives as 0.29.2 on Android 8, Samsung Galaxy S7. The version is not visible on screen. The video is 240x426 and has no cursor; only one tap mark is seen.

Steps:

1. In the YouTube app feed, a video's three-dot menu is open (Save, Download, Share, and so on). The tap that opened it is not visible. (00:01.9; p006)
2. The Android share sheet is shown, with NewPipe among the targets. The tap on Share is not visible. (00:03.1; p008, p027)
3. NewPipe's action dialog opens, with the video player, popup player, background player and download options. The choice made is not visible. (00:08.4; p040)
4. NewPipe opens: a blank screen first, then the video page with the player area showing a loading spinner. Playback does not start for about 7 s. (00:10.0; p042, p043, p044)
5. A tap at [213,311] is shown. Playback starts, a frame is visible by 17 s, and it continues to the end of the clip at 23.9 s. (00:13.4; p048, p053)

Expected (implied): A YouTube Kids video shared to NewPipe opens and plays. This is implied by the ticket title; the ticket's expected and actual fields are empty.

Actual: A regular YouTube video plays in NewPipe after a long spinner (about 7 s, frames at 12 s to 17 s). No error, stuck state or failure is seen. The video does not show YouTube Kids at all.

Key events: p040, p042, p044, p048, p053

Missed by the author:

- The source app is regular YouTube, not YouTube Kids (p006, p027).
- The loading spinner lasts about 7 s before playback starts (p042 to p053).
- The ticket gives no steps, expected result or actual result, and the version is not visible in the video.

Claims:

- "The YouTube Kids video cannot play in NewPipe (ticket title)." [ticket]: not shown - The source is the regular YouTube app and the video plays. The failure may be in the other two recordings, or may need a YouTube Kids link.
- "The speaker's only utterance is a channel-subscribe plug (u001), which comes from the source video's audio." [u001]: not shown - It says nothing about the problem.
