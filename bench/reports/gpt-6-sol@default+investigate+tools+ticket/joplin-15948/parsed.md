# real/joplin-15948

_gpt-6-sol@default, 37 s; looked at: frames/000075.jpg, frames/000093.jpg, frames/000234.jpg, frames/moments/p044.jpg, frames/000310.jpg, frames/000032.jpg, frames/000326.jpg, frames/moments/p036.jpg, frames/000055.jpg, frames/000083.jpg, frames/000270.jpg, frames/moments/p004.jpg, frames/000045.jpg, frames/000059.jpg, frames/000090.jpg, frames/moments/p005.jpg_

Joplin removes two selected notes from a shared notebook and confirms they were moved to the trash, but they return after synchronization. The video supports the temporary deletion reported in the ticket; it does not show the notes' read-only permissions.

## Selected notes in a shared notebook return after deletion and sync

Class: **state-revert**

Environment: Joplin desktop, shared notebook Test. The ticket reports Linux, Joplin 3.7.9 and Joplin Cloud; those details are not visible in the recording.

Steps:

1. Select Test 2 and Test 3 in the shared Test notebook. (00:01.5; p007, p015, p018)
2. Click Delete note in the multiple-selection panel. (00:06.5; p019, p039, p040)
3. Click Synchronize. (00:07.7; p043, p044, p046, p047, p052)

Expected (implied): Read-only notes should not be deletable, even temporarily.

Actual: Test 2 and Test 3 disappear and Joplin says the notes were successfully moved to the trash. After sync, both return to the list and the notebook count returns to 3.

Key events: p018, p019, p039, p040, p043, p044, p046, p047, p052

Missed by the author:

- Joplin explicitly confirms that the notes were moved to the trash [p040].
- Synchronization is already indicated as running after deletion, before the click on Synchronize [p040, p043].
- The frame-based watcher placed the Delete click around 4.5 s; the timeline places the click at 6.5 s [p039]. The brief earlier text changes are screen-reading artifacts, not a separate note-name change [p009, p011, p016, p017].

Claims:

- "Multiple selected notes can be deleted temporarily." [ticket: Current behaviour, steps 1–3]: confirmed - The selected notes disappear after Delete note and later return; their read-only status is not shown.
- "Sync recreates the notes." [ticket: Current behaviour, steps 4–5]: confirmed - Both notes return during the shown sync sequence, though the video cannot isolate the manual sync from synchronization already underway.
- "The notes are read-only and come from a Joplin Cloud share." [ticket: Current behaviour, step 1]: not shown - A share icon is visible, but permissions and the sync provider are not.
