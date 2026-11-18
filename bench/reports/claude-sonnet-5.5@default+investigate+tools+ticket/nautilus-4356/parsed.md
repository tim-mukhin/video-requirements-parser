# real/nautilus-4356

_claude-sonnet-5.5@default, 19 s; looked at: frames/0004.0.jpg_

In Nautilus, the Rename File popover is open on file.txt. The text context menu then opens underneath the popover, so its upper items (Cut, Copy, most of Paste) are covered. Only Delete, Select All, Change direction and Insert Emoji are readable. The video matches the ticket.

## Text context menu opens behind the Rename popover, hiding its top items

Class: **wrong-data**

Environment: Nautilus (GNOME Files, libadwaita style), folder Home/Downloads/temp containing file.txt. The window is partly cropped. OS, Nautilus version and display server are not visible.

Steps:

1. With Home/Downloads/temp open, file.txt is selected and the Rename File popover is shown with the name field. The key press or click that opened it is not visible. (00:00.9; p001, p002, p003)
2. The text context menu appears below the field. The trigger is not visible (no cursor is shown); the ticket says it is a right-click in the filename field. Cut, Copy and most of Paste are covered by the popover. Only Delete, Select All, Change direction and Insert Emoji are readable. (00:02.0; p004)
3. The menu stays open to about 9.5 s. Its visible items change colour, which looks like hover highlighting, and the top items remain covered. (00:02.8; p005, p014)

Expected (implied): The text context menu should be drawn above the rename popover with all items (Cut, Copy, Paste, and so on) visible and usable.

Actual: The menu is drawn beneath the popover. Its upper items are hidden. In frame 0004.0 only the bottom edge of 'Paste' shows under the popover's lower edge.

Key events: p004, p005, p014

Missed by the author:

- The visible menu items change colour over time (p005 to p013 at 2.8 s, p014 to p022 at 6.0 s), consistent with hover highlighting, so the covered menu is still live.

Claims:

- "The context menu is displayed behind the rename popover." [ticket]: confirmed - Frames 0004.0 to 0009.5 show the popover overlapping the top of the menu.
- "Its options are hidden or inaccessible." [ticket]: confirmed - Cut, Copy and most of Paste are covered. The lower items are visible and appear to react to hover, so the menu is only partly inaccessible.
- "Fedora 44, GNOME Shell 50.6, Nautilus 50.4, Wayland." [ticket]: not shown - No version or display-server information is visible.
- "The user right-clicks in the filename field." [ticket]: not shown - No cursor or clicks are visible in the video.
