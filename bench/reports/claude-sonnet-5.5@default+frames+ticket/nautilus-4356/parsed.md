# real/nautilus-4356

_claude-sonnet-5.5@default, 27 s; looked at: frames, frames/0000.0.jpg, frames/0002.0.jpg, frames/0004.0.jpg, frames/0006.0.jpg, frames/0008.0.jpg, frames/0010.0.jpg, frames/0001.0.jpg, frames/0003.0.jpg, frames/0011.0.jpg, frames/0003.5.jpg, frames/0009.5.jpg_

In Nautilus, the Rename File popover opens on file.txt. The text context menu then opens with its upper part (Cut/Copy/Paste) hidden behind the popover, so only Delete, Select All, Change direction and Insert Emoji are readable. The video confirms the ticket's report.

## Text context menu opens behind the Rename popover, hiding its top items

Class: **wrong-data**

Environment: Nautilus (GNOME Files, libadwaita style) in folder Home/Downloads/temp with one file, file.txt. The window is partly cropped. OS and version are not visible; the ticket says Fedora 44, GNOME Shell 50.6, Nautilus 50.4, Wayland.

Steps:

1. The folder Home/Downloads/temp is open and file.txt is selected. (00:00.0; 0000.0)
2. The rename popover appears, probably after F2 or Rename from the menu. The key press or click itself is not visible, but the popover is first seen at 2.0 s. The name field is focused and 'file' is selected. (00:02.0; 0002.0)
3. The text context menu appears below the field, probably from a right-click in the filename field. The right-click is inferred. Its upper items are hidden under the popover, and only the bottom of 'Paste' shows. The menu is first visible at 4.0 s. (00:04.0; 0004.0)
4. The menu stays open from 4.0 s to 9.5 s. Items are highlighted as the pointer moves over Delete and Change direction, so they are interactive. The top items (Cut, Copy, Paste) stay covered. (00:06.0; 0004.0, 0006.0, 0009.5)
5. The popover and the menu are gone, and only the file list remains. (00:11.0; 0011.0)

Expected (implied): The text context menu should be drawn above the rename popover, with every item fully visible and usable.

Actual: The menu is drawn under the popover. Cut, Copy and most of Paste are covered, and only the lower items are visible.

Key events: 0004.0, 0006.0, 0009.5

Missed by the author:

- The visible menu items highlight on hover (0006.0, 0008.0), so the menu is partly interactive, not fully blocked.
- The menu closes by 11.0 s with the file still named file.txt, so no rename happened (0011.0).

Claims:

- "The text context menu appears behind the rename popover." [displayed behind the rename popover]: confirmed - In frames 0004.0 to 0009.5 the popover's bottom edge overlaps the menu, and 'Paste' is cut off.
- "The options are hidden or inaccessible." [Its options are therefore hidden or inaccessible]: confirmed - The top items are covered. The visible items do respond with a hover highlight, so the menu is only partly inaccessible.
- "The problem occurs on Fedora 44 with Nautilus 50.4 on Wayland." [Fedora Linux 44 ... Nautilus 50.4 ... Wayland]: not shown - No version or display server information is visible.
