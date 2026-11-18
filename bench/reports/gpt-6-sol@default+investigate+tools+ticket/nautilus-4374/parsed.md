# real/nautilus-4374

_gpt-6-sol@default, 42 s; looked at: frames/000030.jpg, frames/000062.jpg, frames/000105.jpg, frames/000119.jpg, frames/moments/p005.jpg, frames/000142.jpg, frames/0000.0.jpg, frames/0001.5.jpg, frames/0002.5.jpg, frames/0011.0.jpg, frames/0014.0.jpg, frames/0015.0.jpg, frames/0002.0.jpg_

GNOME Files carries a slash-validation warning from a PNG rename into a new rename of the folder `final`, even though that name has no slash. The stale warning disables Rename until the name field is interacted with.

## Slash warning persists when renaming a different item

Class: **error-shown**

Environment: GNOME Files, Home / Downloads / out-viola. The ticket reports Nautilus 51.1 on Bazzite 51; the video does not show the version or distribution.

Steps:

1. Open Rename for `viola-page000.png` (the menu trigger and selection are not visible). (00:02.0; p001)
2. Enter a slash in the filename; the slash warning appears. (00:02.9; p001)
3. Dismiss the rename popover (the dismissal trigger is not visible). (00:06.2; p002)
4. Open the context menu for folder `final` (the trigger is not visible), then open Rename (the selection is not visible). (00:10.6; p003, p004)

Expected (implied): A new rename operation for `final` should not retain the previous item's slash warning.

Actual: At 12.0 s, Rename Folder shows the unchanged name `final` alongside “File names cannot contain ‘/’” and a disabled Rename button [p004]. The warning disappears and Rename becomes enabled after interaction with the name field, without a visible name change [p005, p006].

Key events: p001, p002, p003, p004, p005, p006

Missed by the author:

- The second rename targets the folder `final`, not the original PNG; its valid name is shown while the stale warning disables Rename [p003, p004].
- The warning clears and the popover shifts upward without a visible change to `final`; the moment strip shows the shift is tied to the warning disappearing, not a separate layout problem [p005, p006].

Claims:

- "Entering a slash triggers the warning." [ticket.md]: confirmed - The PNG rename field contains a slash when the warning appears [p001].
- "The warning persists into a new rename operation whose name has no slash." [ticket.md]: confirmed - The folder rename field reads `final` while the slash warning remains visible [p004].
- "The popover was closed by clicking outside or pressing Escape." [ticket.md]: not shown - The popover disappears, but the video shows neither mouse nor keyboard input [p002].
- "This happens only in the same window or tab, on any file or folder." [ticket.md]: not shown - The video demonstrates one subsequent folder rename in the same window; it does not test other windows, tabs or targets [p003, p004].
