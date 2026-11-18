# real/tbandroid-10575

_gpt-6-sol@default, 60 s; looked at: frames/moments/p011.jpg, frames/moments/p023.jpg, frames/moments/p146.jpg, frames/moments/p161.jpg, frames/0005.5.jpg, frames/0007.5.jpg, frames/0008.5.jpg, frames/0046.0.jpg, frames/0009.5.jpg, frames/0003.0.jpg, looks/0005.60-0006.30-0_50_1080_620/sheet.jpg, looks/0007.70-0008.35-0_50_1080_620/sheet.jpg, frames/0009.0.jpg, frames/0004.0.jpg, frames/0007.0.jpg, frames/0006.0.jpg, looks/0007.45-0008.15-0_0_1080_1100/sheet.jpg, frames/000191.jpg_

Deleting “Test message 13” briefly opens “Test message 12,” but the app then returns to the Inbox instead of keeping the next message open. The video supports the reported navigation problem, but the visible action is deletion, not the two archives inferred by the frame-only notes.

## Deleting a message briefly shows the next message, then returns to the Inbox

Class: **intermittent**

Environment: Thunderbird for Android; Inbox of <email>. Settings also show other accounts. The ticket reports version 17.0b3 on a Fairphone 3 with LineageOS 22.2; those details are not visible in the video.

Steps:

1. Open “Test message 13” from the Inbox (opening trigger not visible). (00:03.6; p002, p003)
2. Tap the trash icon in the message toolbar to delete “Test message 13.” (00:05.6; p007, p011)

Expected (implied): Keep the next message open, as specified by “After deleting or moving a message: Show next message.”

Actual: “Test message 12” appears at 7.3 s for about 0.9 s, then the app returns to the Inbox; its list is briefly blank. The trigger for that return is not visible, so the video does not establish whether it was an additional user action.

Key events: p003, p007, p011, p018, p022, p023, p151, p153

Missed by the author:

- The frame-by-frame view settles the frame-only notes' action guess: the visible tap hits Delete, not Archive [p007].
- The next message does open, but only briefly before the Inbox transition [p011, p022]; the short-event strip confirms this is not merely a missing half-second sample.
- The Inbox content is briefly empty during the return [p023].

Claims:

- "“Show next message” is selected." [ticket: Expected behavior]: confirmed - The Interaction setting shows that value, and the selection dialog marks it selected [p151, p153].
- "The app can return to the message list rather than retaining the next message." [ticket: Actual behavior]: confirmed - “Test message 12” appears briefly before the Inbox returns [p011, p022]. The video's single visible sequence does not establish the claimed roughly 50% frequency.
- "Archiving also reproduces the problem." [ticket: Steps to reproduce]: not shown - The visible toolbar touch is on the trash icon, not the archive icon; no archive outcome is demonstrated.
- "This has happened for about two months across versions 16 and 17." [ticket: Actual behavior]: not shown - The recording covers one session and does not display version history.
- "The account has a high local folder size of 5000." [ticket: Other potentially useful things]: not shown
