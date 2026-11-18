# real/excalidraw-5570

_claude-sonnet-5.5@default, 30 s; looked at: frames, frames/0000.0.jpg, frames/0003.0.jpg, frames/0006.0.jpg, frames/0009.0.jpg, frames/0012.0.jpg, frames/0015.0.jpg, frames/0018.0.jpg, frames/0001.0.jpg, frames/0002.0.jpg, frames/0002.5.jpg, frames/0011.5.jpg, frames/0016.5.jpg, frames/0019.5.jpg_

On Chrome for Android, a long-press on a selected rectangle near the bottom of the screen shows the context menu. On the first attempt the menu is fully visible. On the second attempt it opens at the bottom edge and is mostly cut off. It then keeps shifting position between frames and cannot be scrolled into view, so most items are unreachable.

## Context menu opens clipped at the bottom of the screen and keeps repositioning on Android Chrome

Class: **wrong-data**

Environment: Android phone (status bar shows about 8:52–8:53 AM), Chrome browser, excalidraw.com in a tab. A single rectangle is selected near the bottom of the canvas. The Pixel 4A mentioned in the ticket is not identifiable from the video.

Steps:

1. Start with a rectangle selected near the bottom of the canvas; the hint reads 'Press Enter to add text'. (00:00.0; 0000.0, 0001.0)
2. Long-press the rectangle (inferred, the touch is not visible). The full-height context menu (Cut, Copy, Paste ... Delete) appears above the shape, fully inside the screen. The hint text changes to 'Hold Ctrl to deep select'. (00:02.5; 0002.0, 0002.5, 0003.0)
3. The menu is dismissed (inferred, no tap is visible) and the canvas is idle. (00:06.0; 0006.0, 0009.0)
4. Long-press the rectangle again. This time the menu appears at the bottom edge with only Cut, Copy and Paste visible; the rest is off-screen. (00:11.5; 0011.5, 0012.0)
5. The clipped menu moves between frames: x about 160–185 and y about 662–725. It never moves up to fit the screen. (00:15.0; 0015.0, 0016.5, 0018.0, 0019.5)

Expected (implied): The context menu should open at a stable position that fits within the viewport, or be scrollable, so every item can be reached.

Actual: The first open shows the whole menu. The second open places it at the bottom edge, mostly off-screen, and its position keeps changing. Most items cannot be reached. The behaviour is inconsistent between attempts.

Key events: 0003.0, 0012.0, 0016.5, 0018.0, 0019.5

Missed by the author:

- On the first open (0002.5–0003.0) the menu is fully visible and correctly placed, so the bug is inconsistent between two identical actions.
- In the second open the menu is clipped by the bottom edge of the screen and overlaps the bottom toolbar (0012.0, 0018.0).

Claims:

- "The context menu is displayed and then repositioned." [the context menu is displayed, then repositioned]: confirmed - Between 0012.0 and 0019.5 the menu position shifts, with y moving from about 705 to 725 and 662, and x also changing.
- "The issue happens on Chromium browsers on Android." [it did appear when using a chromium browser]: confirmed - The recording shows Chrome on Android with the symptom. Other browsers and devices are not shown.
- "Context menu scrolling does not work consistently." [context menu scrolling not working consistently on Android]: not shown - No scrolling gesture is visible. Only the inconsistent placement is visible: one open is fully visible and one is clipped.
