# real/mattermost-37659

_claude-sonnet-5.5@default, 21 s; looked at: frames/000005.jpg, frames/000236.jpg, frames/000899.jpg_

The 31 s video shows a Mattermost desktop channel view that is heavily blurred and has no speech and no visible cursor. The message list keeps shifting and re-rendering (images, attachments and posts change position) while a blue "jump to new messages" bar stays fixed at the top. The video is too unreadable to say what the author meant to show, so the most likely candidate is unstable scroll position or content reflow in the channel.

## Mattermost channel message list scrolls or re-lays out repeatedly with the new-messages bar left in place (exact defect unclear)

Class: **intermittent**

Environment: Mattermost desktop app, dark theme, a single channel (an orange-avatar user is highlighted in the sidebar) with image attachments and a pinned blue new-messages banner. Text is unreadable because the video is blurred. No account or organization names can be read.

Steps:

1. Channel view is open with image attachments in the message list and the blue new-messages bar at the top. (00:00.1; p001, p005)
2. The message list content changes position and re-renders over most of the video, with attachment images appearing and disappearing in different places (for example at 7.8 s and 29.9 s). The trigger is not visible, most likely scrolling by the user. (00:07.8; p089, p299, p393)
3. Through all of these changes the blue bar and the text next to it stay at the same place, including at the end of the video. (00:29.9; p092, p394)

Expected (implied): The message list should stay stable once loaded, and the new-messages bar should reflect the actual unread position. No author statement is available.

Actual: The list content moves, changes and re-lays out continuously, and the new-messages bar does not change. Because the video is blurred and has no audio, it is not possible to tell which specific behaviour the author considers wrong.

Key events: p001, p089, p092, p299, p393

Missed by the author:

- The video has no speech, so nothing the author noticed is known. The new-messages bar stays unchanged through every content change [p092, p394].
