# real/joplin-16153

_claude-sonnet-5.5@default, 38 s; looked at: frames/0030.0.jpg, frames/0050.0.jpg, frames/0024.0.jpg, frames/0004.0.jpg, frames/0018.5.jpg, frames/0005.5.jpg, frames/0044.5.jpg_

Two Joplin desktop clients (macOS left, Linux VM right) share the notebook "Test". On the Publish Notes dialog, a note published by the other user has only "Copy Shareable Link" and no unpublish control. Clicking "Copy Shareable Link" does not add one. The dialog for a note the user just published themselves does show the unpublish (share) icon. This matches the ticket's regression report.

## Publish Notes dialog offers no unpublish control for a note published by the other share member

Class: **silent-fail**

Environment: Joplin DEV, two profiles: left macOS (profile-x72f4o0o), right Linux VM (/home/self/.config/joplindev-desktop). Both show the shared notebook "Test" (2 notes: "test", "Test"). Aug 5 2026, about 3:22–3:23 PM. Accounts, server and share owner/recipient roles are not visible. The ticket says Linux, 3.7.10; the video shows a DEV build and a macOS client as well.

Steps:

1. Right (Linux) client: open the context menu on note "test" and click "Publish note...". The Publish Notes dialog opens with only "Copy Shareable Link" (frame 0005.5). (00:03.0; p006, p015, p017)
2. Right client: click "Copy Shareable Link". A sync flashes and "Link has been copied to clipboard!" appears. (00:04.8; p027, p029, p035)
3. Left (macOS) client: click Synchronize. The left note "test" is shown as published (orange) in the list at 0044.5, but it is not orange at 0004.0 before this step. (00:07.2; p044)
4. Left client: right-click "test" and choose "Publish note...". The dialog (frames 0018.5, 0024.0) has the text field and "Copy Shareable Link" and no unpublish icon. Click "Copy Shareable Link" and "Link has been copied" appears. The unpublish control is still absent. (00:16.6; p067, p086, p087, p092)
5. Left client: close the dialog, open "Publish note..." on note "Test" and click "Copy Shareable Link". This is the contrast case. The field now shows the blue share (unpublish) icon at 0030.0 beside the note title. (00:29.0; p125, p127, p139, p142, p146)
6. Right client: click Synchronize, then right-click "Test", the note the left client just published, and choose "Publish note...". (00:33.9; p155, p187)
7. Right client: the dialog for "Test" shows only "Copy Shareable Link" and no unpublish icon (frame 0044.5). Click "Copy Shareable Link". "Link has been copied to clipboard!" appears. Still no unpublish control. Close the dialog. (00:37.4; p188, p195)

Expected (implied): A share member, in particular the share owner, can unpublish any published note in the shared folder. The Publish Notes dialog should show the unpublish control for a note published by the other user.

Actual: For a note published by the other user, the dialog offers only "Copy Shareable Link", before and after clicking it. No error is shown. The unpublish icon appears only for a note this client published itself. The result is the same on both clients.

Key events: p086, p115, p139, p146, p188

Missed by the author:

- The unpublish icon appears when the same client publishes its own note (frame 0030.0, p139–p146) and is missing for the other user's note (p115, p188). This is the key contrast.
- There is no audio. Every fact comes from the screen. Short flashes of "Synchronising..." after each "Copy Shareable Link" click (p029, p088, p143) are normal sync activity, not errors.

Claims:

- "A user cannot unpublish a note published by the other share user." [ticket]: confirmed - The dialog shows no unpublish control on either client for the other user's note, at 17.3–24.7 s on the left and 37.4–40.9 s on the right. The share owner/recipient roles are not visible.
- "Clicking "copy sharable link" does not allow unpublishing on the latest dev." [ticket]: confirmed - After the click, "Link has been copied" appears and the dialog still has no unpublish icon (frame 0044.5; events p092 and the right client's click at 40.9 s). This was seen on both clients.
- "It is a regression from PR 15276 / commit 2c11cbb, and the sync fuzzer reproduces it." [ticket]: not shown - The video has no older build and no fuzzer run.
- "Setup: share a folder, accept it, then publish from either user." [ticket]: not shown - The video starts with the folder already shared. Who published which note is only inferred from the left client's "test" turning orange after the right client's "Copy Shareable Link" click.
- "It is also not possible to unpublish after the recipient is removed from the share." [ticket]: not shown - No user removal is shown.
