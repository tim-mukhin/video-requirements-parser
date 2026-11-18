# real/excalidraw-5570

_gpt-6-sol@default, 60 s; looked at: frames/0004.0.jpg, frames/0004.5.jpg, frames/0011.5.jpg, frames/0015.0.jpg, frames/moments/p002.jpg, frames/moments/p026.jpg, looks/0003.95-0004.50-350_1300_646_800/sheet.jpg, looks/0000.65-0001.05-300_550_696_1450/sheet.jpg, looks/0011.10-0011.70-350_550_646_1450/sheet.jpg, looks/0014.55-0015.10-350_950_646_1050/sheet.jpg_

Excalidraw context menus initially appear within the Android browser viewport, then reposition so labels are cut off or lower commands fall below the screen. This makes menu options difficult to read or reach; the recording does not establish whether scrolling the menu fails.

## Context menus reposition outside the Android viewport

Class: **intermittent**

Environment: excalidraw.com in an Android browser, portrait view. The ticket identifies a Pixel 4A and Chrome 104.0.5112.69, but the recording does not verify the device model or browser version. The Obsidian plugin is not shown.

Steps:

1. With the circle selected, open its context menu (the trigger is not visible). The menu initially fits on screen. (00:00.7; p004)
2. Keep the menu open: it repositions to the right and down, cutting off labels and placing lower commands below the screen. (00:00.9; p005)

Expected (implied): The context menu remains within the viewport, with its labels readable and commands reachable.

Actual: The selected-circle menu moves from a fully visible position at 0.7 s to a clipped position at 0.9 s [p004, p005]. An empty-canvas menu likewise moves from fully visible at 4.0 s to beyond the right edge at 4.2 s [p016, p017]. Later selected-circle openings also place lower commands below the screen [p043, p044, p055, p056]. No menu-scroll attempt is identifiable.

Key events: p004, p005, p016, p017, p043, p044, p055, p056

Missed by the author:

- The empty-canvas menu also shifts right while open, truncating its labels [p016, p017]; the frames settle that the change is not merely an OCR difference.
- Selected-circle menus extend below the viewport after repositioning, hiding lower commands [p043, p044, p055, p056].
- The recording shows excalidraw.com directly, not the Obsidian Excalidraw plugin [p004].

Claims:

- "The context menu is displayed, then repositioned." [ticket.md]: confirmed - The timeline records both position changes; the frames show the menus before and after they shift [p004, p005, p016, p017].
- "Context-menu scrolling does not work consistently." [ticket.md]: not shown - Commands fall below the viewport, but no identifiable scrolling gesture or response is recorded.
- "The recording is from a Pixel 4A using Chrome 104.0.5112.69." [ticket.md]: not shown - The screen shows an Android browser at excalidraw.com, not its device model or browser version.
- "The behavior differs on the other phones and browsers named in the ticket." [ticket.md]: not shown - This recording shows only one browser session.
