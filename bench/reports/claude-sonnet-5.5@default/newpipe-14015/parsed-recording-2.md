# real/newpipe-14015

_claude-sonnet-5.5@default, 18 s; looked at: frames/000341.jpg, frames/000495.jpg_

A YouTube video (Oggy and the Cockroaches) is shared from the YouTube app to NewPipe and played with 'Play video'. NewPipe shows 'Content not available' and a Guru Meditation error report: the extractor raised UNPLAYABLE, 'This video is not available'. This is a playback failure in NewPipe's YouTube extraction.

## NewPipe fails to play a YouTube video opened via Share: 'Content not available' (UNPLAYABLE)

Class: **error-shown**

Environment: Android phone (portrait, Vietnamese UI). YouTube app (search 'oggy', Shorts tab, share sheet), then NewPipe 0.29.2 on Linux Android 8.0.0. Content language vi-VN, country VN. Error report time 2026-11-10T07:32 GMT. The recording app is Mobizen.

Steps:

1. In the YouTube app, search for 'oggy' and open the Oggy and the Cockroaches result. (00:03.1; p012, p037, p047)
2. Open the video's menu and choose Share. The tap on Share is not visible, but the share sheet appears. (00:09.5; p054, p056)
3. In the share sheet, pick NewPipe. The tap is not visible, but the NewPipe chooser opens. (00:12.1; p068)
4. In the NewPipe chooser, pick 'Play video' (highlighted) with 'Just once' or 'Always'. The tap is not visible. (00:14.9; p082)
5. NewPipe shows 'Content not available' with the buttons Go back, Try again and Open in browser. (00:17.6; p084, p086, p087, p088)
6. The error report opens. It shows the request type as requested stream and the error 'UNPLAYABLE: This video is not available'. (00:20.1; p099, p101)

Expected (implied): NewPipe plays the shared YouTube video.

Actual: NewPipe shows 'Content not available'. The report gives the error type as requested stream, with the YouTube extractor throwing UNPLAYABLE 'This video is not available'. The same video plays in the YouTube app.

Key events: p084, p099, p101, p102

Missed by the author:

- The error report is opened, scrolled and probably copied or shared. The tap that opens it is not visible, and the author says nothing about it (p099, p109).
- The video was playable in the YouTube app, so the failure is specific to NewPipe's extractor.

Claims:

- "Thank you." [u017]: not shown - The only speech is a courtesy phrase, so it has no bearing on the bug.
