# real/excalidraw-5570

_gpt-6-sol@default, 41 s; looked at: frames/0002.0.jpg, frames/0004.0.jpg, frames/0004.5.jpg, frames/0005.0.jpg, frames/0005.5.jpg, frames/moments/p010.jpg, frames/moments/p011.jpg, frames/moments/p003.jpg, frames/0003.5.jpg, frames/0006.5.jpg, frames/0012.0.jpg, frames/moments/p014.jpg, frames/moments/p034.jpg, frames/0000.0.jpg, looks/0004.85-0005.30-165_190_230_570/sheet.jpg, looks/0006.20-0006.70-175_180_215_580/sheet.jpg_

On the recorded mobile Excalidraw page, a selected rectangle's context menu briefly appears fully visible, then jumps down and is clipped by the bottom of the screen. The jump hides commands and is easy to miss at normal playback speed.

## Context menu jumps below the mobile viewport after opening

Class: **intermittent**

Environment: excalidraw.com in a portrait mobile browser with a Brave icon visible. The device model and browser version are not shown.

Steps:

1. Start with the rectangle already selected near the bottom of the canvas. (00:01.1; p001)
2. Open its context menu (the trigger is not visible). (00:04.8; p010)

Expected (implied): The context menu remains within the visible screen so its commands are accessible.

Actual: At 5.024 s the full menu is visible above the rectangle; by 5.065 s it has jumped beside the rectangle with its lower commands below the screen. Frame-by-frame inspection shows the same change again at 6.388–6.429 s. The watcher identified clipped and higher positions, but the intervening frames establish that the menu moves during an opening, not merely between openings. No attempted scroll is identifiable.

Key events: p010, p011, p014

Missed by the author:

- In this recording, the full menu lasts only about one frame before jumping to the clipped position at 5.065 s; the same transition recurs at 6.429 s [p010, p014].
- A Brave icon is visible in the browser bar; this recording does not establish Chrome 104 or a Pixel 4A [p001].

Claims:

- "The context menu is displayed, then repositioned." [ticket.md]: confirmed - Consecutive video frames at 5.024 and 5.065 s show the fully visible menu jump to a clipped position.
- "Context-menu scrolling does not work consistently." [ticket.md]: not shown - The recording demonstrates clipping, but shows no identifiable scroll gesture.
- "The Pixel 4A recording used Chrome 104.0.5112.69." [ticket.md]: not shown - The ticket calls that attachment recording-1.mp4; this input is recording-2.mp4. Its browser bar shows a Brave icon, while the device model and browser version are not visible.
