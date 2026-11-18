# real/tbandroid-10575

_claude-sonnet-5.5@default, 26 s; looked at: frames/0008.0.jpg, frames/0004.5.jpg_

With 'After deleting or moving a message' set to 'Show next message', the app opened the next message (Test message 12) for about 0.9 s and then dropped back to a blank Inbox list. The Inbox then reloaded. The video shows one occurrence. The delete or archive trigger is not visible, and the ~50% rate is not shown.

## After delete/archive with 'Show next message', next message flashes then app returns to (blank) Inbox list

Class: **intermittent**

Environment: Thunderbird for Android (version not shown; ticket says 17.0b3), dark theme, 1080x2160 phone, recording 12:43. Account <email>, with 3 more accounts configured (digiresacademy.org, riseup.net, corvus-coop.org). Inbox holds test messages from Danny Garside, 20 Jan.

Steps:

1. Open the Inbox of <email> and open 'Test message 13'. The message view shows delete, mark-unread and archive icons. The opening tap itself is not clearly shown. (00:03.6; p002, p003, p004)
2. Message 13 is on screen about 1.7 s. Then it disappears (the delete/archive tap is not visible; the author's action is inferred). (00:06.0; p007, p008, p009, p010)
3. The next message, 'Test message 12', appears for 0.9 s, which is what 'Show next message' should do. (00:07.3; p011, p012, p013, p014)
4. Message 12 disappears. The toolbar switches to 'Inbox / dannygarside…', which still shows the message-view action icons (trash, mark unread, archive), over an empty list. The app has returned to the message list instead of staying on the next message. (00:08.2; p018, p019, p020, p021, p022, p023)
5. The Inbox list reloads (the many UI-change events at 9.4 s are the list redrawing). The author then opens Settings > Interaction and shows that the setting reads 'Show next message'. (00:09.4; p024, p151)

Expected (implied): After deleting or archiving, the app stays in message view and shows the next message (Test message 12), as the setting says.

Actual: Test message 12 is shown for only ~0.9 s, then it disappears. The app lands on a blank Inbox list with leftover message-view toolbar icons, and the list reloads afterwards. The setting on screen is 'Show next message'.

Key events: p011, p018, p022, p023, p151

Missed by the author:

- The Inbox is blank for about 1 s with the message-view toolbar icons still showing (p022, p023), which suggests a half-finished transition.
- The list reloads at 9.4 s with a burst of redraw events (p025–p125).
- The author does not say anything about the glitch. The only speech is 'Thank you.' (u002) at 37.3 s.

Claims:

- "The app glitches and returns to the message list after delete/archive" [ticket]: confirmed - One occurrence is visible at 7.3–9.4 s: the next message flashes, then the Inbox list appears blank and reloads.
- "It happens about 50% of the time" [ticket]: not shown - Only one delete/archive is recorded in the video.
- "The 'Show next message' setting is selected" [ticket]: confirmed - The Interaction screen at 40.6 s shows 'After deleting or moving a message: Show next message'. The author opens the picker at 44.5 s, but the setting reads 'Show next message' before that.
- "It is a glitch, not the setting being ignored" [ticket]: confirmed - The next message does appear briefly (p011) before the app falls back to the list.
- "The author deleted or archived the message" [ticket]: not shown - No tap on delete or archive is visible. It is not known which action was used.
- "The behaviour has been present for about 2 months across versions 16/17" [ticket]: not shown - This is a claim about the past. The video shows only one moment.
- "Outlook account, multiple accounts, local folder size 5000" [ticket]: not shown - Outlook and the 4 accounts are visible. The folder size 5000 is not shown. The video does not show that any of these cause the bug.
