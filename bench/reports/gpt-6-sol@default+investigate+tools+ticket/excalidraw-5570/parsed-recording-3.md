# real/excalidraw-5570

_gpt-6-sol@default, 44 s; looked at: frames/0004.5.jpg, frames/0009.0.jpg, frames/0009.5.jpg, frames/0011.5.jpg, frames/moments/p099.jpg, frames/moments/p025.jpg, frames/moments/p044.jpg, frames/moments/p064.jpg, frames/0002.0.jpg, frames/0013.0.jpg, frames/0001.5.jpg, frames/0006.0.jpg, frames/0007.5.jpg, frames/0012.5.jpg, frames/moments/p069.jpg, frames/000047.jpg, frames/000101.jpg, frames/000218.jpg, frames/moments/p093.jpg_

The selected rectangle’s context menu opens at inconsistent heights in the mobile-sized viewport. On some openings, most commands extend below the screen; on others, the full menu is visible.

## Context menu sometimes opens below the visible screen

Class: **intermittent**

Environment: excalidraw.com in a portrait, Chrome-style mobile browser. The device model and browser version are not visible.

Steps:

1. With the rectangle selected near the bottom of the canvas, open its context menu (the trigger is not visible). (00:04.2; p001, p024)
2. Repeat opening the menu (the triggers are not visible). (00:09.1; p043, p063, p070, p099)

Expected (implied): Position the menu so its commands remain visible and reachable.

Actual: At 4.2 s, the menu starts near the bottom edge and only its first commands are visible. At 9.1 s and 12.9 s, the full menu, including Delete, is visible higher up. Bottom-clipped openings recur at 11.2 s and 17.3 s. The recording does not show whether the clipped menu can be scrolled.

Key events: p003, p024, p043, p063, p070, p099

Missed by the author:

- The rectangle remains selected near the bottom while the menu opens both fully within the screen and clipped below it [p024, p043, p070].

Claims:

- "The context menu is displayed, then repositioned." [ticket.md]: not shown - This recording shows differently positioned openings separated by the menu closing, not a visible repositioning during one opening. The ticket describes a different recording.
- "Context-menu scrolling does not work consistently." [ticket.md]: not shown - Clipping is visible, but no scroll gesture can be identified.
- "The recording shows a Pixel 4A running Chrome 104.0.5112.69." [ticket.md]: not shown - The ticket identifies its Pixel 4A attachment as recording-1.mp4; this input is recording-3.mp4, and neither the model nor version appears on screen.
