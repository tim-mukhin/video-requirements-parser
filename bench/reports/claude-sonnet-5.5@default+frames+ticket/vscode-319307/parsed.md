# real/vscode-319307

_claude-sonnet-5.5@default, 22 s; looked at: frames, frames/0000.0.jpg, frames/0002.0.jpg, frames/0003.0.jpg, frames/0004.0.jpg, frames/0005.0.jpg, frames/0006.0.jpg, frames/0008.0.jpg_

In the Sessions window, two chat views sit side by side. The user drags the 'Farewell message' view over the sibling 'User greeting' view. The drop-target highlight covers only a half-width region, but on release the views just swap and each takes a half-width slot. The preview does not match the result, which is confusing.

## Drag preview of an already open chat view highlights a half region but the drop swaps the views

Class: **wrong-data**

Environment: VS Code Sessions window (macOS), workspace vscode-distro, branch setting-important. Two chat views side by side: 'Farewell message' and 'User greeting'. The Changes panel is on the right.

Steps:

1. Start with 'Farewell message' on the left and 'User greeting' on the right, both open. (00:00.0; 0000.0)
2. Drag the 'Farewell message' view by its tab. This is inferred from the drag chip under the cursor. A highlight covers the left ~half of its own view. (00:02.0; 0002.0)
3. Move the drag over the sibling 'User greeting' view. The highlight covers only the left ~half of that view. (00:03.0; 0003.0, 0004.0)
4. Move the cursor back to the left edge of the sibling. The highlight now covers the right half of the left view, which is the view's own slot. (00:05.0; 0005.0)
5. Release (inferred from the chip disappearing). The views swap: 'User greeting' is now on the left and 'Farewell message' on the right. Each takes a half-width slot, with no extra split. (00:06.0; 0006.0, 0008.0)

Expected (implied): The highlighted region should match the resulting layout. Either the drop should create a split in the highlighted position, or the preview should show a swap or full-pane target.

Actual: The preview highlights a partial area, partly over the dragged view's own pane and partly over the sibling. The drop then reorders or swaps the views into the two existing slots, which does not match the highlight.

Key events: 0003.0, 0005.0, 0006.0

Missed by the author:

- After release the order of the two views is swapped, which is the visible effect of the drop (0006.0).

Claims:

- "The drag highlights half of its own view and half of the sibling view." [It will highlight half of its own view and half of the sibling view]: confirmed - At 0002.0 the highlight covers part of the own view, and at 0003.0–0005.0 it covers part of the sibling or of the own view's right half.
- "On release the view takes a full space, not half." [when I release the chat view it takes up a full space, not half a space]: not shown - After the drop (0006.0) the two views are equal width and swapped. The result looks like the same slot size as before, which I cannot distinguish from 'full space' without the earlier layout.
