# real/excalidraw-5570

_claude-sonnet-5.5@default, 39 s; looked at: frames, frames/0000.0.jpg, frames/0002.0.jpg, frames/0004.0.jpg, frames/0006.0.jpg, frames/0008.0.jpg, frames/0010.0.jpg, frames/0012.0.jpg, frames/0014.0.jpg, frames/0016.0.jpg, frames/0001.0.jpg, frames/0001.5.jpg, frames/0003.0.jpg, frames/0009.0.jpg, frames/0010.5.jpg, frames/0011.0.jpg, frames/0013.0.jpg, frames/0017.0.jpg_

On a Pixel 4A in Chrome, the Excalidraw context menu on a selected circle opens clipped by the right screen edge and does not scroll. Later menus on the same circle open at different positions: one is cut off at the bottom and one at the right. The menu position is inconsistent, and some items (Delete, Lock) can be unreachable.

## Context menu opens clipped at screen edges and at inconsistent positions on Android Chrome

Class: **intermittent**

Environment: Android phone (Pixel 4A per the ticket) with Chrome, excalidraw.com in a browser tab (12 tabs open), portrait, screen recording active. Mobile layout with a bottom action bar. Only a single hand-drawn circle is on the canvas.

Steps:

1. With the circle selected (handles visible), the user long-presses it. The context menu opens with its left edge at x≈675, so the right part of the menu is cut off by the screen edge. (00:01.0; 0001.0, 0002.0)
2. The menu stays at the same place and clipped (inferred: still held). The long-press seems to be released or the menu replaced. (00:03.0; 0003.0)
3. A different menu is shown: the canvas menu (Paste, Copy as PNG/SVG, Select all, Show grid...). The circle is deselected. This menu is at another position, x≈455 to 900. (00:04.0; 0004.0)
4. The menu is dismissed and the canvas is empty (inferred: a tap outside). (00:06.0; 0006.0, 0007.0)
5. The circle is selected again after a tap or drag. It sits at the far right edge of the screen, partly off-screen. (00:08.0; 0008.0)
6. The context menu opens for the circle, now at the left. The menu's bottom is cut off by the screen edge: 'Lock' and 'Delete' are not visible and the menu does not scroll. (00:10.0; 0010.0)
7. The menu is closed. The circle is deselected. (00:11.0; 0011.0)
8. The menu is opened again and is placed lower and further left than before. It is cut off at the bottom (Flip vertical cut off). (00:12.5; 0012.5, 0013.0, 0017.0)

Expected (implied): The context menu appears fully inside the viewport, or is scrollable, at a stable position next to the touch point. All items, including Delete, are reachable.

Actual: The menu is clipped by the screen edge on the right in the first menu (0001.0 to 0003.0) and at the bottom in the later menus (0010.0, 0013.0, 0017.0). Its position changes between openings and between frames, and the menu content changes from object menu to canvas menu in 0003.0 to 0004.0. Bottom items are not reachable by scrolling in the frames.

Key events: 0001.0, 0003.0, 0004.0, 0010.0, 0017.0

Missed by the author:

- The menu is clipped at the right edge on the first open and at the bottom edge on later opens, with Lock/Delete cut off (0001.0, 0010.0, 0017.0).
- A different (canvas) menu replaces the object menu at 0003.0 to 0004.0.
- The circle itself is at the far right of the screen in 0008.0 and at the left in 0010.0 (the view or the element moved).

Claims:

- "The context menu is displayed, then repositioned on the Pixel 4A." [As you can see the context menu is displayed, then repositioned.]: confirmed - The menu is at x≈675 in 0001.0 to 0003.0, and at x≈455 in 0004.0 (a canvas menu). The menus in 0010.0 and 0013.0 are at other positions. The change is visible in the frames, but a smooth reposition animation is not captured at 0.5 s steps.
- "Context menu scrolling does not work consistently." [context menu scrolling not working consistently on Android]: not shown - No scroll gesture is visible. Only clipped menus and varying positions are seen.
- "The issue does not appear on the Note 8 or iPhone." [ok on Samsung Note 8 / ok on iPhone 5SE]: not shown - The video shows only one device. The Chrome version is not visible.
