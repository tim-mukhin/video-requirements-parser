# real/zed-64366

_claude-sonnet-5.5@default, 27 s; looked at: frames, frames/0000.0.jpg, frames/0005.0.jpg, frames/0010.0.jpg, frames/0015.0.jpg, frames/0020.0.jpg, frames/0025.0.jpg, frames/0026.0.jpg, frames/0012.0.jpg_

This recording shows VS Code (WSL: Ubuntu, jellyfin-web), not Zed. It is the comparison clip the ticket mentions. The author right-clicks items in the Explorer, and the context menu shifts upward and stays inside the window each time. No Zed bug is visible in the video. It only shows the reference behaviour the reporter wants Zed to copy.

## Zed Project Panel context menu clipped at window bottom (video shows only VS Code reference behaviour)

Class: **not-a-bug**

Environment: VS Code on Windows, connected to WSL: Ubuntu, folder jellyfin-web, branch fix/tizen-pause-key, dark theme. Zed does not appear in any frame. The ticket gives Zed v1.20.2 on Windows 10.0.26200.

Steps:

1. In the VS Code Explorer, right-click the .devcontainer folder near the top. The menu opens below and right of the cursor, fully visible. (00:00.0; 0000.0)
2. Right-click .vscode. The menu is shifted up so it sits against the bottom edge of the window. The mouse cursor is in the middle of the menu rather than at its top corner. This is inferred from the cursor position. (00:05.0; 0005.0)
3. Right-click items near the bottom of the Explorer, such as the CONTRIBUTING.md and eslint rows. The menu is moved up so that all items, including Rename and Delete Permanently, are shown. (00:10.0; 0010.0, 0012.0)
4. Right-click .sonarcloud.properties and .editorconfig. The menu is again shifted up to fit. The menu closes between right-clicks. (00:15.0; 0015.0, 0020.0, 0025.0)

Expected (implied): In Zed, a Project Panel context menu opened near the bottom should reposition so the whole menu is visible, as the VS Code menu does in this recording.

Actual: The video shows VS Code only. Its context menus are placed so the full menu stays on screen, with Delete Permanently at the very bottom. The Zed clipping is not shown in any frame.

Key events: 0005.0, 0010.0, 0012.0, 0015.0

Missed by the author:

- The menu's last item (Delete Permanently) sits tight against the window's bottom edge, with the menu bottom at or near the frame edge (0005.0, 0012.0, 0020.0). The reference is not perfectly margin-padded.
- The menu contents differ by item: .md files show Open Preview, and one menu shows Find File References (0012.0). Folders show New File and New Folder (0000.0).

Claims:

- "VS Code repositions the context menu when there is not enough space below the item." [VS Code repositions the context menu when there is not enough space below the selected item, keeping the complete menu visible.]: confirmed - In frames 0005.0, 0010.0, 0012.0 and 0015.0 the menu is shifted upward. All items are visible, with Delete Permanently as the last one, close to the window bottom edge.
- "Zed's Project Panel context menu extends beyond the bottom edge of the window." [The context menu extends beyond the bottom edge of the Zed window, causing some menu items to be clipped]: not shown - Zed does not appear in this recording. It may be in recording-1.mp4.
