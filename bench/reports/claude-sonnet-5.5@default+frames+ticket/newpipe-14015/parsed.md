# real/newpipe-14015

_claude-sonnet-5.5@default, 26 s; looked at: frames, frames/0000.0.jpg, frames/0003.0.jpg, frames/0006.0.jpg, frames/0009.0.jpg, frames/0012.0.jpg, frames/0015.0.jpg, frames/0018.0.jpg, frames/0021.0.jpg, frames/0023.5.jpg_

The video shows the regular YouTube app (not YouTube Kids). A video is shared to NewPipe from the three-dot menu, the player opens, and the video plays after a short spinner. The ticket's problem, a YouTube Kids video that cannot play, is not shown in this recording. The ticket mentions three recordings and this is only one of them.

## YouTube Kids video cannot play (not reproduced in this recording: a regular YouTube video plays in NewPipe)

Class: **not-a-bug**

Environment: Android phone, Vietnamese UI, recorded with Mobizen. The source app is the regular YouTube app (home feed, 'Tất cả' tab), not YouTube Kids. The target is NewPipe, which the ticket gives as version 0.29.2 on Android 8, Samsung Galaxy S7. The version number is not visible in the frames.

Steps:

1. On the YouTube app home feed, open the three-dot menu on a video. This is inferred: the menu is open at 3.0 s and the tap itself is not visible. (00:03.0; 0003.0)
2. Tap 'Chia sẻ' (Share). The Android share sheet then appears. This is inferred from the sheet showing at 6.0 s. (00:06.0; 0006.0)
3. Pick NewPipe. NewPipe's action dialog shows 'Trình phát video', 'Trình phát cửa sổ nổi', 'Trình phát trong nền', 'Tải xuống' and so on, with 'CHỈ MỘT LẦN' and 'LUÔN LUÔN' buttons. A video player entry (probably 'Trình phát video') is chosen. This is inferred. (00:09.0; 0009.0)
4. NewPipe opens: a blank screen first, then the player with a loading spinner. (00:12.0; 0012.0)
5. The video starts playing and keeps playing through the end of the clip. (00:15.0; 0015.0, 0018.0)

Expected (implied): A video shared from YouTube Kids opens and plays in NewPipe. The ticket does not state this; it is implied.

Actual: In this recording, a regular YouTube video plays normally in NewPipe after a few seconds of loading. No error, stuck state or failure is visible. The video does not show YouTube Kids at all.

Key events: 0003.0, 0009.0, 0012.0, 0015.0, 0018.0

Missed by the author:

- The source app is regular YouTube, not YouTube Kids (0000.0, 0003.0). The ticket's steps and actual behaviour are also empty ('See screen recordings' / 'No response'), so no failure is described.
- The NewPipe player works from the share action, with a loading spinner of about 1-2 s (0012.0, 0015.0).

Claims:

- "The YouTube Kids video cannot play in NewPipe." [ticket title: YouTube Kids video cannot play]: not shown - The source is the regular YouTube app and the video plays. The failure must be in the other two recordings, or it needs a YouTube Kids link. Nothing in these frames shows it.
