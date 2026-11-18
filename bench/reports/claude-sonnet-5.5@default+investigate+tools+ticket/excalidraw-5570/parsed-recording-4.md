# real/excalidraw-5570

_claude-sonnet-5.5@default, 28 s; looked at: frames/0003.0.jpg, frames/0003.5.jpg, frames/moments/p004.jpg, frames/0002.5.jpg, looks/0002.10-0003.00-150_150_280_650/sheet.jpg_

On an Android Chromium browser at excalidraw.com, a context menu opens on a selected rectangle and covers most of the canvas, including the right half of the bottom toolbar. The menu appears at one stable position with no visible reposition or scroll, so recording-4 does not show the ticket's 'displayed, then repositioned' behaviour. The open and dismiss cycle repeats about every 2.3 s.

## Context menu on mobile Chromium is taller than the free area and overlaps the bottom toolbar; no repositioning or scrolling visible

Class: **wrong-data**

Environment: Phone-sized portrait screen (480×800) in a Chromium-based mobile browser at excalidraw.com. A single rectangle at the bottom-left of the canvas. The clock reads 8:58 AM. Device and browser version are not visible; the ticket says Pixel 4A, Chrome 104.

Steps:

1. Rectangle is on the canvas, nothing selected; the page has loaded. (00:00.0; u001)
2. Rectangle becomes selected, and the 'Hold Ctrl to deep select' hint appears (the touch that did this is not visible). (00:01.7; p001)
3. Context menu (Cut … Delete) opens at the right of the screen and covers the bottom toolbar's centre and right. It is first seen at about 2.57 s, in the same position until it closes. The opening trigger is not visible, and it is probably a long-press. (00:02.2; p003, p004)
4. Menu and selection disappear at about 3.2 s. Then repeat: the same cycle recurs at 4.4, 6.7, 8.9, 11.2, 13.3, 15.5, 17.7, 19.9 and 22.0 s. (00:03.2; p005, p008, p013, p018, p022, p026, p031, p037, p042, p047)

Expected (implied): The menu should fit the viewport, or be scrollable, and open once at its final position.

Actual: The menu is about 530 px tall (y≈217–745) on an 800 px screen. It hides the centre and right of the selection toolbar and is not scrollable in view. At 0.04 s frame spacing (2.57–2.98 s) it appears at one position and does not jump. The reposition from the ticket is not seen in this recording.

Key events: p003, p004, p005, p008

Missed by the author:

- The menu overlaps the bottom toolbar and hides its centre and right buttons (p003).
- The menu is about 530 px tall and takes up most of the canvas (p003).

Claims:

- "The context menu is displayed, then repositioned (Pixel 4A)." [ticket]: not shown - At 0.04 s spacing around 2.57–2.98 s the menu appears once at a fixed position and does not move. Other cycles were not checked frame by frame.
- "Context menu scrolling does not work consistently." [ticket]: not shown - No scroll gesture or scrolled menu appears in the video.
- "Other devices (Note 8, iPhone 5SE, Xiaomi, Motorola) behave differently." [ticket]: not shown - The video shows only one device.
