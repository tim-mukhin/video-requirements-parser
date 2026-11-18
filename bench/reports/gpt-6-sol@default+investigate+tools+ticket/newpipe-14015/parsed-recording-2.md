# real/newpipe-14015

_gpt-6-sol@default, 42 s; looked at: frames/0007.0.jpg, frames/0008.0.jpg, frames/0009.5.jpg, frames/0010.5.jpg, frames/0012.5.jpg, frames/0015.0.jpg, frames/0018.0.jpg, frames/0020.0.jpg, frames/0021.5.jpg, frames/moments/p029.jpg, frames/moments/p054.jpg, frames/moments/p068.jpg, frames/moments/p080.jpg, frames/moments/p092.jpg, frames/0013.5.jpg, frames/0014.0.jpg_

A video shared from YouTube to NewPipe for playback opens to “Content unavailable” instead of playing. NewPipe’s error report identifies a requested-stream failure and says the video is not available; the recording does not establish whether it is a YouTube Kids video.

## Shared Oggy video shows Content unavailable in NewPipe

Class: **error-shown**

Environment: YouTube and NewPipe 0.29.2 on Android 8.0.0; the device model is not visible.

Steps:

1. Search YouTube for “oggy” and locate the “Oggy and the Cockroaches - Oggy Starts Painting!” result. (00:06.7; p053)
2. Open the result’s menu (the trigger is not visible) and choose Share; the Android share sheet opens. (00:07.9; p056, p058)
3. Expand the share sheet, select NewPipe (the tap is not visible), and choose Play video in NewPipe’s action dialog (the tap is not visible). (00:12.1; p071, p085, p086)

Expected (implied): NewPipe plays the shared video.

Actual: NewPipe displays “Content unavailable” [p087–p091]. Its error report lists a requested-stream failure and “This video is not available” [p102, p104].

Key events: p053, p056, p058, p071, p085, p087, p091, p102, p104

Missed by the author:

- The frames show the Oggy search result and NewPipe’s Play video option; the timeline establishes their order before the failure [p053, p085, p087]. The ticket gives no reproduction steps.
- The error report identifies a requested-stream failure and says “This video is not available” [p102, p104]; the ticket provides no actual-behavior description or logs.

Claims:

- "A YouTube Kids video cannot play." [ticket: title]: not shown - The playback failure is visible, but the result is shown in the regular YouTube app with no Kids designation.
- "The affected version is 0.29.2." [ticket: Affected version]: confirmed - NewPipe’s error report shows version 0.29.2 [p102].
- "The device runs Android 8." [ticket: Affected Android/Custom ROM version]: confirmed - The error report shows Android 8.0.0 [p102].
- "The device is a Samsung Galaxy S7." [ticket: Affected device model]: not shown - No device model is visible.
