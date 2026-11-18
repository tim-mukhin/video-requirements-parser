# [Bug]: Scrolling up through channel history intermittently skips messages and jumps backward

Source: https://github.com/mattermost/mattermost/issues/37659  (reporter: MohammadHadi2031, filed 2026-07-24)

### Before you file a bug report

- [x] I have checked the [issue tracker](https://github.com/mattermost/mattermost/issues) and have not found an issue that matches the one I'm filing.
- [x] This issue is not a troubleshooting question. Troubleshooting questions go here: https://forum.mattermost.com/c/trouble-shoot/16.
- [x] This issue is not a feature request. You can request features and make product suggestions here: https://mattermost.uservoice.com/forums/306457-general/.
- [x] This issue reproduces on one of the [currently supported server versions](https://docs.mattermost.com/about/mattermost-server-releases.html#latest-releases).
- [x] I have read the [contribution guidelines](https://github.com/mattermost/mattermost/blob/master/CONTRIBUTING.md) and the [Mattermost Handbook Contribution Guidelines](https://handbook.mattermost.com/contributors/contributors/guidelines/contribution-guidelines).

### Mattermost Server Version

11.7.2

### Operating System

Windows 10

### Steps to reproduce

1.	Open a channel with a large message history.
2.	Scroll upward to view and load older messages.
3.	Continue scrolling through the older history.
4.	Observe that, intermittently, the message list jumps to an earlier point and skips several messages.

### Expected behavior

Older messages should load in continuous chronological order while scrolling upward, without gaps, skipped messages, or unexpected jumps in scroll position.

### Observed behavior

While scrolling upward, the message list occasionally jumps backward and skips multiple messages. The messages immediately before the jump are not shown before older messages are displayed.

### Log Output

```shell

```

### Additional Information

Environment
•	Mattermost Desktop version: 6.2.2
•	Web app: Also affected in Google Chrome 144.0.7559.110
•	Mattermost Server version: 11.7.2
•	Database schema version: 171
•	Database: PostgreSQL
•	Server operating system: Ubuntu Server 24.04
•	Deployment: Local-network Mattermost server
•	Reverse proxy: Nginx Proxy Manager

Evidence
I have attached a video recording showing the issue.

[attachment: recording.mp4]
