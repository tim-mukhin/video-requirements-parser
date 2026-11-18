# real/signal-6195

_claude-sonnet-5.5@default, 21 s; looked at: frames/0000.0.jpg, frames/0006.0.jpg_

In Signal Desktop's image editor on macOS, pressing and dragging with the pen near the top of the image moves the whole window instead of drawing a stroke. The video shows the window drifting down and right while only fragments of ink appear, so the top of the image is hard to annotate. This matches the ticket.

## Image markup near top of the canvas drags the Signal window instead of drawing (macOS)

Class: **wrong-data**

Environment: Signal Desktop image editor (pen tool, green, Done/Discard/Save toolbar), portrait white image, macOS with a Ventura-style wallpaper, 2006×2304 recording. The version (6.0.0-beta.3) and OS build (13.1 beta) are only in the ticket; they are not visible in the video.

Steps:

1. The editor is open with the pen tool and green selected. The window sits flush at the screen's top-left (frame 0000.0). The cursor is a crosshair near the top of the canvas. (00:00.0; s001)
2. Press and drag with the pen near the top of the image. Content under the cursor moves with it, and the window shifts down and right instead of ink appearing. Parser drags, from 0.4 s: 24 px right and 22 px up over 300 ms. At 1.7 s content moved 24 px down. At 1.8 s the toolbar area moved 10 px left and 7 px down. (00:00.4; p001, p010, p011)
3. Repeat: press and drag near the top edge. Each time the whole area follows the cursor and the window has moved to a new place. At 3.8 s the area moved 45 px right and 20 px down. At 6.6 s it moved 29 px right and 48 px down. At 9.4 s it moved 37 px right and 33 px down. At 6.0 s (frame 0006.0) the window is about 85 px lower and shifted right, and only a small green zigzag and a fragment of a second stroke are drawn at the clipped top edge. (00:03.8; p020, p038, p041, p053)

Expected (implied): Pressing and dragging on the canvas near the top draws a pen stroke and the window stays put. Alternatively the canvas does not extend into the window-drag region, as the ticket says.

Actual: Drags that start near the top of the canvas move the Signal window instead of drawing. The window drifts from the top-left to a lower, right-shifted position over the 9.6 s. Strokes are cut short or clipped at the canvas top, so only fragments of ink appear.

Key events: p001, p010, p011, p020, p038, p041, p053

Missed by the author:

- The recording has no audio or narration.
- The mouse press is not seen directly. The parser's drags and clicks are inferred from the cursor and content moving (p001, p020, p053).
- The window ends up in a clearly different place than it started, and the strokes that were drawn are clipped at the canvas top edge (frame 0006.0).

Claims:

- "Window dragging is triggered instead of drawing near the top of the image." [ticket]: confirmed - Frame 0000.0 shows the window at the top-left. Frame 0006.0 shows it moved down and right with partial ink. The parser reports whole-area drags at 3.8, 6.6, 7.3 and 9.4 s.
- "It is more noticeable on portrait-oriented images." [ticket]: not shown - Only a portrait image is shown, so there is no landscape comparison.
- "Signal 6.0.0-beta.3 on macOS 13.1 beta." [ticket]: not shown - No version information is visible. The wallpaper is consistent with Ventura.
- "Window dragging is 'often' triggered." [ticket]: not shown - The video has a single continuous session, so the frequency cannot be measured. Every drag checked near the top moved the window.
