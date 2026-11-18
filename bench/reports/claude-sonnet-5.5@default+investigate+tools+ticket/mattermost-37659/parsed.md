# real/mattermost-37659

_claude-sonnet-5.5@default, 27 s; looked at: frames/0025.0.jpg, frames/0028.0.jpg_

In a Mattermost desktop channel full of large image posts, the author scrolls up through history. Around 25–30 s the list does not move steadily toward older posts: the same screenshots show up again in a different order and position. The video is heavily blurred, so skipped messages cannot be confirmed. The ticket's 'jumps backward' is supported only as repeated or reordered views.

## Post list jumps back and forth while scrolling up through history with large image posts

Class: **intermittent**

Environment: Mattermost desktop app on Windows (taskbar visible), dark theme, one channel with many image attachments. Window title, channel and user names are unreadable because of blur. The version numbers (desktop 6.2.2, server 11.7.2) come from the ticket and are not visible in the video. A blue 'jump to'-style bar is fixed at the top of the post list throughout (e.g. 0025.0).

Steps:

1. Open a channel with a long history of large image posts. The view is near the newest posts. The scroll trigger (mouse wheel or keys) is not visible, so only the content movement is known. (00:00.0; p001)
2. Scroll up. The content moves down steadily with older posts appearing at the top. Timeline scroll events at 13.5 s (259 px down), 15.4 s (101 px down) and 18.0 s (16 px down) are consistent with this. The first events, up to 4.7 s, are only small moves of 9 to 72 px. (00:13.5; p161, p193, p248)
3. Keep scrolling up. A green-strip screenshot reaches the top at about 25 s (frame 0025.0). (00:25.0; p348)
4. The list then moves the wrong way. Content moves 13 px up at 26.3 s. At 28.0 s the view shows a yellow-bar screenshot and a mobile-list screenshot below it. Content then moves 181 px down at 28.4 s. At 30.5 s the green-strip screenshot is back, as at 25 s, so the view returned to a position already passed. (00:26.3; p365, p383)

Expected (implied): Older messages load and display in continuous order while scrolling up, with no jumps in scroll position and no repeated or skipped posts.

Actual: After about 25 s, while the author keeps scrolling up, the view moves forward and back between the green-strip, mobile-list and yellow-bar posts. It returns to the green strip at 30.5 s. There is no error message and no cursor or input is visible. A gap in the message sequence cannot be verified because the frames are blurred.

Key events: p161, p348, p365, p383

Missed by the author:

- Large image posts change size as they load while scrolling (many icon/colour changes in the timeline, e.g. p094 to p137). This is a plausible cause of the position jumps, not proven by the frames.
- The video has no speech or visible cursor, so the author gives no commentary and the scroll input is unknown.

Claims:

- "The message list occasionally jumps backward while scrolling up." [ticket]: confirmed - Frames 0025.0, 0028.0 and 0030.5, plus the 26.3 s and 28.4 s scroll events, show the position going back to content already passed. The video covers one occurrence only, so 'intermittent' rests on the ticket.
- "Several messages are skipped before older ones are shown." [ticket]: not shown - The frames are blurred and sampled every 0.5 s, so a missing run of messages cannot be established.
- "The web app in Chrome is also affected." [ticket]: not shown - Only the desktop app is visible.
- "Desktop 6.2.2, server 11.7.2, Windows 10." [ticket]: not shown - No version is legible. Only a Windows-style taskbar is visible.
