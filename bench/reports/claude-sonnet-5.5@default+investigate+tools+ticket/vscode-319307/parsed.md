# real/vscode-319307

_claude-sonnet-5.5@default, 24 s; looked at: frames/0003.0.jpg, frames/0004.5.jpg, frames/0008.0.jpg_

In the Sessions window, two chat views sit side by side. The user drags the already-open 'Farewell message' view. The drop-target highlight covers only a half of a view (the left half of the sibling, or the right half of its own pane). On release the two views swap and each fills a full half-width slot. The preview does not match the result, which is confusing.

## Dragging an already-open chat view shows a half-pane drop highlight, but the drop just swaps the views

Class: **wrong-data**

Environment: VS Code Sessions window on macOS, workspace vscode-distro, branch setting-important. Two chat editors, 'Farewell message' (left) and 'User greeting' (right), with the Changes panel on the right and the Sessions list on the left. The video is 8.5 s, has no audio, and the cursor is followed through about 62% of it.

Steps:

1. Start with 'Farewell message' on the left and 'User greeting' on the right, both open. The cursor hovers over the 'Farewell message' tab. (00:00.9; p001)
2. Press on the 'Farewell message' tab and start dragging it. A drag chip appears under the cursor, with a flickering drop overlay on its own pane. (00:02.0; p007, p008, p010)
3. Drag over the sibling 'User greeting' view. The highlight covers only its left half, not the whole pane (frame 0003.0). (00:03.3; p015, p016)
4. Drag back over the left view. The highlight now covers only the right half of that view (frame 0004.5). (00:04.5; p020, p021, p026)
5. Repeat the drag and drop. On the last release the views are swapped, with 'User greeting' on the left and 'Farewell message' on the right. Each takes a full half-width pane, with no half-pane split (frame 0008.0). (00:07.6; p032, p038, p050, p051)

Expected (implied): The highlighted drop region should match the layout produced on release. Either the highlight covers the full target pane, or the drop creates a split in the highlighted half.

Actual: The highlight covers about half of the dragged view's own pane or half of the sibling. Releasing swaps the two views, and each fills a full half-width slot. The preview misrepresents the result.

Key events: p015, p020, p026, p038, p050, p051

Missed by the author:

- The drag was repeated several times (about 2 to 7 s), and each time the highlight shifted between halves of different panes (p015, p020, p026, p033).
- The final result is a swap of the two views' order, which the ticket does not mention (p050, p051).
- Between 7.3 and 8.5 s the cursor is not followed, so the final release is not directly visible. It is inferred from the layout change (p038, p039).

Claims:

- "Dragging the view highlights half of its own view and half of the sibling view." [ticket]: confirmed - At 3.0 s the highlight covers the left half of the sibling pane. At 4.5 s it covers the right half of the dragged view's own pane. No frame shows one highlight spanning both panes.
- "On release the view takes up a full space, not half a space." [ticket]: confirmed - After the drop (0008.0) both views are equal full slots, swapped, with no half-pane split.
