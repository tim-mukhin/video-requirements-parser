# real/joplin-16153

_claude-sonnet-5.5@default, 45 s; looked at: frames/0000.0.jpg, frames/0008.0.jpg, frames/0016.0.jpg, frames/0024.0.jpg, frames/0032.0.jpg, frames/0040.0.jpg, frames/0048.0.jpg, frames/0053.0.jpg, frames/0019.0.jpg, frames/0028.0.jpg, frames/0036.0.jpg, frames/0044.0.jpg, frames/0050.0.jpg, frames/0022.0.jpg, frames/0026.0.jpg, frames/0020.5.jpg, frames/0030.0.jpg, frames/0034.0.jpg, frames/0042.0.jpg_

Two Joplin desktop clients (macOS on the left, a Fedora VM on the right) share the folder "Test". A note published by one user is opened in the other user's Publish Notes dialog. The dialog offers only "Copy Shareable Link" and no way to unpublish. This matches the ticket's regression report.

## Publish dialog gives no unpublish option for a note published by the other user in a shared folder

Class: **silent-fail**

Environment: Joplin DEV, two profiles: macOS (left, profile-x72f4o0o) and a Fedora Linux VM (right, /home/self/.config/joplindev-desktop). Both show the shared notebook "Test" with 2 notes, "test" and "Test". Wed Aug 5, about 3:22–3:23 PM. The two accounts and the server are not visible.

Steps:

1. Starting state: both clients show the shared notebook "Test" with notes "test" and "Test". On the left, "test" has an orange title, which I read as published. (Which user published it is inferred, not shown.) (00:00.0; 0000.0, 0016.0)
2. On the left client, open the Publish dialog for the published note "test" (right-click, Publish note…, inferred). The dialog has only a text field and "Copy Shareable Link". There is no unpublish control. (00:19.0; 0019.0, 0022.0, 0024.0)
3. On the left client, open the Publish dialog for the second note "Test". Click "Copy Shareable Link". A share/unpublish icon then appears beside the note, so this user can unpublish a note they published themselves. (00:30.0; 0028.0, 0030.0)
4. On the right client, after a sync (inferred), "Test" appears orange, meaning published by the other user. Right-click it and choose "Publish note…". (00:36.0; 0034.0, 0036.0)
5. The right client's dialog for the other user's note shows only "Copy Shareable Link" and no unpublish icon. Clicking the link shows "Link has been copied to clipboard!". Unpublishing is still not possible after that. (00:42.0; 0042.0, 0044.0, 0050.0)

Expected (implied): A share member, in particular the share owner, should be able to unpublish a note in the shared folder that the other user published.

Actual: For a note published by the other user, the Publish dialog shows no unpublish control, even after "Copy Shareable Link". The only unpublish control seen in the video is the icon on the user's own published note (0030.0).

Key events: 0024.0, 0030.0, 0044.0, 0050.0

Missed by the author:

- The unpublish icon appears beside the note in the dialog on the user's own published note (0030.0), but not on the other user's note (0024.0, 0044.0). This contrast helps locate the bug.
- The video has no sound, so the author's narration is unavailable.

Claims:

- "A user cannot unpublish a note published by the other share user." [Attempt to unpublish the note. Observe that this isn't possible.]: confirmed - Both clients' dialogs for the other user's published note have no unpublish control (0024.0, 0044.0, 0050.0). I could not tell which of the two accounts is the share owner.
- "Clicking "copy sharable link" does not allow unpublishing the note on the latest dev." [With the latest dev, clicking "copy sharable link" does not allow unpublishing the note.]: confirmed - After the click, the dialog still has no unpublish control (0050.0).
- "The issue is a regression from #15276 or the commit 2c11cbb, and the sync fuzzer fails." []: not shown - The video has no older build and no fuzzer run.
- "The recipient accepted the share and the first publish happened from either user, as in the ticket steps." []: not shown - The video starts with the folder already shared, so setup is not shown. Which user published which note is not visible.
