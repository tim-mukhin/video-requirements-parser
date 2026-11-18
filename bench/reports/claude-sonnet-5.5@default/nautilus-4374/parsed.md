# real/nautilus-4374

_claude-sonnet-5.5@default, 21 s; looked at: frames/000030.jpg, frames/000119.jpg, frames/000062.jpg, frames/000105.jpg_

In Nautilus (Files), a Rename dialog for the folder "final" opens already showing the warning "File names cannot contain '/'", although the name is the valid, unchanged "final". The warning appears to carry over from an earlier rename dialog in which the user had typed a "/". This is misleading, and the Rename button looks dimmed.

## Rename Folder dialog shows stale "File names cannot contain '/'" error for a valid name

Class: **wrong-data**

Environment: Nautilus (GNOME Files), folder Home/Downloads/out-viola, containing the folder "final" and files viola-page000.png and later. No audio, and no cursor or keys are visible.

Steps:

1. Select viola-page000.png and open Rename File. The name field contains "viola-page000//.png" (a typed "/"), and the dialog legitimately shows "File names cannot contain '/'". The trigger for opening the dialog is not visible. (00:02.9; p001)
2. The dialog closes and the rename is cancelled or dismissed. The way it was closed is not visible. (00:06.2; p002)
3. The context menu opens on the folder "final", with Rename... (F2) available. The trigger is not visible. (00:10.6; p003)
4. The Rename Folder dialog opens with the unchanged name "final". The warning "File names cannot contain '/'" is already displayed, and the Rename button looks inactive. (00:12.0; p004)
5. The warning and then the dialog disappear. (00:14.4; p005, p006, p007, p008)

Expected (implied): A freshly opened Rename Folder dialog with the valid name "final" shows no warning, and its Rename button is in its normal state.

Actual: The Rename Folder dialog for "final" shows the "/" warning at once, although the name contains no "/". The message is likely left over from the previous Rename File dialog.

Key events: p001, p004, p005

Missed by the author:

- The first warning is correct, since the field contained "//" [p001].
- The second dialog shows the same warning with a valid name [p004]. No one comments on it because the video has no audio.
