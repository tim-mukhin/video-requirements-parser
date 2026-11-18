# Some emoji tooltips appear at top-left after clicking another application

Source: https://github.com/RocketChat/Rocket.Chat/issues/42674  (reporter: AnsariTazeem, filed 2026-10-09)

### Description:

Some emoji-name tooltips appear at the top left of the page after I click another application and move the pointer back to Rocket.Chat without clicking or refocusing inside it.

### Steps to reproduce:

1. Open a conversation and the composer emoji picker.
2. Hover over emojis. Their tooltips initially appear near them.
3. Leave the picker open and click another application, such as Notepad.
4. Move the pointer back over the picker without clicking Rocket.Chat.
5. Hover over different emojis.

### Expected behavior:

The tooltip should appear near the hovered emoji.

### Actual behavior:

The white emoji-name tooltip appears at the page's top-left instead of near the hovered emoji. This affects some emojis, not all.

[attachment: recording.mp4]

### Server Setup Information:

- Version of Rocket.Chat Server: 8.10
- Workspace: https://open.rocket.chat

### Client Setup Information

- Browser: Brave 1.96.61; also reproduced in Google Chrome 154.0.8037.99 (64-bit)
- Operating System: Windows 11

### Additional context

The recording is from open.rocket.chat in Brave. I also reproduced the issue on localhost.

A second monitor is not required but we can reproduce this bug with two screens as well, one having the Rocket.Chat interface and other screen having any another application. I reproduced it with Rocket.Chat and Notepad on the same display.

Moving the pointer slightly may reposition the current tooltip, but the problem can happen again when hovering other emojis.
Clicking inside Rocket.Chat restores normal behavior.

Alt+Tab did not reproduce it in an earlier test.

### Relevant logs:

No new browser console errors appeared while I reproduced the issue.
