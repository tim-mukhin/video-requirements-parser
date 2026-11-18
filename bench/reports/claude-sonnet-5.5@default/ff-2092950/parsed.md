# real/ff-2092950

_claude-sonnet-5.5@default, 21 s; looked at: frames/000003.jpg, frames/000071.jpg, frames/000299.jpg, frames/001132.jpg_

A silent screen recording of a 'Fancy Range Slider' demo with a shape dropdown (curve, wave, zig-zag, bell, diagonal, arc, random). The author drags the thumb along each curve. At the maximum the value tooltip is cut off by the right edge of the viewport, so it reads '100' only partly. The video has no audio, so the intended problem is not stated.

## Slider value tooltip is clipped at the right edge when the thumb is at the maximum (100)

Class: **wrong-data**

Environment: Browser page 'Fancy Range Slider' (a CodePen-style demo, 488x454 capture). It has a 'Select The Shape' dropdown and a 'Keep the tooltip straight' checkbox, which stays unchecked. A small 'CodePen Preview' button appears from 00:07 onward. No accounts or organizations are visible.

Steps:

1. Page loads with shape 'curve' and the thumb at 20, with the tooltip fully visible. (00:00.0; s001)
2. Drag the thumb to the far left, where the value is 0 (the thumb becomes a filled dot), then to the far right, where the value is 100. The click and drag positions are inferred, not seen as keys. (00:02.3; p002, p004, p005, p006)
3. Open the shape dropdown and pick 'wave'. (00:06.3; p011, p012, p013)
4. Drag the thumb to the right end of the wave. The tooltip showing '100' is cut off by the right edge of the viewport, and only part of it is visible. (00:09.3; p023, p024, p026, p027)
5. Repeat on the other shapes (zig-zag, bell, diagonal, arc, random). The value tooltip changes quickly as the thumb moves. (00:11.8; p034, p055, p057, p073, p086, p123)

Expected (implied): The value tooltip stays fully visible at every thumb position, including the minimum and maximum, for example by shifting or clamping inside the viewport.

Actual: At value 100 on the 'wave' shape the tooltip extends past the right edge of the viewport and is cut off (frame 000299). At 0 on 'curve' the tooltip sits at the left edge (frame 000071). Because there is no audio, the recording does not say whether the clipping is the problem the author meant to show.

Key events: p027, p023, p024, p026, p002

Missed by the author:

- There is no speech, so nothing the author noticed is known. A 'CodePen Preview' button overlay appears at the top right of the slider from 00:07 (p014).
- Tooltip values flash for under 1 s while dragging (p018, p022, p048, p050, p088, p092, p093). The value can jump, for example 94→97→98→100 (p018, p022, p025, p027) and 12→13→1 (p060, p062).
- On the 'random' shape the final screen shows value 17 (frame 001132). The tooltip text is slightly rotated, following the curve.
