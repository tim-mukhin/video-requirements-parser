# real/kde-528799

_claude-sonnet-5.5@default, 28 s; looked at: frames/0000.0.jpg, frames/0003.0.jpg, frames/0006.0.jpg, frames/0009.0.jpg, frames/0012.0.jpg, frames/0015.0.jpg, frames/0018.0.jpg, frames/0021.0.jpg, frames/0025.0.jpg_

On Android, Krita is open with a vector 'Mask' layer containing a panel rectangle. The user drags the left edge handle of that shape with the selection (arrow) tool. The video does not clearly show the reported snapping, and it does not show the snapping settings.

## Vector shape resized with the arrow (shape selection) tool reportedly snaps instead of resizing precisely (not clearly shown)

Class: **wrong-data**

Environment: Krita on Android tablet, recorded with XRecorder. Documents: getaroom.kra and an unsaved 36.2 MiB document. Layer 'Mask' (vector) is selected. The first tool-bar tool (arrow) is active and the Tool Options panel shows Geometry X/Y/W/H. Zoom changes from 54.8% to 90.4%.

Steps:

1. A vector shape (the top-right comic panel) is selected on the 'Mask' vector layer with the arrow tool. Handles are visible and Tool Options show X 221.17, width 182.45. (00:03.0; 0003.0)
2. The user zooms the canvas, shown by a 'Zoom: 90.4%' overlay. This is inferred to be a pinch gesture. The shape is unchanged. (00:06.0; 0006.0)
3. The user drags the left-edge handle to the right (inferred). The shape's left edge is now at X 238.31 and width 148.16, and the status bar shows 'Updating... 33%'. (00:09.0; 0009.0)
4. The user drags the left edge again. X is 232.26 and width 160.26. (00:12.0; 0012.0)
5. The user drags the left edge left. The shape now overlaps the left panel (X 209.87, width 205.07), with 'Updating... 33%' shown again. (00:15.0; 0015.0)
6. The left edge is dragged further left to X 178.41, width 268.02, and it covers the left panel's top border. (00:18.0; 0018.0)
7. The edge is back at X 223.18, width 178.43, near where it started. The user then opens the 'Stop sharing screen?' dialog to end the recording. (00:21.0; 0021.0, 0025.0)

Expected (implied): The shape's edge follows the pointer exactly and does not jump to snap positions when snapping is turned off.

Actual: The left edge ends up at different positions that do not change steadily across drags (X 221 → 238 → 232 → 210 → 178 → 223). The video shows no clear jump to a snap target and does not show the pointer position, so it is not possible to tell whether the edge follows the finger or snaps.

Key events: 0009.0, 0012.0, 0015.0, 0018.0, 0021.0

Missed by the author:

- The status bar shows 'Updating... 33%' during edits (0009.0, 0015.0), so the canvas may be lagging. The shape's left edge may be trailing the finger, which could look like snapping (inferred).
- The ticket does not say the document is a comic page with a mask vector layer, or that the zoom was changed before the drags (0006.0).
- The shape at 0015.0 and 0018.0 overlaps the neighbouring panel, which suggests it is not snapping to the neighbour's edge.

Claims:

- "The tool used is the leftmost arrow tool." [Click on arrow (freehand select i think) tool on the furthest left]: confirmed - The leftmost toolbar tool is highlighted and the shape handles show. It is the shape selection/edit tool, not freehand selection. The tool selection click itself is not shown.
- "All snap settings are off." [even if all my snap to... Settings are off]: not shown - No snap settings or menu are opened in the video.
- "The more times it is stretched, the further away it snaps." [The more times you stretch it, the further away it snaps]: not shown - The left edge moves back and forth and ends near its start. There is no clear growing offset, and the pointer is not visible.
