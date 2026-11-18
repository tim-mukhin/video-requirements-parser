# real/firefox-2092548

_claude-sonnet-5.5@default, 26 s; looked at: frames/moments/p011.jpg, frames/moments/p012.jpg_

With the vertical-tabs sidebar set to expand on hover, the page content shifts sideways for one frame (about 33 ms) just before the expanded sidebar collapses. The Google logo and search box jump about 21 px right, and the Gmail/Sign in header jumps about 43 px right. This happens twice, and it matches the ticket's one-frame reflow. The sidebar is meant to overlay the page, so the content should never move.

## Vertical tabs: page content shifts for one frame as the hover-expanded sidebar collapses

Class: **intermittent**

Environment: Firefox with vertical tabs (the ticket gives Linux x86_64, Firefox 160), one tab on www.google.com at 90% zoom. The sidebar is collapsed to icons and expands on hover. No account is visible. The recording is 1280x720 and 5.1 s long.

Steps:

1. With the sidebar collapsed, move the cursor to its left edge. It expands over the page and shows 'Google ×' and '+ New Tab'. Hover and click are inferred; the enabled settings are not visible. (00:01.2; p003, p004, p005)
2. The content shifts for one frame (logo and search box +21 px, header +43 px), then returns to its place. Frames at 1.700 s show 'Sign in' pushed off the right edge. (00:01.7; p011, p012)
3. Move the cursor away. The sidebar collapses to icons and the covered page text (About/Store, India, Advertising, Business) comes back. (00:01.8; p013, p014, p020)
4. Repeat: expand at 2.6 s, then a one-frame shift of the same size at 3.0 s, and collapse at 3.1-3.2 s. In the two cycles checked, the shift happened both times. (00:03.0; p024, p032, p033, p034, p035)

Expected (implied): The sidebar overlays the content on both expand and collapse, and the content area never changes size.

Actual: Before each collapse, the page content jumps right for about one frame (33 ms) and snaps back. A reflow is visible at the point the sidebar is collapsing.

Key events: p011, p012, p032, p033

Missed by the author:

- The shift lasts one frame, at 1.700 s and again at about 3.0 s, so it is easy to miss. It comes just before the collapse, not on expand (p011, p012, p032, p033).
- The settings from ticket step 1 (vertical tabs, collapsed, expand on hover) are not shown in the video.

Claims:

- "When the sidebar opens and closes, the window or content resizes or reflows (ticket)" [ticket]: confirmed - The moment strips for p011/p012 show the content moving for one frame. The video has no speech.
- "The sidebar overlays the content rather than resizing it during the steady expanded state (ticket's expected result)" [ticket]: confirmed - At 1.5 s and 3.0 s the sidebar covers the left page text without moving the rest of the page. The only shifts are the one-frame jumps.
