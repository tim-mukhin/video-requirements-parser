# real/joplin-15948

_claude-sonnet-5.5@default, 23 s; looked at: frames/0000.0.jpg, frames/0002.0.jpg, frames/0004.0.jpg, frames/0006.0.jpg, frames/0008.0.jpg, frames/0009.5.jpg_

In a shared notebook with read-only notes, two notes are selected and deleted. The app reports success and the notes disappear, but after a sync they come back. The app lets the user delete notes it cannot really delete, so the deletion is only temporary and the success message is misleading.

## Read-only shared notes can be deleted locally with multi-select, then reappear after sync

Class: **state-revert**

Environment: Joplin desktop on Linux, dark theme, Markdown editor. Two notebooks are both named 'Test' and both show a share icon. The selected one has 3 notes. The ticket gives version 3.7.9 (dev) and a Joplin Cloud sync target. That version is not visible in the frames.

Steps:

1. Open the shared notebook 'Test' (3 notes: Test 1, 2, 3). Test 1 is open in the editor. (00:00.0; 0000.0)
2. Select Test 2 and Test 3 together. The editor pane switches to the multi-note action panel (Tags, Move to notebook, Duplicate, Delete note, ...). The selection method is inferred, since the click itself is not visible. (00:02.0; 0002.0)
3. Move the pointer to 'Delete note' and click it. The click is inferred, because the pointer is on the button in 0004.0 and the notes are gone by the next frame. (00:04.0; 0004.0)
4. The notes vanish from the list. The notebook count drops from 3 to 1 and the toast 'The notes were successfully moved to the trash' appears. No read-only warning is shown. (00:04.0; 0004.0)
5. Synchronize runs. Its button shows the spinning icon in 0004.0 and the last-sync time is updated to 15:30. (00:06.0; 0004.0, 0006.0)
6. After the sync, Test 2 and Test 3 are back in the list and the notebook count is 3 again. (00:08.0; 0008.0)

Expected (implied): Read-only notes should not be deletable at all, not even temporarily. Delete should be blocked or disabled for a selection that contains them.

Actual: Delete is accepted for read-only notes selected together. They disappear locally with a success toast, then the sync restores them.

Key events: 0002.0, 0004.0, 0006.0, 0008.0

Missed by the author:

- The app shows a green 'successfully moved to the trash' toast with a Cancel link for notes that cannot be deleted (0004.0, 0006.0).
- The Trash entry was never opened to check where the notes went.

Claims:

- "Multiple read-only notes can be selected" [Select multiple read-only notes (e.g. from a Joplin Cloud share)]: confirmed - Test 2 and Test 3 are multi-selected in a notebook with a share icon (0002.0). The video does not show that the notes are read-only.
- "Clicking Delete deletes the notes" [Click 'Delete'. Observe that the notes have been deleted.]: confirmed - The count goes from 3 to 1 and the toast confirms the move to trash (0004.0).
- "Notes are recreated after sync" [Sync. Observe that the notes have been recreated.]: confirmed - Test 2 and Test 3 are back and the count is 3 after the sync (0006.0 to 0008.0).
- "Version, OS and sync target" [Joplin 3.7.9 (dev, linux), Joplin Cloud]: not shown - The frames show none of this. The ticket does not mention that the sync was run in the video.
