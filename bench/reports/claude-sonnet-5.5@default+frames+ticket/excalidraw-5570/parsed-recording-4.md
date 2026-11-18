# real/excalidraw-5570

_claude-sonnet-5.5@default, 31 s; looked at: frames, frames/0000.0.jpg, frames/0003.0.jpg, frames/0006.0.jpg, frames/0009.0.jpg, frames/0012.0.jpg, frames/0015.0.jpg, frames/0018.0.jpg, frames/0021.0.jpg, frames/0002.0.jpg, frames/0002.5.jpg, frames/0003.5.jpg, frames/0005.0.jpg, frames/0023.5.jpg_

On an Android Chromium-based browser at excalidraw.com, a long-press on a rectangle opens a context menu. The menu is about 530 px tall, covers most of the canvas and overlaps the bottom toolbar. The video repeats this open/dismiss cycle about every 3 s. At 0.5 s sampling I do not see the 'reposition after display' jump the ticket describes, and I see no scrolling.

## Context menu on mobile browser is oversized and overlaps the bottom toolbar; no scrolling or repositioning is visible

Class: **not-a-bug**

Environment: Android phone, Chromium-based mobile browser (title bar shows excalidraw.com, 8:58 AM). Excalidraw canvas with one rectangle at the bottom-left. Browser version and device are not visible; the ticket says Pixel 4A, Chrome 104.

Steps:

1. Start with a rectangle on the canvas and nothing selected. (00:00.0; 0000.0)
2. Inferred long-press on the rectangle: it becomes selected, with a 'Hold Ctrl to deep select' hint and the selection toolbar. (00:02.5; 0002.5)
3. The context menu (Cut ... Delete) appears at the right of the screen, spanning y≈217–745 px and covering the bottom toolbar's right part. Its x position differs by 1–3 px between frames (left edge at 203/202/204 px), which looks like an open animation. (00:03.0; 0003.0, 0005.0)
4. The menu is dismissed (inferred tap outside) and the selection is cleared. The same cycle repeats at about 6–7.5 s, 9–9.5 s, 12 s, 15 s, 18 s and 21 s. (00:06.0; 0006.0, 0009.0, 0012.0, 0015.0, 0018.0, 0021.0)

Expected (implied): The context menu should be positioned so it fits the viewport, or be scrollable if it does not fit, and should appear once at a stable position without a visible jump.

Actual: The menu is displayed at a fixed position and covers the bottom toolbar. No scroll of the menu is shown. A repositioning jump is not visible at this sampling rate; the only change between menu frames is a 1–3 px horizontal shift.

Key events: 0003.0, 0005.0, 0012.0

Missed by the author:

- The menu is about 530 px tall on a 800 px screen and overlaps the bottom selection toolbar, hiding the toolbar's centre and right buttons (0003.0).
- Menu items shift by a few pixels horizontally between frames (0003.0 vs 0005.0).

Claims:

- "The context menu is displayed, then repositioned." [As you can see the context menu is displayed, then repositioned.]: not shown - This is a different recording, with 0.5 s frame spacing. The menu looks the same in every frame it is visible; only a 1–3 px x shift appears (0003.0 vs 0005.0 vs 0012.0).
- "Context menu scrolling does not work consistently." [context menu scrolling not working consistently on Android]: not shown - No scroll gesture or scrolled menu appears in any frame.
