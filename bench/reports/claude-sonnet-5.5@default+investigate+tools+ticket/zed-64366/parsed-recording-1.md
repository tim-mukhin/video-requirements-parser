# real/zed-64366

_claude-sonnet-5.5@default, 25 s; looked at: frames/0006.0.jpg, frames/0019.0.jpg_

In Zed's Project Panel, right-clicking an entry in the lower half of the tall panel opens a context menu that runs past the bottom edge of the window. The last items (Delete, and in one case Trash, Rename, Delete) are cut off and cannot be read or clicked. The menu is shifted upward, but not enough to fit. The video confirms the ticket's core claim.

## Project Panel context menu is clipped at the bottom of the window when opened on lower entries

Class: **wrong-data**

Environment: Zed (the ticket gives v1.20.2 stable on Windows 10, which the video does not show). Window 1918x1126 in the recording, light theme. Project 'jellyfin-web' over WSL 'Ubuntu', branch main / fix/tizen-pause-key, 'Restart to Update' button in the title bar. Project Panel docked on the right, showing the src folder. The recording shows only Zed, with no VS Code comparison.

Steps:

1. With the Project Panel open on the src folder, right-click the folder 'constants' (the click is inferred from the cursor stopping, then the menu opening). A menu of about 25 entries opens. It is shifted up but still runs off the bottom edge: the last visible row is 'Delete', with a sliver of a further row below it. The frame at 6.0 s shows this. (00:04.9; p038, p039)
2. Repeat on a row in the middle of the panel ('hooks'). The menu opens again and bounces up and down by 46 px as it is positioned, still clipped at the bottom. (00:11.7; p073, p076, p088, p098)
3. Scroll the panel down and right-click the file 'apiclient.d.ts'. The file menu is longer, with Open File Permalink and Copy File Permalink. It is cut off after 'Rename' (frame at 19.0 s), so Trash and Delete are not visible. (00:18.4; p112, p114)
4. Repeat further down the panel (fails every time it was checked in the frames viewed). The watcher saw the menu still cut off after 'Rename' for a menu opened on 'index.html' at about 30 s. (00:21.5; p117, p118)

Expected (implied): The context menu should reposition or shrink so that all of its entries stay inside the window, as the reporter says VS Code does.

Actual: The menu is taller than the space available. It is nudged upward but still extends past the bottom of the window. The lowest entries (Delete for the folder menu; Trash, Delete and Expand All for the file menu) are clipped and unreachable.

Key events: p039, p076, p114, p118

Missed by the author:

- The ticket says the menu is clipped near the bottom of the panel, but it is clipped for rows high in the list too, such as 'constants' (p038, p039).
- The menu bounces by 46 px up and down while it opens (p088, p098, p065), so its position is recomputed more than once.
- Several flickers of menu text (p018 to p022, p049 to p051) are part of the menu being drawn and moved. The window is only about 1126 px tall in the recording, which may be why the menu does not fit.

Claims:

- "The context menu extends past the bottom edge of the Zed window, clipping lower items." [ticket]: confirmed - Frames at 6.0 s and 19.0 s show the menu cut off at the bottom edge.
- "The menu is clipped when the item is near the bottom of the Project Panel." [ticket]: confirmed - It is clipped on folders high in the list ('constants') as well as on lower files. The menu is clipped in every frame checked, so it does not depend on the item being at the very bottom.
- "VS Code repositions its menu in the same situation." [ticket]: not shown - This recording shows only Zed.
- "It also happens with a clean Zed configuration." [ticket]: not shown - The video shows no settings or config state.
- "Zed version and OS (Windows 10, v1.20.2)." [ticket]: not shown - No version or OS is visible. The window has Windows-style controls, and the shortcuts shown are Ctrl-based.
