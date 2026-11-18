# real/newpipe-14015

_gpt-6-sol@default, 41 s; looked at: frames/0007.0.jpg, frames/0003.5.jpg, frames/0018.5.jpg, frames/0024.0.jpg, frames/0027.0.jpg, frames/moments/p094.jpg, frames/0000.0.jpg, frames/0005.5.jpg, frames/0007.5.jpg, frames/0023.5.jpg, frames/0025.0.jpg, frames/moments/p095.jpg, frames/moments/p078.jpg, frames/0006.0.jpg, frames/0008.0.jpg, frames/0029.0.jpg, frames/moments/p026.jpg, frames/moments/p091.jpg_

Two POPS Kids videos opened in NewPipe show “Content unavailable” instead of playing. An Asphalt video plays between the failures, so playback is not universally broken; the video's error report identifies a ContentNotAvailableException.

## POPS Kids videos show Content unavailable in NewPipe

Class: **error-shown**

Environment: NewPipe with a Vietnamese-language interface. Its on-screen error report identifies version 0.29.2; the ticket reports Android 8 and a Samsung Galaxy S7, which are not shown.

Steps:

1. In the What's New feed, locate the POPS Kids video “Candyko's Quiz Adventure: Christmas | LOTTY FRIENDS” [p074]. (00:23.3; p074)
2. Open that video (the trigger is not visible); its video page appears [p076]. (00:24.8; p076)

Expected (implied): The selected video loads and plays.

Actual: The Candyko video page shows “Nội dung không khả dụng” (“Content unavailable”) with Report, Retry and Open in browser buttons [p090, p092, p094]. Asphalt gameplay continues in the player area above the error [p095]. Earlier, another POPS Kids video, “Dining with Doraemon Series #218,” showed the same error [p007], while “RACE BEYOND THE ROAD | OLD ASPHALT 8” visibly played [p025, p040].

Key events: p007, p013, p015, p025, p040, p074, p076, p090, p092, p094, p095

Missed by the author:

- The video shows an earlier POPS Kids failure on “Dining with Doraemon Series #218” [p007] and opens an error report for it [p013, p015]; the ticket does not describe either.
- The Asphalt video plays between the failures [p025, p040], and its gameplay remains visible above the Candyko error [p095].

Claims:

- "YouTube Kids videos cannot play." [ticket: title]: confirmed - The two POPS Kids selections shown fail [p007, p092]; the recording does not establish that every Kids video fails.
- "The affected version is 0.29.2." [ticket: affected version]: confirmed - The on-screen NewPipe error report lists 0.29.2 [p015].
- "The device runs Android 8 and is a Samsung Galaxy S7." [ticket: affected Android version and device model]: not shown
