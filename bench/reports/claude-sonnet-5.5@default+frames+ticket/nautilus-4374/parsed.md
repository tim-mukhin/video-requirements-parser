# real/nautilus-4374

_claude-sonnet-5.5@default, 27 s; looked at: frames, frames/0000.0.jpg, frames/0003.0.jpg, frames/0006.0.jpg, frames/0009.0.jpg, frames/0012.0.jpg, frames/0015.0.jpg, frames/0017.0.jpg, frames/0001.5.jpg, frames/0005.0.jpg, frames/0010.5.jpg, frames/0013.5.jpg_

In Nautilus, a rename popover shows the "File names cannot contain '/'" warning after a '/' is typed, and the popover is then dismissed. When the rename popover is opened later on another item (the folder "final"), the same warning and a disabled Rename button appear even though the name "final" has no slash. The stale state clears only after the name is edited again.

## Stale "cannot contain '/'" warning and disabled Rename button shown when reopening the rename popover on another item

Class: **state-revert**

Environment: Nautilus (GNOME Files) file list in Home/Downloads/out-viola, dark theme. Items: folder "final" and viola-pageNNN.png files. The version is not visible in the video; the ticket says 51.1 on Bazzite 51.

Steps:

1. Right-click viola-page000.png (inferred from the context menu) and choose Rename... from the menu. (00:01.5; 0001.5)
2. In the Rename File popover, a '/' is typed into the name, giving "viola-page000/.png". The Rename button is dimmed. The warning text is not visible in the sampled frame. (00:03.0; 0003.0)
3. Dismiss the popover without renaming (inferred as Esc or a click outside). The list is back with viola-page000.png focused, then the selection moves to "final". (00:05.0; 0005.0, 0006.0)
4. Right-click the folder "final" and choose Rename... from the context menu. (00:10.5; 0010.5)
5. The Rename Folder popover opens with the unchanged name "final". It already shows "File names cannot contain '/'" and the Rename button is dimmed. (00:12.0; 0012.0, 0013.5)
6. After the name is edited (a trailing space appears after "final"), the warning disappears and Rename becomes enabled. (00:15.0; 0015.0)

Expected (implied): A new rename popover starts with no warning and an enabled Rename button when the name has no '/'.

Actual: The new rename popover for "final" shows the old '/' warning and a disabled Rename button until the text is edited.

Key events: 0003.0, 0012.0, 0013.5, 0015.0

Missed by the author:

- The Rename button is also disabled while the stale warning shows (0012.0, 0013.5), so the user cannot confirm an unchanged name.
- The warning wording on screen is "File names cannot contain '/'" even for a folder, whereas the ticket title says "File / Folder names" (0012.0).
- The stale state goes away once the text is edited (0015.0).

Claims:

- "Typing '/' in the rename popover triggers the warning." [type a `/` character ... the warning is triggered]: not shown - '/' is typed at 3.0 and the Rename button is dimmed, but the warning text is not visible in the sampled frames.
- "The warning persists into a new rename session on another item after the popover is closed." [Open the rename menu again, on any file or folder, and see that the warning is present]: confirmed - The Rename Folder popover for "final" shows the warning at 12.0 and 13.5.
- "The warning is only present in the same window or tab." [(in the same window / tab only)]: not shown - Only one window is shown.
