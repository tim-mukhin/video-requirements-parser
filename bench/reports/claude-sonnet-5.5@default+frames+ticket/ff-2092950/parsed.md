# real/ff-2092950

_claude-sonnet-5.5@default, 29 s; looked at: frames/0000.0.jpg, frames/0005.0.jpg, frames/0010.0.jpg, frames/0015.0.jpg, frames/0020.0.jpg, frames/0025.0.jpg, frames/0030.0.jpg, frames/0035.0.jpg, frames/0005.5.jpg, frames/0006.0.jpg, frames/0006.5.jpg, frames/0009.0.jpg, frames/0010.5.jpg, frames/0011.0.jpg_

A CSS-shaped range slider with a counter tooltip is dragged across several shapes. The thumb keeps changing look between frames: a hollow ring, a filled disc, a dot-in-ring, and at 10.5 s no thumb at all while the tooltip still shows 79. This matches the reported flicker, but the video has no shapes or tooltip-less cases to confirm the ticket's other claims.

## Range slider thumb flickers/disappears while dragging with counter tooltip

Class: **intermittent**

Environment: Browser page 'Fancy Range Slider' (CodePen preview, a 'CodePen Preview' button is visible). Shape dropdown (curve, wave, zig-zag, bell, diagonal, arc, random) and a 'Keep the tooltip straight' checkbox. Browser name and version are not visible; the ticket is a Mozilla Bugzilla report, so Firefox is likely but not shown.

Steps:

1. Open the slider page with shape 'curve'. The thumb is a hollow ring at value 20. (00:00.0; 0000.0)
2. Drag the thumb (inferred from the moving cursor and changing value). The thumb is now a filled disc at 5, then at 31. (00:05.0; 0005.0, 0005.5)
3. The thumb returns to a hollow ring at 57. The user opens the shape dropdown and picks 'wave' (inferred click). (00:06.0; 0006.0, 0006.5, 0009.0)
4. Keep dragging toward high values. At 79 (10.5 s) the thumb is not drawn at all while the tooltip is visible. At 100 (10 s) it shows as a small dot, and it is a filled disc at 12 (11 s). (00:10.0; 0010.0, 0010.5, 0011.0)
5. Keep dragging on other shapes (zig-zag, bell with straight tooltip, diagonal, arc, random). The thumb alternates between ring and filled disc from frame to frame. (00:15.0; 0015.0, 0020.0, 0025.0, 0030.0, 0035.0)

Expected (implied): The thumb keeps a stable, consistent appearance and is always visible while dragged.

Actual: While dragging, the thumb's appearance changes between frames (hollow ring, filled disc, dot-in-ring) and it is missing at 10.5 s while the tooltip is still shown. The ticket says this happens mostly at high values; the video also shows it at low and mid values.

Key events: 0005.0, 0006.0, 0010.0, 0010.5

Missed by the author:

- The thumb is absent while the tooltip still shows 79 (0010.5).
- The effect appears on every shape and with 'Keep the tooltip straight' both on and off (0020.0, 0025.0).

Claims:

- "Dragging the thumb makes it flicker" [When you drag the thumb, you will notice some flickering]: confirmed - The thumb style changes between neighbouring frames and disappears at 10.5 s.
- "The flicker happens mostly on the right side (high values)" [happens mostly on the right side (high values)]: not shown - The thumb is missing at 79, but the odd thumb styles also show at 5, 12, 20 and 31, so the video does not show a right-side bias.
- "The flicker needs the output tooltip with the counter value" [The output (the tooltip) needs to be present with the counter value to activate the flicker]: not shown - The tooltip is visible in every frame; the reduced case without it is not recorded.
