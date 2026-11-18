# real/kde-528799

_claude-sonnet-5.5@default, 28 s; looked at: frames/000340.jpg_

In Krita on an Android tablet, the user drags the left-edge handle of a vector shape on the 'Mask' layer with the shape-selection tool. The shape's geometry jumps in large, uneven steps and the shape ends up slightly skewed. A snap to a target is not visible, because there is no cursor and no snap settings are shown. The video is weak evidence for the ticket's "snaps further each time" claim.

## Krita Android: dragging a vector shape's edge handle with the shape-selection tool gives jumpy, imprecise resizing

Class: **wrong-data**

Environment: Krita on an Android tablet (clock 5:40), recorded with XRecorder. Documents: getaroom.kra (120.9 MiB) and an unsaved 36.2 MiB document. The 'Mask' vector layer is selected and the leftmost toolbox tool is active (shape selection). Tool Options show a Geometry panel with X/Y and width/height fields. Zoom goes 54.8% → 82.5% → 90.4%. Snap settings are never opened. The Krita and Android versions are not visible.

Steps:

1. Krita opens with the comic page. The Mask vector shape is selected with the leftmost (shape selection) tool, and its Geometry fields read 221.17 / 182.45 pt. The click that chose the tool is not visible. (00:05.2; p022)
2. Zoom the canvas (pinch inferred, not seen). The overlay reads 'Zoom: 90.4 %'. The shape is unchanged. (00:08.8; p025, p026)
3. Drag the shape's left-edge handle (the touch is not drawn). The geometry becomes 248.64 / 127.48, with 'Updating... 0%' shown. (00:10.6; p032, p034)
4. Repeat the drag several times. The values go 238.31/148.16 (11.9 s), 223.23/178.34 (13.3 s), 232.26/160.26 (14.4 s), 215.67/193.46 → 183.46/257.90 (15.9–16.3 s), 209.87/205.07 (18.2 s), 178.41/268.02 (20.9 s). The shape overlaps the left panel and its top edge ends up slanted (frame 000340). (00:11.9; p044, p055, p062, p068, p071, p079, p088)
5. A later change (22.6 s) puts the values at 223.18/178.43, close to the starting 221.17/182.45. The jump is not explained on screen. The recording is then stopped. (00:22.6; p098, p106)

Expected (speech): The edge follows the finger precisely, with no snapping, when the snap options are off.

Actual: Each drag gives a large, non-monotonic change in geometry. The values do not follow a steady progression and return to near the start. Krita shows 'Updating... 0–33%' during edits, and the shape ends up skewed and overlapping the neighbouring panel. The video does not show where the finger is, so it cannot be seen whether the edge snaps or just lags.

Key events: p034, p044, p055, p068, p071, p079, p088, p098

Missed by the author:

- The status bar shows 'Updating... 0–33%' during the edits (p032, p045, p069, p077), so redraw lag may play a part.
- The shape ends up skewed with a slanted top edge, which is not a pure edge-handle resize (frame 000340).
- The tooltip 'Press CTRL...om center.' flashes while the handle is dragged (p066, p078).
- The zoom was changed before the drags (p025).

Claims:

- "The leftmost arrow tool is used (reporter thinks it is freehand select)." [ticket]: confirmed - The leftmost toolbox tool is active and the shape handles are shown (frame 000340). It is the shape-selection tool, not freehand selection.
- "All snap-to settings are off." [ticket]: not shown - No snap settings or menu are opened in the video.
- "The more you stretch it, the further away it snaps." [ticket]: not shown - The values swing back and forth and end near the start. No growing offset is visible, and no finger or cursor is visible.
- "Android, latest Qt." [ticket]: not shown - The device looks like an Android tablet, but no version is visible.
