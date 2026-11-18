# real/nautilus-4356

_claude-sonnet-5.5@default, 13 s; looked at: nothing_

In Nautilus, right-clicking the filename field during a rename opens the Cut/Copy/Paste menu behind the rename popover. The menu is hidden or unusable with the mouse. Keyboard shortcuts still work.

## Text context menu appears behind rename popover when right-clicking filename

Class: **wrong-data**

Environment: Fedora Linux 44, GNOME Shell 50.6, Nautilus 50.4, Wayland. Single Nautilus window; no accounts or organizations.

Steps:

1. Open Nautilus. (00:00.0; )
2. Select any file or folder. (00:00.0; )
3. Press F2 or choose Rename from the context menu. (00:00.0; )
4. While the filename is editable, right-click inside the filename text field. (00:00.0; )
5. Observe where the text context menu (Cut/Copy/Paste) appears. (00:00.0; )

Expected (speech): The text context menu appears above the rename popover and is fully visible and interactive.

Actual: The Cut/Copy/Paste context menu is drawn behind the rename popover, so its options are hidden or inaccessible.

Key events: 

Claims:

- "The context menu is displayed behind the rename popover." [right-clicking inside the editable filename field opens the text context menu behind the rename popover]: not shown - No video was available. This is the reporter's claim from the ticket text only.
- "Keyboard shortcuts (Ctrl+C/X/V) are not affected." [Keyboard shortcuts such as Ctrl+C, Ctrl+X, and Ctrl+V are not the issue]: not shown - Not verified; there is no video.
