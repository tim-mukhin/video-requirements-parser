# real/tbandroid-10575

_claude-sonnet-5.5@default, 48 s; looked at: frames/0000.0.jpg, frames/0003.0.jpg, frames/0006.0.jpg, frames/0009.0.jpg, frames/0012.0.jpg, frames/0015.0.jpg, frames/0018.0.jpg, frames/0021.0.jpg, frames/0024.0.jpg, frames/0004.5.jpg, frames/0007.5.jpg, frames/0027.0.jpg, frames/0030.0.jpg, frames/0033.0.jpg, frames/0036.0.jpg, frames/0039.0.jpg, frames/0042.0.jpg, frames/0045.0.jpg, frames/0048.0.jpg, frames/0051.0.jpg, frames/0054.0.jpg, frames/0005.5.jpg, frames/0006.5.jpg, frames/0008.5.jpg, frames/0010.0.jpg, frames/0011.0.jpg, frames/0004.0.jpg, frames/0007.0.jpg, frames/0008.0.jpg_

The reporter opens "Test message 13" and, apparently, deletes it. The setting "After deleting or moving a message" is shown set to "Show next message". The message view flickers between blank and content, briefly shows "Test message 12", then falls back to the Inbox list, which is blank for about 1 s and then reloads scrolled to the top. The rest of the video shows the settings that could be relevant, but no further delete or archive is recorded.

## After deleting/moving a message, view flickers and returns to the message list despite "Show next message" setting

Class: **wrong-data**

Environment: Thunderbird for Android (ticket says 17.0b3), dark theme, 1080x2160 phone, screen recording on 21 Feb. Account <email>, Inbox with test messages "Test message 6"–"13" from Danny Garside, 20 Jan. Four accounts are configured: outlook.com, digiresacademy.org, riseup.net and corvus-coop.org. The Interaction setting shows "After deleting or moving a message: Show next message".

Steps:

1. Inbox list is shown. The top message is "Test message 13"; note that "Test message 11" appears twice in the list. (00:00.0; 0000.0)
2. Tap "Test message 13" (a touch dot is visible on the row). The message opens, with delete, mark-unread and archive icons in the toolbar. (00:03.0; 0003.0, 0004.5)
3. The message view flickers: it goes blank at 5.0 s and shows message 13 again at 5.5 s. The delete or archive tap is not visible in the frames. It is inferred from the ticket and from the view changing. (00:05.0; 0004.0, 0005.5, 0006.0)
4. The view goes blank, then briefly shows "Test message 12", the next message. This is what the setting is supposed to do. (00:07.5; 0007.0, 0007.5)
5. The next message disappears at once. A transitional frame shows the Inbox title with the message toolbar icons, and then the Inbox list is blank. (00:08.0; 0008.0, 0008.5, 0009.0)
6. The Inbox list reloads (blurred at first) and is scrolled to the top, with different messages from the ones at the start. The user is back in the list instead of in the next message. (00:10.0; 0010.0, 0011.0)
7. The author opens the drawer, then Settings > account > Reading mail, General settings, Folders and General settings > Interaction. He taps the "After deleting or moving a message" row at about 45 s. The setting reads "Show next message". (00:42.0; 0012.0, 0015.0, 0019.0, 0034.0, 0042.0, 0045.0)

Expected (implied): After deleting or moving a message with "Show next message" selected, the app stays in message view and shows the next message.

Actual: The app shows the next message ("Test message 12") for about half a second. The view then flickers blank and the app returns to the Inbox list. The ticket says this happens in about 50% of cases.

Key events: 0004.5, 0007.5, 0008.0, 0009.0, 0042.0

Missed by the author:

- "Test message 11" appears twice in the Inbox list at the start (0000.0). This may be a duplicate or a stale row.
- The Inbox list is blank for about 1 s and then reloads with different content from the start (0009.0–0011.0).
- The toolbar briefly shows Inbox title with message action icons (0008.0), so the view is mid-transition.
- The video shows only one occurrence, and no second delete or archive is recorded.

Claims:

- "After a delete or archive the app glitches and returns to the message list" [The app seems to glitch (maybe ~50% of the time) and return to the message list]: confirmed - One occurrence is visible: the view flickers and ends on the Inbox list at 9–10 s (0007.5–0010.0). The 50% rate is not shown, because only one delete or archive is recorded.
- "The setting is "Show next message"" [Next message shown (if that setting is selected)]: confirmed - Interaction settings at 0042.0 show "After deleting or moving a message: Show next message".
- "It is a glitch, not the app ignoring the setting" [It doesn't feel like it is simply not listening to the setting, it seems like it is glitching]: confirmed - The next message does appear briefly (0007.5) before the app returns to the list.
- "The delete or archive action was performed" [Delete or archive messages]: not shown - No tap on delete or archive is visible in the frames, and it is not clear which action was used. The frames show the message-view changes only.
- **R1** [stated] After deleting or moving a message with "Show next message" selected, the app must stay in message view on the next message. - 0042.0, 0007.5, 0009.0
