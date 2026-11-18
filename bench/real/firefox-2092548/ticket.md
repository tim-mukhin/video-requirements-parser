# Vertical-tabs hover-expand: content area briefly reflows for one frame when the sidebar collapses

Source: https://bugzilla.mozilla.org/show_bug.cgi?id=2092548  (reporter: <email>, filed 2026-11-13)

[attachment: recording.mp4]
You can see google opened, when you open and close the sidebar, it resizes/reflows the window

User Agent: Mozilla/5.0 (X11; Linux x86_64; rv:160.0) Gecko/20100101 Firefox/160.0

### Steps to reproduce

1. Enable vertical tabs, collapse the sidebar, and turn on "Expand sidebar on hover".
2. Hover the collapsed sidebar so it expands over the page.
3. Move the cursor away so it collapses.

### Actual results

As the sidebar collapses, the page content area briefly resizes/reflows (shifts to a
different width for ~1 frame) before snapping back to its correct size.

### Expected results

The sidebar overlays the content on both expand and collapse, so the content area never
changes size
