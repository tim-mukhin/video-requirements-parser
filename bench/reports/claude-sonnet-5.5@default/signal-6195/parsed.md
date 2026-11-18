# real/signal-6195

_claude-sonnet-5.5@default, 24 s; looked at: frames/000002.jpg, frames/000141.jpg, frames/000236.jpg, frames/000273.jpg_

A silent video (no speech) of a drawing or markup editor with a blank white canvas, Discard/Save buttons and a colour slider with Done. The user draws green strokes near the top edge of the canvas. Meanwhile the editor window shifts down and sideways until its bottom toolbar, including Save and Discard, is pushed off the bottom of the screen. The strokes are also clipped at the canvas top edge. The intent of the video is not stated, so the cause is uncertain.

## Editor window drifts down off-screen while drawing, hiding the Save/Discard toolbar; strokes are clipped at the canvas top

Class: **wrong-data**

Environment: macOS (Ventura-style wallpaper). A small dark image-markup/drawing editor window with traffic-light buttons, a white canvas, a colour slider, pen/size/Done controls, a bottom toolbar (Discard, pen, Aa, sticker, crop, undo, redo, Save). The app name is not visible. The cursor is followed through the whole video, but keys are not seen.

Steps:

1. The editor is open on a blank canvas with the green pen selected. It sits at the top-left of the screen with its toolbar fully visible (the trigger that opened it is not visible). (00:00.0; p001)
2. Click and drag with the pen on the canvas near its top edge. A green 'N'-like stroke appears. The window has already moved down and right by about 50 px (the first stroke is p001 and p004). (00:00.5; p001, p004, p006)
3. Keep drawing short strokes near the top. A further stroke appears at 00:04.6 (p020) and a hand-cursor click at 00:08.6 (p042) lands at the right edge of the canvas. The window keeps shifting down and left between frames 000141 and 000236. The Discard/Save/tool row gets cut off at the bottom of the screen and the strokes are cut off at the canvas top. (00:04.6; p020, p021, p026, p035, p036, p042)

Expected (implied): The editor window stays in place and the strokes are drawn completely on the canvas. The bottom toolbar (Save, Discard, undo) stays visible and reachable.

Actual: The editor window moves down on screen during drawing, so the bottom toolbar (Discard, Save, tools) is pushed off the screen by the end of the video. The strokes touch or run past the canvas top edge and are partly clipped. No error is shown. At 9.6 s the Save button is mostly out of sight.

Key events: p006, p021, p026, p035, p036, p042

Missed by the author:

- The window position changes between frames 000002, 000141 and 000236 (top-left offset from about 0 to about 85 px). By frame 000236 the bottom toolbar is cut off at the screen bottom (p035-p040: many icons in the toolbar change or vanish).
- Strokes drawn at the very top of the canvas are cut by the canvas edge (the 'N' is clipped at the top in frames 000236 and 000273).
