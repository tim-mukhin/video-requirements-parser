# real/newpipe-14015

_claude-sonnet-5.5@default, 25 s; looked at: frames/0025.0.jpg, frames/0014.5.jpg_

A video shared from the YouTube app to NewPipe 0.29.2 with 'Video player' ends on a 'Content not available' screen. The error report says YouTube returned UNPLAYABLE: 'This video is not available'. The video does not show whether a second attempt was made, so the ticket's claim that it fails repeatedly is not shown.

## Video shared from YouTube to NewPipe fails with 'Content not available' (UNPLAYABLE: This video is not available)

Class: **error-shown**

Environment: Android phone, portrait, 240x426 recording. Mobizen recorder is running. Vietnamese UI. The YouTube app (not YouTube Kids) shares to NewPipe, and the error report is dated 2026-11-10 07:32 GMT. The ticket gives NewPipe 0.29.2, Android 8 and a Samsung Galaxy S7; the video text only partly confirms this. The report shows service YouTube and content language vi-VN.

Steps:

1. In the YouTube app, tap the search field and type 'oggy'. The results list has 'Oggy và những chú gián tinh nghịch' first (the keyboard and query are seen; the tap trigger is only partly visible). (00:03.1; p012, p042, p048)
2. Open the result's menu. It lists Save, Download and Share (the trigger is not visible). (00:07.9; p056)
3. Choose Share. The share sheet opens (the trigger is not visible). Pick NewPipe in it. (00:09.5; p058, p071)
4. In the NewPipe dialog, 'Trình phát video' (Video player) is highlighted (frame 0014.5), so it was most likely tapped (the tap is not shown). (00:14.9; p085)
5. NewPipe shows 'Nội dung không khả dụng' (Content not available) with 'Báo cáo', 'Thử lại' and 'Mở trong trình duyệt' buttons. (00:17.6; p087, p089, p090, p091)
6. The error report opens (the trigger is not visible). It shows the request type 'requested stream' and the YouTube service. The error is UNPLAYABLE: 'This video is not available', thrown in onFetchPage. (00:20.1; p102, p104, p105)

Expected (implied): The shared video opens and plays in NewPipe's video player.

Actual: NewPipe shows 'Content not available'. Its error report names a YouTube extractor failure at fetch time: UNPLAYABLE 'This video is not available'.

Key events: p085, p087, p102, p104, p105, p110

Missed by the author:

- The error report's exception text is YouTube's own UNPLAYABLE status, so the video may be restricted by YouTube. This is likely not a NewPipe crash (p104, p105).
- The report names the content language vi-VN and the country VN (p102). A region or age restriction is a possible cause, but the video does not show it.

Claims:

- "The video cannot play in NewPipe." [ticket]: confirmed - The error screen (p087) and the report (p104, p105) show playback failing.
- "It is a YouTube Kids video (ticket title)." [ticket]: not shown - The source app looks like regular YouTube, with Shorts and Music tabs and the search 'Tìm trên YouTube'.
- "The affected version is 0.29.2." [ticket]: not shown - The version line was not read in the timeline OCR (the watcher reports it in frame 0018). Package org.schabi.newpipe is seen at p104.
- "The failure repeats (the other recordings are attached as well)." [ticket]: not shown - At 25.1 s the same error screen shows again after the report is closed (p110). No second share or loading is seen in the timeline, and the click at 26.7 s (p112) landed on unreadable text. The watcher's retry sequence is not supported by the timeline.
