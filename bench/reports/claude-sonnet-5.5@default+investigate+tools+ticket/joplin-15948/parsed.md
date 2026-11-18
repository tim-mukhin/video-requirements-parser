# real/joplin-15948

_claude-sonnet-5.5@default, 26 s; looked at: frames/0003.0.jpg, frames/0006.5.jpg, frames/0009.0.jpg_

In a shared notebook, two notes are multi-selected and deleted with 'Delete note'. They vanish with a green 'successfully moved to the trash' toast, and the next sync brings them back. The app accepts a delete it cannot persist, so the success toast misleads.

## Multi-selected notes in a shared notebook can be deleted locally, then reappear after sync

Class: **state-revert**

Environment: Joplin desktop (Linux, dark theme). Two notebooks named 'Test' with share icons (5 and 3 notes). Notebook 'Test' with 3 notes (Test 1, 2, 3) is open. The video has no audio and shows no version or sync target. Cursor followed for 89% of the video. Clicks are inferred.

Steps:

1. In the shared notebook 'Test' (3 notes), click Test 3, then select Test 2 as well (a multi-select click at 355,127). The editor pane turns into the multi-note action panel (Tags, Move to notebook, Duplicate, Delete note, ...). The way the second note was added to the selection is not visible. (00:01.5; p007, p015, p018, p019)
2. Click 'Delete note'. The list drops to Test 1, the notebook count goes 3 to 1, and a toast says 'The notes were successfully moved to the trash.' No read-only warning is shown. (00:06.5; p039, p040)
3. Click 'Synchronize'. The sync reports 'Updated remote items: 2' and completes at 15:29. The count then rises back to 3 and Test 2 and Test 3 are back in the list; the last-sync time is 15:30. (00:07.7; p043, p044, p046, p047, p048)

Expected (implied): Read-only notes cannot be deleted at all, not even temporarily. Delete should be blocked or disabled, or at least show a warning, for a selection containing them.

Actual: Delete is accepted for both notes and a success toast appears. The notes disappear locally, then the sync restores them. The sync summary shows 'Updated remote items: 2' before the notes return, but the video does not show what that sync did on the server.

Key events: p015, p039, p040, p044, p046, p047, p048

Missed by the author:

- The success toast 'moved to the trash' is shown for notes the app cannot really delete, and it stays on screen after the notes come back (p040, frame 0009.0).
- The pointer hovered over 'Switch to to-do type' and 'Copy Markdown link' for about 2.5 s before the delete click. This is hesitation, not a finding (p037, p038).
- The author never opened Trash to see where the deleted notes went.

Claims:

- "Multiple read-only notes can be selected and Delete clicked" [ticket]: confirmed - Test 2 and Test 3 are multi-selected in a notebook with a share icon (frame 0003.0), and Delete note is clicked (p039). The video does not show that the notes are read-only; it only shows the share icon.
- "The notes are deleted" [ticket]: confirmed - The count goes 3 to 1 and the toast confirms the move to trash (p040, frame 0006.5).
- "After sync the notes are recreated" [ticket]: confirmed - Test 2 and Test 3 are back and the count is 3 after the sync (p046, p047, frame 0009.0).
- "Joplin 3.7.9, Linux, Joplin Cloud" [ticket]: not shown - No version or sync target is visible. The Linux look of the window fits.
