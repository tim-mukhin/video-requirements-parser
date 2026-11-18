# real/resolve-yt-NAlREQjCvKE

_claude-sonnet-5.5@default, 23 s; looked at: nothing_

In DaVinci Resolve Studio 19.1 (build 12), Fusion, an outer sphere is textured with an image whose alpha comes from a Chroma Keyer. The inner sphere behind it stays hidden. With a PNG that already has alpha, the inner sphere shows through. The author calls the keyed result unexpected. The timeline shows only the node edits and the later Z-translate changes, not the rendered viewer result.

## Fusion 3D: outer sphere textured via Chroma Keyer alpha hides the inner sphere; a PNG with native alpha does not

Class: **wrong-data**

Environment: DaVinci Resolve Studio 19.1 build 12, Fusion page. Nodes: ChromaKeyer1, ImageWithAlpha, ImageNoAlpha, Inner and Outer (Shape3D), Merge3D1. Inspector and Viewer windows. No accounts or organizations are shown.

Steps:

1. In the Fusion node graph, select ImageWithAlpha (a PNG with a real alpha). It feeds the Outer sphere's material, and the inner sphere is visible through the outer one. (00:29.8; p052, p079)
2. Select ImageNoAlpha (the same flag map without alpha). (00:48.0; p095, p097)
3. Select ChromaKeyer1, whose Chroma Color ranges are set. (00:51.1; p104, p105)
4. Connect ChromaKeyer1's output to the Outer sphere's material. The link ChromaKeyer1: Output -> Outer: Material is shown. (00:54.3; p123, p125, p160)
5. Select Merge3D1 and look at the result. The author says the inner sphere is now hidden. (00:56.8; p135, p136, p159)
6. Reconnect ImageWithAlpha to the Outer material. The author says the inner sphere is visible again. (01:07.2; p165, p171, p181)
7. Open the Inner sphere's Transform and change Translate Z. The author says the inner sphere becomes visible once it is pulled out of the outer sphere. (01:25.3; p196, p211, p213, p216, p222, p226)

Expected (speech): A texture whose alpha comes from a Chroma Keyer should make the outer sphere transparent in the keyed areas, like a PNG with native alpha, so the inner sphere shows through.

Actual: With the keyed image on the outer sphere, the author says the inner sphere stays hidden. With the native-alpha PNG it is visible. The author only gets it visible by moving the inner sphere out of the outer one, and calls this unexpected. The rendered viewer content is not in the timeline text.

Key events: p123, p135, p160, p165, p171, p216, p222, p226, p241

Missed by the author:

- Memory use rose in the viewer while the Chroma Keyer was connected: '11% - 3585 MB' changed to '11% - 3671 MB' (p123, p133).
- The Translate Z value was changed several times (1.562555, 0.737969, 0.602848, 0.585524, 0.592454) and then reset to 0.0 (p216, p222, p226, p229, p234, p241). The author did not say which Z value made the inner sphere visible or whether it was still hidden at 0.0.

Claims:

- "Inner sphere is hidden when the Chroma Keyer output feeds the outer sphere" [u008]: not shown - The timeline shows the ChromaKeyer1 -> Outer: Material link (p160). The viewer pixels are not described, so the hidden inner sphere was not checked against a frame.
- "Inner sphere is visible when an image with a native alpha PNG is used" [u009]: not shown - The reconnection ImageWithAlpha -> Outer: Material is shown (p181). The viewer content is not described.
- "Dragging the inner sphere out makes it visible" [u011]: not shown - Translate Z values change (p216, p222, p226, p229, p234) and are then reset to 0.0 (p241). The visibility result is not in the text.
- "The version is DaVinci Resolve Studio 19.1 build 12" [u001]: confirmed - The splash text 'VERSION 19.1 BUILD 12' is on screen (p011).
