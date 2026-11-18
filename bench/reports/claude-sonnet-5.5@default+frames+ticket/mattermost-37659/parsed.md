# real/mattermost-37659

_claude-sonnet-5.5@default, 41 s; looked at: frames, frames/0000.0.jpg, frames/0004.0.jpg, frames/0008.0.jpg, frames/0012.0.jpg, frames/0016.0.jpg, frames/0020.0.jpg, frames/0024.0.jpg, frames/0028.0.jpg, frames/0030.5.jpg, frames/0025.0.jpg, frames/0026.0.jpg, frames/0027.0.jpg, frames/0022.0.jpg, frames/0029.0.jpg, frames/0026.5.jpg_

The recording shows a Mattermost desktop channel scrolled upward through a history full of screenshots. Around 24–30 s the same messages (a green-strip screenshot, a mobile-list screenshot, a yellow-bar screenshot) come back in a different order and position, so the scroll position jumps back and forth instead of moving steadily toward older messages. This matches the ticket's 'jumps backward' report, but the frames are heavily blurred, so skipped messages cannot be confirmed.

## Scrolling up through channel history jumps back and forth and re-shows already seen messages

Class: **intermittent**

Environment: Mattermost Desktop app (window title not legible) on Windows, dark theme, one channel with many image attachments. The ticket says desktop 6.2.2, server 11.7.2, and that Chrome is also affected. Frames are blurred, so channel and user names are unreadable.

Steps:

1. Open a channel with a long history that has many large image posts. The newest content is at the bottom. (00:00.0; 0000.0)
2. Scroll upward (inferred from the content moving down the screen). Older posts appear at the top and the list moves steadily for about 20 s. (00:04.0; 0004.0, 0008.0, 0012.0, 0016.0, 0020.0)
3. Keep scrolling. A green-strip screenshot reaches the top at about 24 s. (00:22.0; 0022.0, 0024.0, 0025.0)
4. At 26 s the view jumps to content that is further down: the text posts after the green strip and a mobile-list screenshot. At 26.5–28 s a yellow-bar screenshot appears, and at 29 s the mobile-list image is shown again. The list is not moving steadily toward older messages. (00:26.0; 0026.0, 0026.5, 0027.0, 0028.0, 0029.0)
5. By 30.5 s the view is back at the same green-strip screenshot seen at 24–25 s, so the list has jumped back to a position it already passed. (00:30.5; 0030.5)

Expected (implied): Scrolling up shows older messages in continuous order, without jumps in scroll position or repeated or skipped messages.

Actual: While the user keeps scrolling up, the list position moves forward and back (green strip at 24–25 s, mobile list at 26–26.5 s, yellow bar at 27–28 s, green strip again at 30.5 s). The order of posts around the yellow-bar and mobile-list screenshots does not match what was shown earlier, which fits the ticket's 'jumps and skips' description.

Key events: 0025.0, 0026.0, 0026.5, 0028.0, 0030.5

Missed by the author:

- A 'Jump to'/'New messages' style bar stays fixed at the top of the post list throughout the video (e.g. 0004.0), and its relation to the jumps is unknown.
- Large image attachments change height as they load while the user scrolls, which is a plausible cause of the position jumps (the post sizes and positions differ between 0020.0 and 0022.0). This is a candidate cause, not shown in the frames.

Claims:

- "The message list intermittently jumps to another point while scrolling up." [the message list occasionally jumps backward]: confirmed - Scrolling is smooth until about 24 s. After that the view moves between the green-strip, mobile-list and yellow-bar posts and returns to the green strip at 30.5 s (0025.0, 0026.0, 0028.0, 0030.5).
- "Several messages are skipped before older ones are shown." [skips multiple messages]: not shown - The frames are blurred and sampled every 0.5 s, so a gap in the message sequence cannot be verified. Only the repeated and reordered views are visible.
- "The problem also affects the web app in Chrome." [Web app: Also affected in Google Chrome]: not shown - Only the desktop app window is visible.
- "The window shows Mattermost Desktop 6.2.2 on Windows." [Mattermost Desktop version: 6.2.2]: not shown - No version is legible. The Windows-style taskbar is visible.
