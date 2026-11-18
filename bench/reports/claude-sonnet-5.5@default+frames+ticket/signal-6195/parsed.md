# real/signal-6195

_claude-sonnet-5.5@default, 24 s; looked at: frames, frames/0000.0.jpg, frames/0002.0.jpg, frames/0004.0.jpg, frames/0006.0.jpg, frames/0008.0.jpg, frames/0009.5.jpg_

In Signal Desktop's image editor on macOS, drawing with the pen near the top edge of the canvas moves the whole window instead of drawing. Strokes are cut off, and the window drifts down and sideways. The top of the image can't be annotated.

## Drawing near the top of the image in the markup editor drags the window instead

Class: **wrong-data**

Environment: Signal Desktop (version 6.0.0-beta.3 per ticket, not visible in the video), image editor with the pen tool, green colour selected. The image is a tall white portrait image. macOS with a Ventura-style wallpaper. The window starts at the top-left of the screen.

Steps:

1. The image editor is open with the pen tool selected (green). The cursor is a crosshair over the canvas near its top. The window is flush with the top-left of the screen. (00:00.0; 0000.0)
2. The user draws a zigzag stroke near the top of the image (inferred: mouse pressed and dragged). The window is already about 15 px lower than at 0 s, and the top of the stroke is clipped at the canvas edge. (00:02.0; 0002.0)
3. The user presses at the top edge and moves right. The window moves down and right with the cursor instead of drawing, and the window's top-left corner shifts. (00:04.0; 0004.0)
4. A new stroke begins near the top. Only a tiny fragment is drawn and the window keeps moving. The window is lower again, about 85 px from the top. (00:06.0; 0006.0)
5. The drawn marks are fragmentary: a short mark at the top and only a partial stroke. The window has shifted position again. (00:08.0; 0008.0)
6. A further stroke is drawn near the top edge. It is partly clipped and the window sits at a different position than at 0 s. (00:09.5; 0009.5)

Expected (implied): Pressing and dragging on the canvas near the top draws a stroke. The window does not move, or the canvas does not extend into the window-drag region.

Actual: Drags starting near the top of the canvas move the Signal window rather than drawing. The window position changes between frames (0 s, 2 s, 4 s, 6 s, 8 s, 9.5 s) while strokes are cut short or clipped.

Key events: 0000.0, 0002.0, 0004.0, 0006.0, 0009.5

Missed by the author:

- The window ends up in a different place than where it started, and it moved even during strokes that look partly drawn (0002.0 to 0009.5).
- Part of the stroke at the top is clipped at the canvas edge, so some drawn ink is lost (0002.0, 0006.0).

Claims:

- "Window dragging is triggered instead of drawing near the top of the image." [When trying to markup an image near the top of the window, the window is dragged instead.]: confirmed - The window moves between frames while the pen is at the top edge, and the strokes are truncated. The mouse button is never visible, so the drag is inferred from the window motion.
- "It is more noticeable on portrait images." [may be more noticeable ... on portrait-oriented images]: not shown - Only a portrait image is shown, so there is no landscape comparison.
- "The version is 6.0.0-beta.3 on macOS 13.1 beta." [Signal Version: 6.0.0-beta.3]: not shown - No version information is visible. The wallpaper is consistent with macOS Ventura.
