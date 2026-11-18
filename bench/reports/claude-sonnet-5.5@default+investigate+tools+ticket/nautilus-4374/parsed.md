# real/nautilus-4374

_claude-sonnet-5.5@default, 21 s; looked at: frames/0012.0.jpg, frames/0005.0.jpg_

In Nautilus, a '/' typed into the rename popover shows the warning "File names cannot contain "/"". After the popover is dismissed, a later rename popover on a different item (the folder "final") opens with the same warning, although its name has no '/'. The warning clears only after the text is edited.

## Stale "File names cannot contain '/'" warning shown when the rename popover is reopened

Class: **state-revert**

Environment: Nautilus (GNOME Files), Home/Downloads/out-viola, dark theme, one window. Items: folder "final" and viola-pageNNN.png files. The version is not visible in the video; the ticket says 51.1 on Bazzite 51. The video has no audio, and neither the cursor nor keys are visible.

Steps:

1. Open the Rename File popover on viola-page000.png (the trigger is not visible) and type '/'. The name becomes "viola-page000/.png" and the warning appears. (00:02.9; p001)
2. Dismiss the popover (the trigger is not visible; the ticket says Esc or a click outside). By 5.0 s the file list is back with no popover, and the popover text is gone from the screen by 6.2 s. (00:06.2; p002)
3. Open the context menu on the folder "final" and choose Rename... (F2). The menu is on screen at 10.6 s (the click is not visible). (00:10.6; p003)
4. The Rename Folder popover opens with the unchanged name "final". It already shows the warning "File names cannot contain "/"" and the Rename button is dimmed. (00:12.0; p004)
5. The warning box moves up 41 px at 13.8 s and the warning disappears at 14.4 s, after the name is edited (the edit is not visible in the timeline). (00:13.8; p005, p006)

Expected (implied): A new rename popover starts clean: no warning, and Rename enabled for a name without '/'.

Actual: The popover for "final" opens with the old '/' warning and a dimmed Rename button, although the name "final" has no '/'. The warning clears only after the text is edited.

Key events: p001, p002, p004, p005, p006

Missed by the author:

- The Rename button is dimmed while the stale warning shows, so an unchanged name cannot be confirmed (p004).
- The warning wording is "File names" even for a folder, whereas the ticket title says "File / Folder names" (p004).
- The dismissed popover still held a second slash, "viola-page000//.png", at 6.2 s (p002).

Claims:

- "Typing '/' in the rename popover triggers the warning." [ticket]: confirmed - p001 shows "File names cannot contain "/"" with the name "viola-page000/.png" at 2.9 s.
- "The warning persists into a new rename session on another file or folder." [ticket]: confirmed - The frame at 12.0 s (p004) shows the Rename Folder popover for "final" with the warning and a dimmed Rename button.
- "This happens only in the same window or tab." [ticket]: not shown - Only one window appears in the video.
