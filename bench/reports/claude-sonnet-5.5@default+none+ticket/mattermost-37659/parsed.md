# real/mattermost-37659

_claude-sonnet-5.5@default, 16 s; looked at: nothing_

While scrolling up through a large channel history in Mattermost, the message list intermittently jumps backward and skips several messages. The messages just before the jump are never shown, so users miss content in the history. It occurs in both the desktop app and the web app.

## Scrolling up through channel history intermittently skips messages and jumps backward

Class: **intermittent**

Environment: Mattermost server 11.7.2 (PostgreSQL, schema 171, Ubuntu Server 24.04, local network, Nginx Proxy Manager reverse proxy). Client OS is Windows 10. Mattermost Desktop 6.2.2 and Google Chrome 144.0.7559.110 web app are both affected. No account or organization details are given.

Steps:

1. Open a channel with a large message history. (00:00.0; )
2. Scroll upward to view and load older messages. (00:00.0; )
3. Keep scrolling through the older history. (00:00.0; )
4. Watch for the message list to jump to an earlier point and skip several messages. This happens intermittently. (00:00.0; )

Expected (speech): Older messages load in continuous chronological order while scrolling up, with no gaps, skipped messages or unexpected jumps in scroll position.

Actual: The message list occasionally jumps backward and skips several messages. The messages immediately before the jump are not shown before older messages are displayed.

Key events: 

Claims:

- "The issue also affects the web app in Chrome." [Web app: Also affected in Google Chrome 144.0.7559.110]: not shown - There is no video. The report only states it, and the video it mentions was not available.
- "A video recording shows the issue." [I have attached a video recording showing the issue.]: not shown - The recording was not available, so it could not be checked.
