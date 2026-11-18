# real/excalidraw-11376

_claude-sonnet-5.5@default, 26 s; looked at: frames/0004.5.jpg, frames/0010.5.jpg, frames/0003.5.jpg, frames/0008.5.jpg, frames/0012.0.jpg_

In the Excalidraw desktop app, the Create a Folder dialog opens with the previously used folder name already in the Name field, selected. The video shows it on the first open (Constructor) and again after Try1 was created. Impact is minor friction, but the dialog does not reset.

## New Folder dialog is prefilled with the previously created folder's name

Class: **wrong-data**

Environment: Excalidraw desktop app on macOS, dark theme, no audio. Folder view ExcaliDraw > OOPS > Basics, with existing folders Classes, Constructor and Object. The version 1.7.3 from the ticket is not visible in the video.

Steps:

1. In Basics, click New Folder (the trigger is not visible; the cursor was last seen on the button at 2 s). The dialog opens with Name = "Constructor", selected, and Create enabled. (00:03.2; p002)
2. The Name field then shows the placeholder "My new group" and Create is greyed, so the text was cleared (keys are not seen). The ticket's reading is that the user has to delete the prefill by hand, and that is consistent with what the frames show. (00:04.0; p010)
3. Type "Try1" and confirm (the confirm action is not seen). The dialog closes and the folder "Try1" appears in the list. (00:06.7; p012, p014, p015, p017)
4. Click New Folder again. The dialog opens with Name = "Try1" prefilled and selected, not empty. The frames show the same prefill until 16.6 s. (00:09.8; p020)

Expected (implied): The Name field is empty or shows a default or placeholder such as "Untitled Folder"/"My new group" on each open (the ticket's expectation; the video's own placeholder "My new group" shows the app has one).

Actual: The field opens already filled with a previously used name: "Constructor" on the first open, "Try1" on the second. The text is selected, and Create is enabled for a duplicate name.

Key events: p002, p010, p020

Missed by the author:

- The first open already shows the prefill ("Constructor" at 3.2 s) before anything was created in the recording [p002].
- At 4.0 s the field changes to the placeholder "My new group", showing that an empty state exists and Create is disabled then [p010].
- The second dialog closes at about 16.6 s with no folder created [p028-p030]. A macOS screen-capture toolbar then appears at 19.7 s, which is outside the bug [p042].

Claims:

- "Reopening New Folder after creating Try1 shows Try1 in the input." [ticket]: confirmed - Frames 0010.5 and p020 show Name = Try1 selected after the Try1 folder appeared (0012.0).
- "The user has to backspace or select all to clear the text." [ticket]: not shown - The text is highlighted (selected), so typing would replace it. At the first open the field was emptied between 3.5 s and 4.0 s without any visible input. On the second open it was never cleared or typed over, and the dialog was dismissed at about 16.6 s.
- "The dialog does not clear its state after a folder is created." [ticket]: confirmed - Try1 returns after creation. The prefill of "Constructor" at the start suggests the same stale state was present before recording.
- "App Version 1.7.3 (59)." [ticket]: not shown - No version is visible in the frames.
