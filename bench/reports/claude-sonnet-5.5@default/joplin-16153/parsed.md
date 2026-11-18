# real/joplin-16153

_claude-sonnet-5.5@default, 41 s; looked at: frames/000149.jpg, frames/000215.jpg, frames/001958.jpg, frames/001906.jpg, frames/001841.jpg, frames/000760.jpg_

The video has no audio. It shows two Joplin DEV desktop windows (macOS on the left, a Fedora VM on the right) sharing a notebook "Test" with two notes. Several times the author opens Publish note... and clicks "Copy Shareable Link". Each time a sync starts, then "Link has been copied to clipboard!" appears. The video never shows the clipboard contents or any visible failure, so what is wrong is not clear.

## "Copy Shareable Link" in Publish Notes triggers a sync; the copied link is never shown or verified

Class: **silent-fail**

Environment: Joplin (DEV) desktop with profile joplindev-desktop on macOS (left window) and on a Fedora Linux VM (right window, dark theme). Notebook "Test" is shown with a share icon and 2 notes: "test" and "Test". Clock reads Aug 5 3:22-3:23 PM. No accounts or organizations are visible.

Steps:

1. Open the note menu in the VM window (the trigger is not visible; a click at 2124,391 precedes it) and choose Publish note... (00:01.8; p005, p006, p014)
2. The Publish Notes dialog opens, listing the note "test". (00:03.4; p016)
3. Click "Copy Shareable Link". The "Synchronizing..." text and a "Cancel" button flash for 0.3 s. The sync button then returns to "Synchronize". (00:04.8; p026, p027, p028, p034)
4. "Link has been copied to clipboard!" appears. (00:05.1; p033)
5. Repeat on the macOS window and on the other note ("Test") via the context-menu Publish note.... Each time the sequence is: click Copy Shareable Link, then "Generating link...", then "Synchronizing..."/"Cancel", then the copied message. (00:17.9; p083, p084, p085, p088, p138, p139, p140, p142, p228, p230, p231, p232, p233)

Expected (implied): Copying a shareable link should only generate the link and copy it, and it should be clear that the link is valid. The video gives no spoken expectation, so this is inferred.

Actual: Every Copy Shareable Link click starts a full synchronisation first ("Synchronizing...", then Cancel), and only afterwards shows the "copied" message. The clipboard contents are never shown, so the video does not show whether the link works or what is wrong with it.

Key events: p026, p027, p028, p033, p084, p088, p139, p142, p230, p231, p233

Missed by the author:

- The sync is started silently by Copy Shareable Link and shows only for 0.2-0.3 s (p027, p084, p139, p231).
- The sync button label flickers (OCR reads "Cancel"/"Synchronise"/"Synchronize" in quick succession, p043, p044, p058, p059, p060). This is probably the same sync cycle.
