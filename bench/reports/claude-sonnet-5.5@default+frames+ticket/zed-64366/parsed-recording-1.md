# real/zed-64366

_claude-sonnet-5.5@default, 26 s; looked at: frames/0000.0.jpg, frames/0010.0.jpg, frames/0020.0.jpg, frames/0030.0.jpg, frames/0036.5.jpg_

In Zed, the Project Panel context menu is taller than the window and is cut off. The video shows it opened on a Project Panel entry (a folder at 0.0 s, a file at 20.0 s and 30.0 s). The menu's bottom items (Expand All, Rename and below) run off the bottom edge in every frame viewed. The menu keeps moving, and at 10.0 s its top is also cut off. The menu is not repositioned or scrolled to fit, so the lower actions cannot be reached or read.

## Project Panel context menu is clipped at the window edge (bottom, and top at 10.0 s)

Class: **wrong-data**

Environment: Zed (the ticket gives v1.20.2 stable on Windows 10), Project Panel on the right with project 'jellyfin-web' (WSL Ubuntu, branch main / fix/tizen-pause-key). A 'Restart to Update' button is in the title bar. The window is about 1280x751 in the frames.

Steps:

1. A Project Panel context menu is already open on the 'components' folder (the cursor is on that row). The menu is taller than the window and is cut off at the bottom: 'Expand All' is only partly visible and nothing below it can be seen. (00:00.0; 0000.0)
2. The cursor moves over the menu (inferred: the user is hovering or scrolling). The menu is shifted so its top is cut off ('New File' is hidden) and its bottom is still cut off after 'Expand All'. The highlighted row in the panel is now 'constants'. (00:10.0; 0010.0)
3. The panel has scrolled and the menu is open for the file 'apiclient.d.ts'. The menu shows items such as 'Open File Permalink', and the bottom is cut off at 'Rename'. Trash, Delete and Expand All are not visible. (00:20.0; 0020.0)
4. The menu is open for 'index.html' near the bottom of the panel. The bottom is still cut off after 'Rename'. (00:30.0; 0030.0)

Expected (implied): The context menu should reposition or shrink so that all of it stays inside the window, as the ticket says VS Code does.

Actual: The menu extends beyond the bottom edge of the window in every frame viewed. Items such as Trash, Delete and Expand All are cut off or hidden. At 10.0 s the menu's top item is also hidden.

Key events: 0000.0, 0010.0, 0020.0, 0030.0

Missed by the author:

- The menu is already open at 0.0 s, so the right-click is not in the recording. It was not possible to see how the menu first opens.
- At 10.0 s the menu's top item 'New File' is also cut off, so the clipping is not only at the bottom (0010.0).
- The window is only about 751 px high in the frames and the menu has about 25 entries, which may be why it does not fit. The menu is also clipped when opened on a row that is not at the very bottom of the panel (0000.0, 0020.0).

Claims:

- "The context menu extends past the bottom edge of the Zed window, clipping lower items." [The context menu extends beyond the bottom edge of the Zed window, causing some menu items to be clipped]: confirmed - The menu is cut at the bottom edge in the frames at 0.0, 10.0, 20.0 and 30.0 s.
- "VS Code repositions its menu in the same situation." [VS Code repositions the context menu when there is not enough space below]: not shown - I only viewed this recording, which shows Zed. The VS Code comparison is presumably in recording-2.
- "It happens with a clean installation or configuration." [This also occurs with a clean Zed configuration.]: not shown - The frames show no settings or config state.
