# real/blender-yt-5bCFMDuojZE

_claude-sonnet-5.5@default, 27 s; looked at: nothing_

In Blender 3.4.1 Geometry Nodes, the node editor lags badly on a very large node tree. Box select, drags and clicks respond late, and selection stays visible while the mouse moves. The author says the lag grows with node count and disappears at about 8,000 nodes. The video shows the lag only through the author's speech and the counter. The ticket does not describe the symptom.

## Node editor UI lags on large Geometry Nodes trees (box select, drag, click) and the lag scales with node count

Class: **intermittent**

Environment: Blender 3.4.1, file bug_7.blend, Geometry Nodes workspace. Node Counter add-on and Node Wrangler in the sidebar. Spreadsheet top left, 3D viewport top right, node editor at the bottom. Synthetic tree of '1000 nodes' group nodes (47,990 to 55,988 by Node Counter), not a humanoid. Only about 1,000 nodes are connected to an output.

Steps:

1. Open the tree. Node Counter reads 'Total Nodes: 47990'. About 1,000 nodes are connected to the output and the rest are unconnected copies. (00:11.6; p010, u001, u002)
2. Box-select and drag the nodes. The author reports the view lags behind the cursor and clicks are delayed (frames not checked for the lag itself). (00:23.6; u003, u004, u005, u006, u011)
3. Delete part of the tree. The counter drops 47990 → 15998. The author says a delay remains, but other people cannot perceive it. (01:06.1; p262, u017, u019)
4. Delete more. The counter drops 15998 → 8000. The author says the delay is gone and box select is fine. (01:18.4; p326, u020, u021)
5. Undo to restore the nodes (counter 8000 → 15998), then paste more branches back (23996, 31994, 39992, 47990, 55988). The author says the lag returns and worsens. (01:35.2; p396, p502, p522, p541, p556, p578, u023, u028, u029)
6. Move the mouse with nodes selected. The author reports the selection state lags behind the mouse. (02:16.9; u036, u037, u040)
7. Click and drag Group Output. The author reports a delay between click and drag. (02:52.1; p855, u044)

Expected (implied): The node editor should stay responsive (box select, click and drag without noticeable delay) on a large tree, especially when most nodes are not connected to the output.

Actual: By the author's account, interaction in the node editor is slow with tens of thousands of nodes. It is workable at about 14,000 to 15,000 and fine at about 8,000. The screen shows no error or crash. The lag is not measured in the timeline; it rests on speech and on the counter values.

Key events: p010, p262, p326, p396, p578, u007, u019, u021, u044, u045

Missed by the author:

- Cross-checks list 'Cancel' reverting to 'Select' and 'Scroller Activate' (p273, p320, p461) with no click seen. These are modal operator states in the header while dragging and are not an error.
- The counter reaches 55988 after pasting, above the 47990 the author set as 48,000 (p578).
- The ticket's Twitch link and the 14000+ humanoid are not visible in the video.

Claims:

- "There is a lag even at about 14,000 nodes." [u012]: not shown - The counter shows 15,998 at 01:06, but the lag is not measurable from the timeline.
- "At about 8,000 nodes the delay is gone completely." [u021]: not shown - The counter reads 8000 at 01:18 (p326), but no latency data is visible.
- "Only about 1,000 nodes are connected to an output." [u002]: not shown - The tree is shown, but connectivity cannot be verified from OCR.
- "The lag has nothing to do with evaluation time, which is under a millisecond." [u045]: not shown - No evaluation timing is on screen.
- "The ticket says the author has a 14000+ node humanoid." [u012]: refuted - The scene is a synthetic tree of '1000 nodes' groups. The counter reads 8,000 to 56,000.
- "Other people cannot see the lag at 15,000 nodes." [u019]: not shown - This is a claim about other people.
