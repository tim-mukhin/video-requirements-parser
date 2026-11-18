# real/excalidraw-11376

_claude-sonnet-5.5@default, 27 s; looked at: frames/000002.jpg, frames/000499.jpg, frames/000347.jpg, frames/001216.jpg, frames/000154.jpg, frames/000184.jpg_

In an ExcaliDraw folder view (OOPS > Basics), the "Create a Folder" dialog opens with the Name field already filled with an existing folder's name. It showed "Constructor" the first time and "Try1" the second time. The field should be empty with the "My new group" placeholder. The video has no audio, so the author's intent is inferred from the screen.

## Create a Folder dialog is prefilled with an existing folder name instead of an empty field

Class: **wrong-data**

Environment: ExcaliDraw, dark theme, folder view ExcaliDraw > OOPS > Basics. Existing folders: Classes, Constructor, Object. No account or organization is visible.

Steps:

1. Click "New Folder" in the Basics folder view. The cursor is on the button and the dialog appears. (00:03.2; p002)
2. The dialog opens with Name = "Constructor" (selected), which is the name of an existing folder. The placeholder "My new group" only appears after the text is cleared, with Create greyed out. (00:04.0; p003, p010)
3. Type "Try1" and confirm. The Try1 folder (0 items) appears in the list. The confirm action is in the gap where the cursor is not followed, so it is not visible. (00:07.3; p012, p014, p015, p017)
4. Open New Folder again (the trigger is not visible). The dialog opens with Name = "Try1", the folder just created, prefilled and selected. (00:09.8; p020)

Expected (implied): A new Create a Folder dialog opens with an empty Name field showing the "My new group" placeholder, and Create disabled until a name is typed.

Actual: The Name field is prefilled with the name of an existing folder. First it was "Constructor", which is not the most recently created folder. Then it was "Try1", which already exists. Pressing Create without editing would make a duplicate name. The dialog then stays open for about 6 s and closes at 00:16.9. How it was closed is not visible, and no new folder appears.

Key events: p002, p003, p010, p017, p020, p029

Missed by the author:

- The first dialog is prefilled with "Constructor", an existing folder name (frame 000154, p003).
- The second dialog is prefilled with "Try1" although that folder already exists (p020, frame 000499).
- Small flashes of "R" and "4" at 00:10.4, 00:17.9 and 00:25.4 (p026, p033, p055) are most likely recording-tool UI or OCR noise, not app behaviour. The "Options Capture" bar at 00:19.7 (p042) looks like the screen-capture tool, not the app.
