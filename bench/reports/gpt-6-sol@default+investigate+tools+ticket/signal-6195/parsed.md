# real/signal-6195

_gpt-6-sol@default, 36 s; looked at: frames/moments/p020.jpg, frames/moments/p038.jpg, frames/moments/p041.jpg, frames/moments/p053.jpg, frames/0000.0.jpg, frames/0004.0.jpg, frames/0008.5.jpg, frames/moments/p001.jpg, frames/moments/p010.jpg, frames/moments/p026.jpg, frames/0001.0.jpg, frames/0002.0.jpg, frames/0006.0.jpg_

In Signal Desktop's macOS image editor, some attempts to draw at the top of a tall image move the entire window instead of adding a mark. Other strokes at the same edge succeed, making annotation unreliable and eventually pushing the bottom controls off-screen.

## Drawing at the top of an image can drag the editor window

Class: **intermittent**

Environment: Signal Desktop image editor on macOS. The ticket reports Signal 6.0.0-beta.3 and macOS 13.1 Beta; neither version is visible in the recording.

Steps:

1. Start with a tall image open in the editor, its top edge close to the window top and the green drawing tool selected. How the image was opened is not visible. (00:00.0; s001)
2. Draw near the image's top edge; a green stroke appears. (00:00.4; p001)
3. Continue dragging near that edge. The editor window moves with the image instead of adding the intended stroke. (00:03.8; p020)

Expected (implied): Dragging on the canvas draws there without moving the editor window.

Actual: The window and canvas shift together during some top-edge drags, while existing green marks stay fixed on the image. Later drags again move the window, leaving its bottom controls below the visible screen.

Key events: p001, p010, p020, p026, p038, p041, p053

Missed by the author:

- The green drawing tool is already selected when recording begins [s001].
- Repeated window movement pushes the editor's bottom controls below the visible screen [p038, p041]. The moment frames establish this movement; the timeline's changing toolbar text alone does not establish a separate toolbar failure.

Claims:

- "Drawing near the top can drag the window instead." [ticket.md: Bug Description]: confirmed - The timeline records top-edge drags, and the moment frames for p020 and p038 show the entire editor shifting.
- "Window dragging makes drawing at the top difficult." [ticket.md: Actual Result]: confirmed - The p001 moment shows a successful green stroke; the p020 and p038 moments show subsequent window movement instead. It is not a constant failure.
- "The problem may be easier to reproduce with portrait-oriented images." [ticket.md: Steps to Reproduce]: not shown - The image shown is tall, but no other orientation is tested.
- "Attach an image, open markup, and adjust Signal Desktop's width." [ticket.md: Steps to Reproduce]: not shown - The recording begins with the editor already open and the image near its top.
