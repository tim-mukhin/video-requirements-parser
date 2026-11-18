# real/tbandroid-10575

_claude-sonnet-5.5@default, 16 s; looked at: nothing_

In Thunderbird for Android 17.0b3, deleting or archiving a message sometimes returns to the message list. The user has chosen the setting 'After deleting or moving a message' to show the next message. The reporter says this happens about 50% of the time and looks like a glitch rather than the setting being ignored. It has gone on for about 2 months, so it affects normal triage of mail.

## 'After deleting or moving a message' setting intermittently ignored: app returns to message list instead of showing next message

Class: **intermittent**

Environment: Thunderbird for Android 17.0b3 (also seen in stable and beta 16/17), installed from 'Other' source. LineageOS 22.2-20260211-NIGHTLY on a Fairphone 3. Multiple accounts, mainly an outlook.com account. Local folder size set to 5000.

Steps:

1. Set 'After deleting or moving a message' to show the next message. (00:00.0; )
2. Open a message in a folder, with other messages after it. (00:00.0; )
3. Delete or archive the message. Repeat, since it only happens some of the time. (00:00.0; )

Expected (speech): The next message is shown, as the setting selects.

Actual: About half the time, the app seems to glitch and returns to the message list instead of showing the next message.

Key events: 

Claims:

- "The failure happens about 50% of the time." [maybe ~50% of the time]: not shown - Only the ticket text is available. The recording was not seen and the reporter's estimate is approximate.
- "The setting is not simply ignored; the behaviour is a glitch." [It doesn't feel like it is simply not listening to the setting, it seems like it is glitching someway]: not shown - The reporter's impression. It cannot be checked without the recording or the logs.
- "The behaviour has been present for about 2 months across versions 16 and 17." [I think I've seen this behavior for the last ~2 months, in various stable and beta versions (16/17)]: not shown - The reporter is unsure ('I think') and gives no version evidence.
