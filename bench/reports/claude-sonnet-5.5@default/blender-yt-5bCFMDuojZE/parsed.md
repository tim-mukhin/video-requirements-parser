# real/blender-yt-5bCFMDuojZE

_claude-sonnet-5.5@default, 38 s; looked at: nothing_

In Blender's Geometry Nodes editor the UI lags badly when the node tree is large: box select, click-select and link drags respond late. The author's counter shows lag at 47,990 and 15,998 total nodes, and none at 8,000. He says the lag is not caused by node evaluation, because the evaluation timing on screen is under 1 ms. This is an editor/UI performance problem that scales with node count.

## Node editor UI lags on box select, click and link drag in a Geometry Nodes tree with many nodes

Class: **stuck**

Environment: Blender (title bar 'bug 7.blend'), Geometry Nodes editor with a Node Counter overlay, a spreadsheet and a 3D viewport. Auto-offset message is shown while dragging. Node Wrangler is enabled. No accounts or organizations are visible.

Steps:

1. Open the .blend file with a Geometry Nodes tree of about 48,000 nodes. The Node Counter reads 'Total Nodes: 47990', and about 1000 nodes are connected to the output. (00:11.6; p009, u001, u002)
2. Click and drag a box select in the node editor. The selection rectangle visibly trails the cursor. (00:26.1; p239, u003, u004)
3. Drag-move the selected nodes. Auto-offset readouts jump in large steps (Dx 34 to 633 to 1131), so the movement is choppy. (00:30.9; p250, p252, p255, u006, u007)
4. Click a node. The author says there is a long delay before the click takes effect. (00:43.9; p262, u010, u011)
5. Delete nodes so the counter drops to 15,998. Box select and node drag still lag. (01:06.1; p289, u017, u018, p296)
6. Delete more nodes so the counter drops to 8,000. The author says the delay is gone. (01:18.4; p348, u021)
7. Undo back to 15,998 nodes. The delay returns. (01:35.2; p416, u023, u024)
8. Add nodes step by step (23,996, 31,994, 39,992, 47,990, 55,988). The author says the lag gets worse. (01:58.0; p518, p538, p557, p572, p594, u028, u029)
9. At about 55,988 nodes, move the mouse after a selection. The author says the nodes stay 'still selected' and the UI is 'not snappy'. (02:14.5; p595, u037, u040)
10. Click and drag a node link. There is a delay between the click and the drag starting. (02:41.0; p641, p656, u044)
11. The author points at the evaluation time, under 1 ms (about 0.96 ms). He concludes the output time is not what is slow. (02:50.4; p756, u045, u046)

Expected (implied): Box select, click-select and link dragging in the node editor respond immediately, without visible lag, however large the tree is.

Actual: The editor responds with a noticeable delay once the tree has roughly 15,000 or more nodes. The delay grows with node count. At about 48,000 to 56,000 nodes it is described as unusable: the box select lags behind the cursor, nodes stay selected after the mouse moves, and drag starts late. At 8,000 nodes the author reports no delay.

Key events: p009, p239, p252, p255, p289, p348, p416, p594, p641, p756, u021, u046, u047, u054

Missed by the author:

- The 'went back by itself' cross-checks (Cancel to Select, p283/p326/p462) are only the header/status bar reverting after a drag finishes. They are not a defect.
- Several nodes flash in a flicker of unreadable text on the node canvas during redraws (for example p023-p044, p163-p186, p808-p829), which suggests the editor redrew the whole large tree.
- A screenshot-like jump at 02:48.4 shows the spreadsheet switching from 0 rows to 8 rows (p666), then back to 0 (p701): the spreadsheet updates while the editor is busy.

Claims:

- "The bug was reported, but other people cannot see what the author sees; at 14,000 or 15,000 nodes the delay is noticeable but others cannot perceive it, so he exaggerated the count to 48,000." [u001]: not shown - What others see is outside the video. The counter does show 47,990 nodes at the start.
- "Only 1,000 nodes seem connected; the rest are not connected to any output." [u002]: confirmed - The OCR text near the nodes reads '1000 nodes' and the node counter reads about 48,000 (p009).
- "At about 8,000 nodes the delay is completely gone." [u021]: confirmed - After the counter dropped to 8000 (p348) no lag-like events follow before the undo. The effect is mainly the author's own observation.
- "Other people cannot perceive the delay at around 15,000 nodes." [u019]: not shown - This is a claim about other people.
- "Node evaluation is not the cause of the delay." [u045]: confirmed - The overlay reads about 0.96 ms (p756, p980), so evaluation is not slow. The OCR is noisy.
- "The 1,000 nodes are copies; the base node group is only 10 real nodes." [u054]: not shown - The node group label reads '1000 nodes' and later '10 nodes'/'100 nodes' after edits; the instance count is not verified.
