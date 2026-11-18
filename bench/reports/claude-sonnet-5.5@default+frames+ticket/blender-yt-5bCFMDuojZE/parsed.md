# real/blender-yt-5bCFMDuojZE

_claude-sonnet-5.5@default, 49 s; looked at: frames/0000.0.jpg, frames/0020.0.jpg, frames/0050.0.jpg, frames/0090.0.jpg, frames/0130.0.jpg, frames/0180.0.jpg, frames/0234.0.jpg, frames/0070.0.jpg, frames/0080.0.jpg, frames/0100.0.jpg, frames/0110.0.jpg, frames/0150.0.jpg, frames/0210.0.jpg, frames/0030.0.jpg, frames/0060.0.jpg, frames/0120.0.jpg, frames/0170.0.jpg, frames/0195.0.jpg, frames/0220.0.jpg, frames/0140.0.jpg, frames/0126.0.jpg_

A silent screen recording of Blender 3.4.1 in the Geometry Nodes workspace. It shows a very large node tree (Node Counter 47990–55998) that the user selects, drags and deletes in pieces, then restores. No error or visibly failing action appears, and the ticket does not name the bug, so the actual defect cannot be determined from the frames.

## Large geometry node tree (~48–56k nodes by Node Counter): defect not identifiable from the video

Class: **stuck**

Environment: Blender 3.4.1 (version at bottom right), file bug_7.blend, Geometry Nodes workspace. Object 'Cube' with a Geometry Nodes modifier. The editor has a Node Counter add-on panel, with Node Wrangler also in the sidebar. Spreadsheet is at top left, 3D viewport at top right, node editor at the bottom.

Steps:

1. The node tree is open in the node editor. The Node Counter reads 'Total Nodes: 47990'. The tree is a trunk of about 11 group nodes with 5 parallel branches and a separate output node. The spreadsheet is empty (Rows: 0). (00:00.0; 0000.0)
2. The user pans the view and moves nodes around. The output node is moved at 30 s (inferred drag). At 60 s a box-select rectangle is drawn around the lower branches. (00:30.0; 0020.0, 0030.0, 0050.0, 0060.0)
3. Nodes are removed or detached and moved. The counter drops to 15998 with a single chain, then to 8000 with only a short chain left. The status bar shows 'Auto-offset set to right' during the drags. (01:10.0; 0070.0, 0080.0, 0090.0)
4. Branches are added back (inferred paste or undo). The counter goes 15998 → 31994 → 39992 → 47990 → 55988/55998. The newly added rows show a red/orange outline, which I take to be selection. (01:50.0; 0110.0, 0126.0, 0130.0, 0140.0, 0150.0, 0170.0)
5. The user zooms in on the group nodes (each labelled '1000 nodes'). A tooltip appears: 'Display number of users of this data (click to make a single-user copy)'. The spreadsheet briefly shows 8 vertices (cube at x≈11–13). The user then enters a group, whose breadcrumb reads '1000 nodes > 100 nodes'. (03:00.0; 0150.0, 0180.0, 0190.0, 0210.0, 0220.0)

Expected (implied): Not stated, because the video has no sound. Implied: the large tree should stay responsive, and the Node Counter total should match the nodes that are present.

Actual: No error, crash or wrong result is visible in the sampled frames. The most likely candidates are slow response with a very large tree, or an inaccurate counter. At 130 s the counter reads 47990 with 6 rows, while 140 s reads 55988 with 7 rows. The counter also reads 55998 at 180 s and 55988 at 190 s for what looks like the same tree, a 10-node difference that may be an inconsistency.

Key events: 0000.0, 0090.0, 0130.0, 0170.0, 0180.0

Missed by the author:

- The ticket does not describe the symptom or give steps.
- The Node Counter total varies by 10 between what look like identical states (55998 at 0180.0 vs 55988 at 0190.0).
- Blender version is 3.4.1 and the file is bug_7.blend (0000.0).

Claims:

- "The author has a 14000+ node humanoid that shows a bug" [Video demonstrating a bug I found with my 14000+ node humanoid.]: not shown - The scene is a Cube with a synthetic tree of '1000 nodes' groups, not a humanoid. The Node Counter reads 8000–56000, not 14000. The video shows no clear failure.
