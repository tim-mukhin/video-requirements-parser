# real/newpipe-14015

_claude-sonnet-5.5@default, 27 s; looked at: frames, frames/0000.0.jpg, frames/0003.0.jpg, frames/0006.0.jpg, frames/0009.0.jpg, frames/0012.0.jpg, frames/0015.0.jpg, frames/0018.0.jpg, frames/0021.0.jpg, frames/0024.0.jpg, frames/0027.0.jpg, frames/0013.5.jpg, frames/0014.5.jpg, frames/0016.5.jpg, frames/0025.0.jpg_

In the YouTube app the user searches "oggy" and shares a video to NewPipe, choosing "Video player". NewPipe shows "Content not available" and an error report with ContentNotAvailableException, "This video is not available". A second attempt gives the same result.

## Video shared from YouTube to NewPipe fails with "Content not available" (ContentNotAvailableException)

Class: **error-shown**

Environment: Android 8 (Linux Android 8.0.0), Samsung Galaxy S7 per ticket. YouTube app (Vietnamese UI) shares to NewPipe 0.29.2 (version shown in the error report). Mobizen screen recorder is running. The service shown in the report is YouTube.

Steps:

1. In the YouTube app, tap the search field and type "oggy" (inferred from the keyboard and the query). (00:03.0; 0003.0, 0006.0)
2. Open the menu on the first result ("Oggy và những chú gián tinh nghịch") and choose Share (inferred). (00:09.0; 0009.0)
3. Pick NewPipe in the share sheet (inferred). (00:09.0; 0009.0)
4. In the NewPipe dialog choose "Trình phát video" (Video player). It is highlighted, so a tap is inferred. (00:12.0; 0012.0)
5. NewPipe shows the "Nội dung không khả dụng" (Content not available) screen with a sad face. (00:15.0; 0015.0)
6. Open the error report: ContentNotAvailableException, "This video is not available", NewPipe 0.29.2. (00:18.0; 0018.0)
7. Go back and retry. The share dialog appears again, then a loading spinner, then the same error screen. (00:25.0; 0014.5, 0016.5, 0025.0)

Expected (implied): The shared video opens and plays in NewPipe's player.

Actual: NewPipe shows "Content not available". The error report names ContentNotAvailableException from the YouTube extractor with the message "This video is not available". The retry fails the same way.

Key events: 0015.0, 0018.0, 0025.0

Missed by the author:

- The error report names an exception from the YouTube extractor's fetchPage call. The "video is not available" message may come from YouTube refusing the request (0018.0). The video does not show the cause.
- The source app is the normal YouTube app, not YouTube Kids (0000.0). The reporter may mean a different video in the other recordings.

Claims:

- "The video cannot play in NewPipe (ticket title says it is a YouTube Kids video)." [YouTube Kids video cannot play]: confirmed - Playback fails with a not-available error. The video does not visibly come from YouTube Kids. The source app looks like the regular YouTube app.
- "Affected version is 0.29.2." [0.29.2]: confirmed - The error report shows version 0.29.2.
