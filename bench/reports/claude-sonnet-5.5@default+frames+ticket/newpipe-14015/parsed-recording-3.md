# real/newpipe-14015

_claude-sonnet-5.5@default, 27 s; looked at: frames/0000.0.jpg, frames/0003.0.jpg, frames/0006.0.jpg, frames/0009.0.jpg, frames/0012.0.jpg, frames/0015.0.jpg, frames/0018.0.jpg, frames/0021.0.jpg, frames/0024.0.jpg, frames/0027.0.jpg, frames/0031.5.jpg, frames/0004.5.jpg, frames/0019.5.jpg, frames/0020.5.jpg_

In NewPipe 0.29.2 (Vietnamese UI), some videos from the feed fail with 'Content not available' and a ContentNotAvailableException report. Other feed videos, for example the Asphalt 8 one, play normally. The failing videos are from the POPS Kids channel (YouTube Kids content, per the ticket title).

## Some feed videos (YouTube Kids content) fail to load with 'Content not available' / ContentNotAvailableException

Class: **error-shown**

Environment: NewPipe 0.29.2 (org.schabi.newpipe), Android 8.0.0, Samsung Galaxy S7, Vietnamese UI, 'What's new' feed tab, screen recorded with Mobizen.

Steps:

1. Open the 'Cỏ gì mới' (What's new) feed tab. (00:00.0; 0000.0)
2. Tap the 'Dining with Doraemon Series #218' (POPS Kids) item (inferred tap). The player view opens with a spinner. (00:04.5; 0004.5)
3. The page shows a sad face and 'Nội dung không khả dụng' (Content not available) with Report, Retry and Open in browser buttons. (00:06.0; 0006.0)
4. The error report screen ('Báo lỗi') opens, apparently from the Report button (inferred). It shows org.schabi.newpipe 0.29.2 and a ContentNotAvailableException stack trace from the YoutubeStreamExtractor. The reporter scrolls through it. (00:09.0; 0009.0, 0012.0)
5. Back on the feed, the 'Race Beyond the Road | Old Asphalt 8' (Cym64) item is tapped. It loads and plays. (00:15.0; 0015.0, 0018.0)
6. Back on the feed, the 'Candyko's Quiz Adventure: Christmas' (POPS Kids) item is tapped. It fails with the same 'Content not available' error. (00:21.0; 0021.0, 0024.0, 0027.0)

Expected (implied): Feed videos from YouTube Kids content should load and play like the other videos.

Actual: The POPS Kids videos (Doraemon, Candyko) show 'Content not available' and a ContentNotAvailableException report. The Cym64 video plays, though it also shows a spinner at 0020.5.

Key events: 0006.0, 0012.0, 0024.0, 0018.0

Missed by the author:

- The Asphalt 8 video from a regular channel plays fine, so the failure only affects some videos (0018.0).
- The stack trace says the content is not available, which points to the extractor rather than the network (0012.0).

Claims:

- "YouTube Kids video cannot play" [YouTube Kids video cannot play (ticket title)]: confirmed - Two POPS Kids videos fail with a content-unavailable error. The screen never says they are YouTube Kids content, and I infer that from the channel name and the ticket title.
