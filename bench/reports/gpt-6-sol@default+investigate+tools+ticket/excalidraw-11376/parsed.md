# real/excalidraw-11376

_gpt-6-sol@default, 54 s; looked at: frames/0003.5.jpg, frames/0004.5.jpg, frames/0006.5.jpg, frames/0007.5.jpg, frames/0010.0.jpg, frames/0017.5.jpg, frames/moments/p021.jpg, frames/moments/p003.jpg, frames/0002.5.jpg, frames/0007.0.jpg, frames/0009.5.jpg, frames/0017.0.jpg, frames/moments/p026.jpg, frames/moments/p008.jpg, frames/moments/p059.jpg, frames/0019.5.jpg, frames/0022.5.jpg, frames/moments/p043.jpg, frames/moments/p050.jpg_

The New Folder dialog retains the last created folder name instead of opening with a fresh entry. The timeline establishes the creation and reopening sequence; the frames show that the retained name is already selected, so it can be replaced by typing.

## New Folder dialog retains the previous folder name

Class: **silent-fail**

Environment: Excalidraw, in ExcaliDraw > OOPS > Basics. The ticket reports a macOS desktop download, version 1.7.3 (59); the recording does not show the platform or version.

Steps:

1. Open New Folder (the trigger is not visible). The Name field contains selected text, Constructor. (00:03.2; p002)
2. Clear the field and enter Try1. (00:04.0; p010, p015)
3. Confirm creation (the trigger is not visible); the Try1 folder appears. (00:07.2; p016, p017)
4. Open New Folder again (the trigger is not visible). (00:09.8; p020)

Expected (implied): The Name field should be empty or show a default placeholder, not the previous folder name.

Actual: The reopened dialog contains Try1, selected. The frames confirm the retained value; the timeline records the dialog reopening at 9.8 seconds.

Key events: p002, p010, p015, p017, p020

Missed by the author:

- The first opening also contains a selected existing name, Constructor; its origin is not shown [p002].
- After the first name is cleared, the field shows the placeholder “My new group” and Create is disabled [p010].
- The later Capture controls and moving selection border belong to the screen-capture interface, not the folder dialog [p042, p043, p053].

Claims:

- "The previous folder name remains in the New Folder field." [ticket.md]: confirmed - Try1 appears as a created folder and is selected in the reopened dialog.
- "The user must manually backspace or select all before entering another name." [ticket.md]: refuted - The reopened dialog already has Try1 selected, so typing can replace it.
- "The recording shows macOS desktop version 1.7.3 (59)." [ticket.md]: not shown - No platform or version identification appears in the recording.
