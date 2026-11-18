# real/newpipe-14015

_claude-sonnet-5.5@default, 24 s; looked at: frames/0027.5.jpg, frames/0030.0.jpg_

In NewPipe 0.29.2 (Vietnamese UI), opening two POPS Kids videos from the feed fails with 'Nội dung không khả dụng' (Content not available). The Doraemon video also produces a ContentNotAvailableException report. An Asphalt 8 video from the same feed plays. In the Candyko case, the previous video's player keeps playing above the error page.

## Some feed videos (POPS Kids, apparently YouTube Kids content) fail with 'Content not available'; previous video keeps playing behind the error

Class: **error-shown**

Environment: NewPipe 0.29.2, Vietnamese UI, 'Có gì mới' (What's new) feed. Phone-sized portrait recording by Mobizen. The ticket says Android 8 on a Samsung Galaxy S7. The device model and Android version are not visible in the video. Channels seen: POPS Kids and Cym64.

Steps:

1. On the feed, open 'Dining with Doraemon Series #218' (POPS Kids). The tap is not visible. The player page shows 'Nội dung không khả dụng' with Báo cáo (Report), Thử lại (Retry) and Mở trong trình duyệt (Open in browser). (00:03.2; p007)
2. Report screen 'Báo lỗi' opens (the trigger is not visible). It shows app version 0.29.2 and a ContentNotAvailableException from YoutubeStreamExtractor ("video is not available"). The reporter scrolls through it. (00:05.8; p013, p015, p016)
3. Go back to the Doraemon error page, then to the feed. (00:10.6; p020, p023)
4. Contrast: open 'Race Beyond the Road | Old Asphalt 8' (Cym64). It loads and plays (player controls, 360p and 1x appear). (00:14.5; p025, p037, p045)
5. Back on the feed, open 'Candyko's Quiz Adventure: Christmas' (POPS Kids). The same 'Nội dung không khả dụng' page appears. (00:26.8; p072, p090, p092, p093)
6. Tap the player area and then at (182,124). The error page stays. The Asphalt video image still moves above it. (00:28.2; p121, p147)

Expected (implied): The POPS Kids videos should load and play like the Cym64 video, or show a clear reason they cannot. The previous video's player should not keep running over a failed load.

Actual: Both POPS Kids videos show 'Content not available'. The Doraemon one also gives a ContentNotAvailableException from YoutubeStreamExtractor. The Asphalt 8 video plays. In the Candyko case the earlier Asphalt video is still visible and changing in the player area above the error page (frames 0027.5 and 0030.0).

Key events: p007, p013, p015, p025, p045, p090, p092, p093

Missed by the author:

- The Candyko error appears while the previous Asphalt video is still playing in the player area (p090, p092; frames 0027.5, 0030.0). The failed load does not stop or replace the old player.
- A video from another channel plays in the same feed (p037, p045), so the failure affects only some videos. The video shows no common cause such as the channel. The video has one utterance ('Thank you.') and no explanation.

Claims:

- "YouTube Kids video cannot play (ticket title)" [ticket]: confirmed - Two POPS Kids videos fail. The screen never says they are YouTube Kids content, so that part comes from the title and channel name.
- "Affected version 0.29.2" [ticket]: confirmed - The report screen shows 0.29.2 (p015).
- "Android 8, Samsung Galaxy S7" [ticket]: not shown - The device model and Android version are not visible in the video.
