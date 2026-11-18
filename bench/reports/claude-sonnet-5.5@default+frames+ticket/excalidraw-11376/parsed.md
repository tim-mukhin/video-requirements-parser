# real/excalidraw-11376

_claude-sonnet-5.5@default, 28 s; looked at: frames/0000.0.jpg, frames/0004.0.jpg, frames/0008.0.jpg, frames/0012.0.jpg, frames/0016.0.jpg, frames/0020.0.jpg, frames/0024.0.jpg, frames/0002.0.jpg, frames/0010.0.jpg, frames/0014.0.jpg, frames/0018.0.jpg_

In the Excalidraw desktop app, the "Create a Folder" dialog opens with the name of the previously created folder in the Name field. The video shows this twice: "Constructor" on the first open and "Try1" on the second. The text is pre-selected, so typing replaces it, which makes this a minor annoyance.

## New Folder dialog is prefilled with the previously created folder's name

Class: **wrong-data**

Environment: Excalidraw desktop app on macOS, dark theme. Folder view Basics, under ExcaliDraw > OOPS, with existing folders Classes, Constructor and Object. The version (1.7.3) is not visible in the frames. The end of the video shows the macOS screen-capture toolbar.

Steps:

1. In the Basics folder view, click the "New Folder" button (cursor on the button; the click itself is inferred). (00:02.0; 0002.0)
2. The "Create a Folder" dialog opens. The Name field is prefilled with "Constructor" (selected), not empty. Constructor is the existing folder that was already there when the video started, which is probably the last one created. (00:04.0; 0004.0)
3. Type a new name. The field shows "Try", then "Try1". The selected text is replaced as typed. (00:08.0; 0008.0, 0010.0)
4. Confirm with Create (inferred, since the click or Enter is not visible). The dialog closes and the new folder "Try1" appears in the list. (00:12.0; 0012.0)
5. Click "New Folder" again. The dialog opens with "Try1" prefilled (selected) instead of an empty or default name. (00:14.0; 0014.0, 0016.0)
6. The cursor moves to Cancel and the dialog closes. No second folder is created. (00:18.0; 0018.0, 0020.0)

Expected (implied): The New Folder dialog opens with an empty field or a default placeholder such as "Untitled Folder", not the previous folder's name (the ticket's expectation).

Actual: The Name field is prefilled with the previously used folder name. The text is selected, so the first keystroke overwrites it.

Key events: 0004.0, 0014.0, 0016.0

Missed by the author:

- The very first dialog open already shows the prefill "Constructor" (0004.0), so the problem is not limited to the second open in the same session.
- The prefilled text is selected (0004.0, 0016.0), which the ticket does not mention.
- Cancelling the second dialog (0018.0) was not part of the ticket's steps.

Claims:

- "The input is prefilled with the last created folder's name (Try1) when New Folder is clicked again." [The input field is prefilled with the string from the last created folder (e.g., Try1).]: confirmed - Frames 0014.0 and 0016.0 show "Try1" in the field after Try1 was created.
- "The user has to backspace or select all to clear the text." [This requires the user to manually backspace or select all text to delete it.]: refuted - The prefilled text is highlighted (selected) in 0004.0, 0014.0 and 0016.0, so typing replaces it. Typing over it in 0008.0 shows this. This is a smaller annoyance than the ticket describes.
- "Steps 1-4 reproduce the issue." [Click New Folder, type a name, confirm, click New Folder again.]: confirmed - Frames 0002.0 to 0016.0 follow these steps.
