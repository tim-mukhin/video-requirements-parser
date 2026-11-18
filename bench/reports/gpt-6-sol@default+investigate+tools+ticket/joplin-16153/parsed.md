# real/joplin-16153

_gpt-6-sol@default, 51 s; looked at: frames/0004.0.jpg, frames/0017.5.jpg, frames/0028.5.jpg, frames/0037.5.jpg, frames/0044.5.jpg, frames/moments/p140.jpg, frames/moments/p234.jpg, frames/0005.5.jpg, frames/0018.5.jpg, frames/0022.5.jpg, frames/0029.5.jpg, frames/0043.5.jpg, frames/0051.0.jpg, frames/moments/p052.jpg, frames/moments/p276.jpg, frames/moments/p143.jpg, frames/moments/p236.jpg, frames/moments/p248.jpg, frames/moments/p028.jpg, frames/moments/p235.jpg, frames/0025.5.jpg, frames/0032.5.jpg, frames/0036.0.jpg_

After the light-themed Joplin client publishes the shared note “Test”, the dark-themed client can copy its shareable link but shows no unpublish control. The publishing client shows a share icon for that note; the other client does not, leaving no visible way there to revoke the link.

## Shared note published in one client has no visible unpublish control in the other

Class: **silent-fail**

Environment: Two Joplin DEV desktop windows showing the shared notebook “Test”: a light-themed client and a dark-themed client in a Fedora Linux VM. The video does not identify their accounts or show a Joplin or Server version.

Steps:

1. In the light-themed client, select the capitalized note “Test” and choose “Publish note...” from its context menu. (00:26.2; p120, p122, p127, p139)
2. Click “Copy Shareable Link”; the dialog reports that the link was copied and shows a share icon beside “Test”. (00:29.0; p142, p143, p146)
3. Synchronize the dark-themed client, select “Test”, and choose “Publish note...” from its context menu. (00:33.9; p155, p162, p164, p187, p188)
4. In that client's Publish Notes dialog, click “Copy Shareable Link”. It reports success, but the dialog still has no share icon or unpublish control. (00:44.2; p230, p232, p238)

Expected (implied): The other user, particularly the share owner, can unpublish a published note in the shared folder.

Actual: The dark-themed client's dialog for “Test” offers only “Copy Shareable Link” and “Close”, both before and after copying the link. Unlike the light-themed client's dialog, it shows no share icon. The video does not show an unpublish action being executed or identify which client is the share owner.

Key events: p139, p142, p146, p155, p187, p188, p230, p232, p238, p280

Missed by the author:

- The notebook contains distinct notes named “test” and “Test”; the later comparison uses “Test” in both clients [p139, p188].
- The publishing client's dialog gains a share icon beside “Test”, while the other client's dialog lacks it [p143, p188]. The frames settle this contrast.
- The other client is synchronized before its dialog is opened [p155, p187]. Its brief synchronization state when copying the link ends in a success message, not an error [p236, p238].

Claims:

- "The other user cannot unpublish a note published in the shared folder." [ticket.md: Current behaviour]: confirmed - The other client's Publish Notes dialog has no visible unpublish control, including after its link is copied [p188, p230, p238]. Account ownership and an attempted unpublish operation are not shown.
- "The recording shows the folder being shared and the invitation accepted." [ticket.md: reproduction step 1]: not shown - The shared “Test” notebook is already present in both clients when the recording begins.
- "The share owner remains unable to unpublish after the publishing user is removed from the share." [ticket.md: Expected behaviour]: not shown - No removal from the share is recorded.
- "Clicking “copy sharable link” in the other client does not enable unpublishing." [ticket.md: Update]: confirmed - The dark-themed dialog reports that the link was copied but gains no unpublish control [p232, p238]; a later reopening still lacks one [p280].
- "The issue is a regression associated with the cited pull request or commits, also reproducible by the sync fuzzer." [ticket.md: Reporter's follow-ups and Sync fuzzer]: not shown - The recording contains no version comparison, commit information, or fuzzer run.
