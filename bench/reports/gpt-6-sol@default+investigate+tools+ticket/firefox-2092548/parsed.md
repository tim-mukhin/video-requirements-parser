# real/firefox-2092548

_gpt-6-sol@default, 55 s; looked at: frames/moments/p011.jpg, frames/moments/p032.jpg, frames/moments/p012.jpg, frames/moments/p033.jpg, frames/moments/p010.jpg, frames/moments/p025.jpg, frames/moments/p004.jpg, frames/moments/p014.jpg, frames/0001.5.jpg, frames/0002.0.jpg, frames/moments/p023.jpg, frames/moments/p043.jpg_

When Firefox's hover-expanded vertical-tab sidebar collapses, Google content briefly shifts right before returning to its original position. The half-second frames miss the shift, but the timeline's short-event strips show it on both recorded collapses.

## Google page briefly shifts when hover-expanded vertical-tab sidebar collapses

Class: **intermittent**

Environment: Firefox with vertical tabs and 90% zoom, displaying www.google.com. The ticket reports Firefox 160.0 on Linux; the video does not show the version or OS.

Steps:

1. With the vertical-tab sidebar collapsed on Google, move the pointer onto the sidebar edge; it expands. The timeline infers a click at the edge, but the visible action does not establish one. (00:01.2; p003, p004, p005)
2. Move the pointer away from the expanded sidebar toward the page; it collapses. Repeat the hover-and-leave sequence: the same brief shift is recorded on the second collapse. (00:01.7; p011, p012, p013, p032, p033, p034)

Expected (implied): The sidebar should overlay the page without changing the content layout during collapse.

Actual: During each recorded collapse, the Google content shifts about 21 pixels right and returns roughly 33–34 ms later [p011, p032]. The top-right links and Sign in button shift about 43 pixels right, briefly clipping Sign in at the screen edge [p012, p033]. The sidebar does collapse [p020, p040].

Key events: p011, p012, p020, p032, p033, p040

Missed by the author:

- The short-event strips show the shift on a second collapse as well [p032, p033]; it is absent from the watcher's sampled frames.
- Firefox displays 90% zoom [s001].

Claims:

- "The page briefly reflows as the sidebar collapses." [ticket.md]: confirmed - The timeline and short-event strips capture the shift twice; the watcher's half-second frames missed it.
- "Opening and closing the sidebar resizes or reflows the window." [ticket.md]: not shown - A brief content shift is visible during collapse; the video does not establish a browser-window resize or a corresponding shift on expansion.
- "Expand sidebar on hover is enabled." [ticket.md]: not shown - The sidebar expands as the pointer reaches it, but the setting itself is not displayed.
- "The recording uses Firefox 160.0 on Linux." [ticket.md]: not shown - Neither the browser version nor OS is visible.
