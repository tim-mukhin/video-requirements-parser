# real/firefox-2092548

_claude-sonnet-5.5@default, 32 s; looked at: frames, frames/0000.0.jpg, frames/0000.5.jpg, frames/0001.0.jpg, frames/0001.5.jpg, frames/0002.0.jpg, frames/0002.5.jpg, frames/0003.0.jpg, frames/0003.5.jpg, frames/0004.0.jpg, frames/0004.5.jpg, frames/0005.0.jpg_

A Firefox window with vertical tabs shows google.com. The collapsed sidebar is expanded and collapsed twice, apparently by hovering and moving the mouse away. At 0.5 s sampling, the expanded sidebar overlays the page without moving it. One frame (2.5 s) during collapse shows an intermediate sidebar state. The ticket's one-frame content reflow is not clearly visible in these frames.

## Vertical-tabs hover-expand: sidebar/content flicker when the sidebar collapses

Class: **intermittent**

Environment: Firefox with vertical tabs (the ticket gives Linux x86_64, Firefox 160). The window shows www.google.com at 90% zoom, a single Google tab, and a dark themed sidebar. The visible Google page is the India version. No account is visible.

Steps:

1. Collapsed vertical-tabs sidebar (icons only, about 44 px wide) with the cursor in the page. The video does not show how the settings were enabled, so the ticket's step 1 is taken from the ticket. (00:00.0; 0000.0)
2. Cursor moves to the left edge or sidebar. The sidebar expands to about 198 px, showing the 'Google' tab and 'New Tab'. The page content stays at the same position, and the left part of the page (About/Store, India, Advertising, Business) is covered. I infer this is the hover expand. (00:01.5; 0001.0, 0001.5)
3. Cursor moves away from the sidebar and it collapses back to icons. (00:02.0; 0002.0)
4. Cursor returns to the left edge. One frame shows an intermediate state: the sidebar is only about 44 px wide but still draws clipped expanded content ('G', 'N' cut off). The sidebar toggle button is highlighted and a settings gear appears at the bottom. The page content is fully visible, including About/Store and the footer. (00:02.5; 0002.5)
5. The sidebar is fully expanded again, then collapses at 3.5 s and stays collapsed to the end. Page content is at the same position in every frame. (00:03.0; 0003.0, 0003.5, 0004.0, 0004.5, 0005.0)

Expected (implied): The sidebar overlays the content on both expand and collapse, and the content area never changes size or flickers (from the ticket).

Actual: The sidebar expands and collapses over the page. At 2.5 s there is a transitional frame in which the sidebar has collapsed to its narrow width but still draws clipped expanded contents. The page content is unchanged in all sampled frames, so a content width change or reflow is not visible at this sampling rate.

Key events: 0001.5, 0002.0, 0002.5, 0003.0

Missed by the author:

- At 2.5 s the sidebar is narrow but still draws clipped expanded contents, with a highlighted toggle and a settings gear. This is the most likely candidate for the visible glitch.
- The video does not show the enable/collapse settings from the ticket's step 1.
- The extension badge at the top right changes from 21 to 22 at 5.0 s. It is unrelated.

Claims:

- "Opening and closing the sidebar resizes or reflows the window or content." [when you open and close the sidebar, it resizes/reflows the window]: not shown - The Google logo, search box and header stay at identical coordinates in every frame, and the window size does not change. Only the sidebar width and the covered left part of the page differ. A one-frame reflow could fall between the 0.5 s samples.
- "The content area briefly changes width for about one frame as the sidebar collapses." [shifts to a different width for ~1 frame before snapping back]: not shown - No frame shows the content at a different width. The only anomaly is the intermediate sidebar frame at 2.5 s.
- "The sidebar overlays the content on expand." [The sidebar overlays the content on both expand and collapse]: confirmed - At 1.5 s and 3.0 s the sidebar covers the left page content without moving the rest of the page.
