# real/zed-64366

_claude-sonnet-5.5@default, 17 s; looked at: nothing_

The recording shows VS Code (WSL: Ubuntu, jellyfin-web), not Zed. It is the comparison clip the ticket mentions. Right-click context menus in the Explorer stay fully visible, shifting up near the bottom of the window. The Zed clipping defect is not shown in this video.

## Zed Project Panel context menu clipped at window bottom (this video shows only the VS Code reference behaviour)

Class: **not-a-bug**

Environment: VS Code on Windows, connected to WSL: Ubuntu, folder jellyfin-web, branch fix/tizen-pause-key. Zed is not visible in the video. The ticket gives Zed v1.20.2 on Windows 10.0.26200, which the video does not confirm.

Steps:

1. Right-click a folder near the top of the VS Code Explorer. The full menu opens (New File, Rename, Delete Permanently and others). (00:02.1; p033, p034, p037)
2. Right-click items lower in the Explorer, then repeat on other rows near the bottom. The menu stays fully on screen each time, with Delete Permanently as the last item, and the previous menu closes between right-clicks. (00:05.5; p148, p182, p185, p212, p318, p343, p400, p456, p520)

Expected (implied): In Zed, a Project Panel context menu opened near the bottom of the window should reposition so the whole menu is visible, as VS Code does.

Actual: In this video VS Code menus stay entirely within the window. No Zed window or clipped menu appears. This is reference behaviour, not evidence of the Zed bug.

Key events: p033, p090, p148, p182, p318, p400

Missed by the author:

- The Delete Permanently item sits very close to the window's bottom edge in the shifted menus, so the VS Code reference has almost no margin (p037, p091).
- Menu contents differ by item type: folders show New File and New Folder, and files show other entries (p034 to p059, p091 to p116).

Claims:

- "VS Code repositions the context menu when there is not enough space below the selected item." [ticket]: confirmed - The VS Code menus near the bottom keep all items visible. Delete Permanently is the last item in each menu.
- "Zed's Project Panel context menu extends beyond the bottom edge of the window and clips items." [ticket]: not shown - Zed does not appear in this recording. It may be in recording-1.mp4.
