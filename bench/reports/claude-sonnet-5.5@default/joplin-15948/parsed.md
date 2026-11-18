# real/joplin-15948

_claude-sonnet-5.5@default, 19 s; looked at: frames/000234.jpg, frames/000326.jpg_

In a shared notebook, the author deletes notes (the toast says they were moved to the trash) and then synchronizes. The deleted notes Test 2 and Test 3 reappear in the note list right after the sync. The deletion is undone without the user doing anything.

## Notes deleted in a shared notebook reappear after Synchronize

Class: **state-revert**

Environment: Joplin desktop, dark theme, Linux-style menu bar. The Test notebook (3 notes) is selected and shows a shared icon. The notebook list shows two Test notebooks (5 and 3). There is no audio, so nothing was said. The cursor is followed for 89% of the video; keys are not seen.

Steps:

1. Select notes in the note list of the Test (3) notebook. The list briefly flickers: 'Test 3' reads 'Rest 3' for 0.1 s, and Test 1/2 swap places. The selection of several notes is inferred, since keys are not visible. (00:01.5; p007, p009, p011, p013)
2. Click the note context or menu button at [355,127]. A menu opens with 'Delete note', 'Move to notebook', 'Export' and others. (00:02.2; p015, p018, p019)
3. Click 'Delete note'. The toast 'The notes were successfully moved to the trash' appears, and only Test 1 is left in the list. (00:06.5; p039, p040)
4. Click 'Synchronize'. The sync reports 'Updated remote items: 2'. (00:07.7; p042, p043)
5. After the sync completes, 'Test 2' and 'Test 3' are back in the note list. The Trash toast is still visible. (00:08.6; p044, p045, p046, p047)

Expected (implied): Deleted notes stay in the trash and do not return to the notebook after synchronization.

Actual: After Synchronize, the notes that were just trashed (Test 2, Test 3) reappear in the notebook's note list. The sync status changes from 15:29 (423ms) to 15:30 (479ms). The 'moved to the trash' toast is still on screen.

Key events: p040, p043, p045, p046, p047

Missed by the author:

- The list flickered at the start: 'Test 3' was briefly misrendered as 'Rest 3' after 0.1 s with no click, and Test 1 flashed in and out [p009, p011, p013].
- The sync status text 'Updated remote items: 2' flashed for 0.8 s just before the notes returned [p043].
