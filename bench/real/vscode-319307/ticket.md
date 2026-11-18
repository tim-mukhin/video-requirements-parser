# Dragging already opened chat session view highlights half of view, not full view

Source: https://github.com/microsoft/vscode/issues/319307  (reporter: aiday-mar, filed 2026-06-01)

Testing #318979

- Consider the screen recording below
- Drag the `Farewell message` chat view
- It will highlight half of its own view and half of the sibling view
- Yet when I release the chat view it takes up a full space, not half a space
- It is a bit confusing

[attachment: recording.mp4]
