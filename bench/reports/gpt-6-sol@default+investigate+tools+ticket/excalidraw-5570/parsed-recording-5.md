# real/excalidraw-5570

_gpt-6-sol@default, 34 s; looked at: frames/moments/p034.jpg, frames/moments/p025.jpg, frames/moments/p054.jpg, frames/0008.5.jpg, frames/0011.5.jpg, frames/moments/p010.jpg, frames/0006.0.jpg, frames/0006.5.jpg, frames/0007.0.jpg, frames/0009.5.jpg, frames/moments/p005.jpg, frames/moments/p050.jpg, frames/000172.jpg, frames/000190.jpg, frames/000036.jpg, frames/0005.5.jpg_

On mobile Excalidraw, an arrow-point context menu can jump from a fully visible position to the bottom of the screen, where most commands are cut off. The video establishes inconsistent placement, but does not show whether scrolling the menu works.

## Arrow-point context menu jumps below the mobile viewport

Class: **intermittent**

Environment: excalidraw.com in a mobile Chrome browser on Android. The recording does not establish the device model or Chrome version.

Steps:

1. With an arrow in point-editing mode, open its context menu near the middle point (the trigger is not visible). (00:06.1; p021, p022, p024)
2. Observe the open menu: at 6.8 s it jumps downward, leaving only its first commands visible. (00:06.8; p025, p034, p026, p027, p028, p029, p030, p031, p032, p033)

Expected (implied): The context menu stays within the visible viewport so its commands remain accessible.

Actual: At 6.1 s the full menu is visible; at 6.8 s it shifts downward and most commands extend below the screen. A later opening at 11.2 s is also clipped, while the opening at 9.3 s is fully visible.

Key events: p024, p025, p034, p046, p054

Missed by the author:

- The menu is fully visible at 6.1 s before moving down at 6.8 s [p024, p034]; the timeline establishes the jump and the frames show its effect.
- At 9.3 s the full menu fits on screen [p046], contrasting with the clipped menu at 11.2 s [p054].

Claims:

- "The context menu is displayed, then repositioned." [ticket.md]: confirmed - The menu is fully visible at 6.1 s and jumps downward at 6.8 s [p024, p034]; the frames settle what the move means.
- "Context-menu scrolling does not work consistently." [ticket.md]: not shown - The video shows clipping, but no identifiable attempt to scroll the menu.
- "This recording is from a Pixel 4A running Chrome 104.0.5112.69." [ticket.md]: not shown - Neither the model nor version appears on screen; the ticket identifies recording-1 as its Pixel 4A attachment, whereas this input is recording-5.
- "Repositioning is not observable on the Samsung Note 8." [ticket.md]: not shown - No comparison device appears in this recording.
