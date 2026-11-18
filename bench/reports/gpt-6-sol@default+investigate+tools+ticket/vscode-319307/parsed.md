# real/vscode-319307

_gpt-6-sol@default, 34 s; looked at: frames/0000.0.jpg, frames/0002.5.jpg, frames/0003.0.jpg, frames/0005.5.jpg, frames/0006.0.jpg, frames/moments/p006.jpg, frames/moments/p020.jpg, frames/moments/p026.jpg, frames/moments/p022.jpg, frames/moments/p036.jpg, frames/moments/p056.jpg, frames/moments/p057.jpg, frames/0007.5.jpg, frames/0008.0.jpg_

Dragging an open chat view previews a half-pane destination, but dropping it swaps two full-width chat views. The highlight therefore misrepresents the resulting layout.

## Chat view drag highlight previews half a pane, but drop swaps full panes

Class: **wrong-data**

Environment: VS Code on macOS, with Farewell message and User greeting chat views side by side and Changes on the right.

Steps:

1. Drag the Farewell message view by its title. Over its original pane, the preview highlights only the pane's right half. (00:01.7; p006, p010)
2. Move the dragged view over User greeting; the preview highlights half of that pane. (00:02.9; p012, p015, p026)
3. Release over the highlighted half of User greeting. (00:06.1; p026, p030, p031)

Expected (implied): The drop highlight should preview the final layout: a full-pane swap should not be shown as a half-pane destination.

Actual: Farewell message takes the entire right pane and User greeting takes the entire left pane; no half-width chat pane remains.

Key events: p006, p010, p012, p026, p030, p031

Missed by the author:

- The drop swaps Farewell message and User greeting rather than creating a smaller pane; the Changes pane stays in place [p026, p030, p031].

Claims:

- "Dragging Farewell message highlights half of its own view and half of the sibling view." [ticket.md]: confirmed - The preview highlights half of the original pane at 2.5 s and half of the sibling pane at 3.0 and 5.5 s, at different points in the drag.
- "On release, the chat view takes up a full space rather than half a space." [ticket.md]: confirmed - The preview disappears at 6.118 s; the subsequent view shows both chats occupying full panes in swapped positions.
