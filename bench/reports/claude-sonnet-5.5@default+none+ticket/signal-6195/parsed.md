# real/signal-6195

_claude-sonnet-5.5@default, 15 s; looked at: nothing_

In Signal Desktop's image markup editor on macOS, drawing near the top of the image drags the window instead of drawing. This is most likely when the image is tall and its top sits close to the window's title/drag area. The top of the image is then hard to annotate.

## Image markup near top of window triggers window dragging instead of drawing (macOS)

Class: **wrong-data**

Environment: Signal Desktop 6.0.0-beta.3 on macOS 13.1 Beta (22C5050e). Linked device version not relevant. No account or organization details given. A debug log link is provided but not viewed.

Steps:

1. Attach an image to a message draft. Portrait images (height > width) may reproduce this more easily. (00:00.0; )
2. Click the image to open the markup/edit view. (00:00.0; )
3. Size the Signal Desktop window so the top of the image in the editor is close to the top of the window. (00:00.0; )
4. Try to draw near the top of the image. (00:00.0; )

Expected (speech): Touching the canvas never triggers window dragging, or the canvas does not extend into the window-drag area. The reporter offers either of these as acceptable.

Actual: The window is often dragged instead of a stroke being drawn near the top of the image. This makes it very hard to draw on the top of the image.

Key events: 

Claims:

- "Window dragging is often triggered when drawing near the top of the canvas." [Window dragging is often triggered, making it really hard to draw anything on the top of the image.]: not shown - There is no video, only the ticket text, so this can't be checked.
- **R1** [proposed] Drawing on the markup canvas must not start window dragging. (proposed by awaitlink) - Ticket: Expected Result, option 1
- **R2** [proposed] Alternatively, the canvas must not extend into the area that triggers window dragging. (proposed by awaitlink) - Ticket: Expected Result, option 2
- **R3** [open_question] Unclear: whether the bug occurs on other OSes, on non-beta versions, or only on macOS 13.1 beta. The ticket also doesn't say how far from the top it starts, or how often it happens ("often"). Both Signal's window size and the image's orientation affect it. The ticket's step numbering skips 2. - Ticket: Platform Info and Steps to Reproduce
