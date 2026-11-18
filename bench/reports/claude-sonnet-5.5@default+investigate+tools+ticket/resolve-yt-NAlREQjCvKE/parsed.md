# real/resolve-yt-NAlREQjCvKE

_claude-sonnet-5.5@default, 25 s; looked at: frames/0060.0.jpg, frames/0092.0.jpg_

In Fusion, an Outer sphere textured through a ChromaKeyer hides the Inner sphere even where the key made the texture transparent. The same map as a PNG with a real alpha channel lets the Inner sphere show through. Keyed transparency is not honoured in the 3D scene, so users cannot rely on a chroma key to cut out a texture.

## Fusion 3D: Outer sphere textured via ChromaKeyer still hides the Inner sphere through keyed-transparent areas

Class: **wrong-data**

Environment: DaVinci Resolve Studio 19.1 build 12 (spoken u001 and splash screen p011), Windows, project 'VTR-Logo', Fusion page. Nodes: ImageNoAlpha -> ChromaKeyer1, ImageWithAlpha, Outer and Inner (Shape 3D spheres), Merge3D1, MediaOut1. The ticket has a title and link only, with no version or setup.

Steps:

1. Fusion page: a blue Inner sphere sits inside a slightly larger Outer sphere (author's description, u002/u003). Merge3D1 is selected. (00:24.0; p047, u003)
2. Connect ImageWithAlpha (a PNG with a real alpha channel) to Outer's material. The map shows and the Inner sphere is visible through the transparent areas (spoken, u005; the later contrast frames show the globe without the blue sphere). (00:31.9; p078, p079, u005)
3. Select ImageNoAlpha (the same map without alpha) and ChromaKeyer1, the keyer whose output is to feed Outer, and remove the background (u006/u007). (00:48.0; p095, p104, u007)
4. Drag the ChromaKeyer1 output onto Outer's material input. The viewer shows the flag globe and the Inner sphere is gone, even though the keyed areas are see-through (spoken u008). (00:55.2; p124, p131, p135, u008)
5. Select Inner and drag its X translation out of the Outer sphere (X ~0.59 in frame 0092). Only the part outside the Outer sphere appears, with a hard edge where it crosses the Outer volume. (01:23.8; p196, p211, p217, u011)

Expected (speech): Areas keyed transparent by ChromaKeyer1 should behave like the PNG's own alpha: invisible, with the Inner sphere visible through them.

Actual: With ChromaKeyer1 feeding Outer, the Inner sphere is hidden inside the globe. When moved out, it is cut off where it crosses the Outer sphere (frame direct/frames/0092.0.jpg, frame 0060.0 for the hidden state). With ImageWithAlpha feeding Outer, the Inner sphere shows through. No error is shown.

Key events: p079, p124, p135, p196, u008, u011

Missed by the author:

- The clipped edge of the moved Inner sphere shows that the keyed pixels still occlude 3D geometry (or are not fully zero alpha). This is my reading, not stated in the video (frame 0092.0).
- The author never checked ChromaKeyer1's output alpha, so the video does not show whether it is exactly 0 in the keyed areas.

Claims:

- "With an alpha PNG on the outer sphere the inner sphere is visible through the alpha channel." [u005]: not shown - Spoken at 00:33; I did not open a frame of that state, so the contrast rests on the author's words.
- "With the chroma-keyed image the inner sphere is hidden and gone." [u008]: confirmed - Frame 0060.0 shows only the flag globe with no blue sphere, with ChromaKeyer1 wired to Outer.
- "Dragging the inner sphere out makes it visible." [u011]: confirmed - Frame 0092.0 shows the blue sphere at X 0.59, cut off by the Outer sphere where they overlap.
- "This behaviour is not expected." [u010]: not shown - An opinion; the screen shows no documentation or error.
