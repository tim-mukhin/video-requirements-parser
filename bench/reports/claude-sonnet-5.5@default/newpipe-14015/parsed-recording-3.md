# real/newpipe-14015

_claude-sonnet-5.5@default, 24 s; looked at: frames/000081.jpg, frames/000146.jpg, frames/000446.jpg_

In NewPipe (Vietnamese UI, v0.29.2) a YouTube video, "Dining with Doraemon Series #218", fails to play. It shows "Nội dung không khả dụng" (content not available) with a sad-face placeholder, and the error report shows ContentNotAvailableException "video is not available". Other videos from the same feed open and play, so the failure is specific to this video. The video carries no clear narration, only a "Thank you." at the end.

## NewPipe: a YouTube video fails with "Content not available" (ContentNotAvailableException) while other videos play

Class: **error-shown**

Environment: Android 8.0.0 phone, portrait, screen recorded with Mobizen. NewPipe 0.29.2 (org.schabi.newpipe), Vietnamese UI, service YouTube, content language en-US, request type "requested stream". Feed ("Có gì mới") is open. Report timestamp is 2026-11-10T07:26 GMT.

Steps:

1. Open the "What's new" feed. It is already shown at the start, and its list was last updated about 4 minutes earlier. (00:00.0; p001, p002)
2. Open the video "Dining with Doraemon Series #218 | Where there.." (the tap is not visible). The player page shows a sad-face placeholder, "Nội dung không khả dụng" and the buttons BÁO CÁO, THỬ LẠI and MỞ TRONG TRÌNH DUYỆT. (00:03.2; p007)
3. Open the error report (Báo lỗi, the trigger is not visible). It shows: "Có vẻ NewPipe đã xảy ra lỗi" and "Guru Meditation". The what-happened field says "Nội dung không khả dụng", the type is "requested stream", and the service is YouTube. The stack trace names ContentNotAvailableException, "Got error: ... video is not available", from YoutubeStreamExtractor. (00:05.8; p013, p015, p016, p017)
4. Go back to the same error page. It is still shown (a retry may have been made, but no tap is visible). (00:10.6; p020, p022)
5. Back in the feed, other videos open and play (for example the "Race Beyond the Road | Old Asphalt 8" player at 360p). The failure is therefore specific to the Doraemon video. (00:17.8; p023, p045)

Expected (implied): The video from the feed plays, as the other feed videos do. If the video really is unavailable, the feed should not offer it, or the message should explain why.

Actual: The player page shows only "Content not available" and the report shows ContentNotAvailableException ("video is not available"). The same error page appears again at 00:10.6 and still no playback starts.

Key events: p007, p013, p015, p016, p017, p020, p045

Missed by the author:

- The error report says the request is for YouTube content in en-US with the app language vi_VN (p013). This may matter if the video is region- or availability-restricted, but the video does not show why it is unavailable.
- The feed entry for the video looked normal, with a thumbnail, and gave no sign that it was unavailable (p023).
- Playback of other videos worked in the same session, which points to this video or its extraction rather than a general failure (p045).

Claims:

- ""Thank you." is the only speech. The author makes no factual claim about the bug." [u002]: not shown - Nothing is said about the cause or about earlier behaviour.
