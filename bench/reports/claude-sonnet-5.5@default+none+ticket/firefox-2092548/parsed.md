# real/firefox-2092548

_claude-sonnet-5.5@default, 14 s; looked at: nothing_

With vertical tabs, a collapsed sidebar and "Expand sidebar on hover" enabled, the page content area briefly resizes or reflows for about one frame when the sidebar collapses after hover. The content should stay the same size because the sidebar overlays it. The flicker is a visual glitch that can cause layout jumps. The report is written from the ticket text alone, since there is no video.

## Vertical tabs hover-expand: content area reflows for one frame when sidebar collapses

Class: **intermittent**

Environment: Firefox 160.0 on Linux x86_64 (X11). The ticket says Google was open in the recording. No accounts or organizations are mentioned.

Steps:

1. Enable vertical tabs, collapse the sidebar, and turn on "Expand sidebar on hover". (00:00.0; )
2. Hover the collapsed sidebar so it expands over the page. (00:00.0; )
3. Move the cursor away so the sidebar collapses. (00:00.0; )

Expected (implied): The sidebar overlays the content on both expand and collapse, so the content area never changes size.

Actual: When the sidebar collapses, the page content area briefly resizes or reflows (shifts to a different width for about one frame) before snapping back to its correct size.

Key events: 

Claims:

- "The content area reflows when the sidebar is opened and closed." [when you open and close the sidebar, it resizes/reflows the window]: not shown - There is no video. The ticket body says the reflow happens on collapse, while the attachment note says on open and close, so the two descriptions differ.
- "The reflow lasts about one frame and then snaps back to the correct size." [briefly resizes/reflows (shifts to a different width for ~1 frame) before snapping back]: not shown - There is no recording to check it against.
