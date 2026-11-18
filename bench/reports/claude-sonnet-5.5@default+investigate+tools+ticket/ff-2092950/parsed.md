# real/ff-2092950

_claude-sonnet-5.5@default, 29 s; looked at: frames/moments/p095.jpg, frames/moments/p118.jpg, frames/moments/p112.jpg, frames/moments/p024.jpg_

A screen recording (no audio) of a CSS-shaped "Fancy Range Slider" with a counter tooltip being dragged. The thumb changes appearance between frames (filled disc, dot-in-ring, hollow ring) and is missing for several frames while the tooltip still shows a value. This matches the ticket's flicker, but the video does not show the reporter's conditions for it (the high-value bias, or the need for the tooltip).

## Range slider thumb flickers or vanishes while dragging with counter tooltip

Class: **intermittent**

Environment: Browser page 'Fancy Range Slider' (CodePen preview, 488×454 recording). Shape dropdown: curve, wave, zig-zag, bell, diagonal, arc, random. Checkbox 'Keep the tooltip straight'. The browser name and version are not visible; the ticket is a Mozilla Bugzilla report, so Firefox is likely but not shown.

Steps:

1. Open the slider page. The shape is 'curve' and the thumb is at 20. The cursor is not tracked in the first second. (00:00.0; p002)
2. Press on the thumb and drag it along the curve. Value and thumb style change while dragging. (00:02.2; p001, p003)
3. Open the Shape dropdown and choose 'wave'. (00:06.3; p016, p017, p018)
4. Drag the thumb across the wave to high values (94, 97, 98, 100). The tooltip flashes through values. At 9.6–9.7 s the thumb shows as a dot-in-ring, then as a hollow ring. (00:08.4; p020, p021, p024, p028, p030, p033)
5. Repeat dragging on other shapes (zig-zag, bell, diagonal, arc). Each drag changes the thumb style from frame to frame. (00:13.3; p045, p046, p069, p070, p087, p089)
6. On the last shape, 'arc' (the dropdown shows 'arc' by 28.9 s), drag to the right end (88, 89, 97). At 28.3–28.6 s the tooltip jumps 72→57 and the thumb is a filled disc for about two frames. It then disappears while the curve is still drawn. (00:26.7; p103, p104, p108, p109, p110, p112)

Expected (implied): The thumb stays visible with a stable appearance for the whole drag, with the tooltip following it.

Actual: While the thumb is dragged with the tooltip shown, it changes style between consecutive frames (filled disc, dot-in-ring, hollow ring). It also drops out for a few frames (moment p112), leaving only the curve and tooltip. No error is shown.

Key events: p024, p112, p001, p103

Missed by the author:

- The 'FLICKER' events at the top of the page (p063, p095, p118, p139) are the shape dropdown and cursor changing. They are not the thumb, so they are not evidence of the bug.
- The thumb vanishes while the tooltip remains and moves (p112, 28.4–28.6 s).

Claims:

- "Dragging the thumb makes it flicker" [ticket]: confirmed - Frames in moments p024 and p112 show the thumb style changing within 0.1 s and the thumb vanishing for several frames.
- "The flicker happens mostly on the right side (high values)" [ticket]: not shown - The moments checked (p024, p112) are at high values, but the changing thumb style also appears at low and mid values. The video has no comparison that shows a right-side bias.
- "The output (tooltip with counter) must be present for the flicker to occur" [ticket]: not shown - The tooltip is visible throughout; no variant without it is recorded.
- "The simplified CodePen demo reproduces the issue" [ticket]: not shown - The video shows only one page, 'Fancy Range Slider', which looks like the full demo. The URL and browser are not visible.
