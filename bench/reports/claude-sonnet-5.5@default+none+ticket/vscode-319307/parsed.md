# real/vscode-319307

_claude-sonnet-5.5@default, 13 s; looked at: nothing_

Dragging an already-open chat session view (`Farewell message`) shows a drop highlight covering half of its own view and half of the sibling view. Releasing it makes it fill the full space, not half. The mismatch between the preview and the result is confusing.

## Dragging an already opened chat session view highlights half of the view instead of the full view

Class: **wrong-data**

Environment: VS Code (testing #318979), chat view `Farewell message`, with a sibling view beside it. The ticket gives no OS, build or account details.

Steps:

1. Open the chat session view `Farewell message` next to a sibling view, as in the recording. (00:00.0; )
2. Start dragging the `Farewell message` chat view. (00:00.0; )
3. Observe the drop highlight: it covers half of its own view and half of the sibling view. (00:00.0; )
4. Release the chat view. (00:00.0; )

Expected (implied): The drop highlight should match the area the view takes after release. Dropping a view that is already open should either highlight the full view, or the result should be half the space.

Actual: The highlight covers half of the dragged view and half of the sibling view. After release the chat view takes up the full space, not half.

Key events: 

Claims:

- "The highlight covers half of the dragged view and half of the sibling view." [It will highlight half of its own view and half of the sibling view]: not shown
- "On release the view takes the full space rather than half." [Yet when I release the chat view it takes up a full space, not half a space]: not shown
