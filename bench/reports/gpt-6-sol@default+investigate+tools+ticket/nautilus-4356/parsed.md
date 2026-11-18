# real/nautilus-4356

_gpt-6-sol@default, 29 s; looked at: frames/moments/p008.jpg, frames/moments/p017.jpg, frames/moments/p020.jpg, frames/moments/p022.jpg, frames/0002.5.jpg, frames/0006.5.jpg, frames/0000.0.jpg, frames/0001.5.jpg, frames/0003.5.jpg, frames/0005.5.jpg, frames/0008.5.jpg_

In Nautilus, the filename text context menu opens behind the Rename File popover, which covers its upper options. The visible lower options still respond to hover, but the obscured options cannot be used normally.

## Filename text context menu is obscured by Rename File popover

Class: **silent-fail**

Environment: Nautilus, Home / Downloads / temp, file.txt. The ticket reports Fedora Linux 44, GNOME Shell 50.6, Nautilus 50.4, and Wayland; these details are not visible in the video.

Steps:

1. With file.txt selected, open Rename File (the trigger is not visible). (00:00.9; p001, p003)
2. Open the filename field's text context menu (the trigger is not visible). (00:02.0; p004)

Expected (implied): The text context menu remains fully visible in front of the rename popover.

Actual: The rename popover covers the menu's upper options. Delete, Select All, Change direction, and Insert Emoji remain visible below it. The direct frames establish the overlap; the short-event strips show hover highlighting, not disappearing menu content.

Key events: p003, p004, p008, p016, p017

Missed by the author:

- The video shows file.txt in Home / Downloads / temp, with the basename selected for renaming [p001, p003].
- The lower menu entries remain visible and change highlight; the apparent drawing changes in the short-event strips are not evidence that the menu vanished [p008, p016, p017].

Claims:

- "The text context menu appears behind the rename popover, hiding options." [ticket.md: Description and Actual result]: confirmed - The frames show the popover covering the menu above Delete.
- "The hidden options cannot be accessed." [ticket.md: Actual result]: not shown - No attempt to activate a covered option is visible; lower options do respond to hover.
- "F2 or the file context menu started renaming, followed by a right-click in the filename." [ticket.md: Steps to reproduce]: not shown - The video shows neither keys nor a cursor; the popover and text menu appear without visible triggers.
- "The reported Fedora, GNOME, Nautilus, and Wayland versions are shown in the recording." [ticket.md: Environment]: not shown - No version or display-server information appears on screen.
