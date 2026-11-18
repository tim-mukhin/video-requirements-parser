# real/tbandroid-10575

_claude-sonnet-5.5@default, 33 s; looked at: frames/000088.jpg, frames/000149.jpg, frames/000191.jpg, frames/000912.jpg, frames/000943.jpg, frames/000122.jpg_

In an Android mail app (K-9 style) on <email>, an open message (Test message 13) goes blank, then Test message 12 flashes up, then the app drops back to the Inbox. The author then opens the settings and checks the 'After marking a message as unread' and 'After deleting or moving a message' options. The video has no narration, so the exact trigger and the author's intent are inferred, not shown.

## Message view navigates away from the open message (13 → 12 → Inbox) although settings say 'Stay on current message'

Class: **silent-fail**

Environment: Android phone, portrait, dark theme, K-9-style mail client. Account <email>. Other accounts in the list: <email>, <email>, <email>. Settings > General settings > Interaction was opened.

Steps:

1. Message view of 'Test message 13' (Danny Garside, 20 Jan) is open. The toolbar has delete, mark-as-unread, archive and overflow icons. The tap that opened it is not visible. (00:04.3; p003, p004)
2. The message content disappears. The toolbar icon changes from 'mark as unread' to an envelope with a check. This suggests the author marked the message unread, but no tap is shown. (00:06.0; p007, p008, p009, p010)
3. 'Test message 12' (the neighbouring message) flashes for 0.9 s. (00:07.3; p011, p012)
4. The app returns to the Inbox list (taps at the top bar). (00:08.2; p015, p017, p022)
5. The author opens the drawer, then Settings, then Account settings and checks Reading mail and Folders. This does not change anything visible. (00:10.8; p127, p131, p133, p144)
6. In General settings > Interaction the author sees 'After marking a message as unread: Stay on current message'. 'After deleting or moving a message' is set to 'Show next message'. The author opens that dialog and dismisses it without changing it. (00:44.5; p151, p152, p153, p154, p155)

Expected (implied): After the message is marked unread, the view stays on that message, as the 'Stay on current message' setting says.

Actual: The open message disappears, a different message (12) shows for under a second, and then the Inbox list appears. No error is shown.

Key events: p003, p007, p011, p015, p155

Missed by the author:

- The mark-as-unread icon changes to a 'read' envelope just before the content disappears (frames/000122.jpg, p007…p010).
- Test message 12 flashes for only 0.9 s before the Inbox appears (p011…p014). This is the 'Show next message' behaviour, not 'Stay on current message'.
- After the screen change at 8.7 s, a burst of 17 'clicks' and about 60 colour changes is registered (p023…p125). This is the app redrawing the blurred Inbox, not real taps.

Claims:

- "The only utterance is 'Thank you.' (speech recognition, probably noise). It makes no claim about the behaviour." [u002]: not shown
