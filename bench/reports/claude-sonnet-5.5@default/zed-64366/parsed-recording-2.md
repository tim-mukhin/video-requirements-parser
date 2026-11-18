# real/zed-64366

_claude-sonnet-5.5@default, 30 s; looked at: frames/000066.jpg, frames/000121.jpg, frames/000330.jpg, frames/000792.jpg_

The author opens the Explorer context menu in VS Code (WSL: Ubuntu, jellyfin-web) on many folders and files, one after another. The video has no speech, so the intended problem is not stated. The most visible oddities are that the menu offers 'Delete Permanently' (shown with the Del key) and 'Download...', and that the menu opens and closes repeatedly.

## Explorer context menu in WSL workspace offers 'Delete Permanently' and 'Download...' instead of the usual Delete

Class: **wrong-data**

Environment: VS Code in a WSL: Ubuntu remote window, workspace jellyfin-web, branch fix/tizen-pause-key. The Explorer sidebar is open and the editor area is empty (welcome watermark). The status bar shows Sign In and a Copilot/Continue item. No speech.

Steps:

1. Click on the .github folder in the Explorer. A context menu opens (New File, New Folder, Reveal in File Explorer, Cut/Copy/Paste, Download..., Copy Path, Rename, Delete Permanently). The trigger is probably a right-click; the timeline records only an inferred click. (00:02.1; p033, p034, p039, p057)
2. Click on another folder row. The previous menu closes and a new one opens. The same menu content repeats. (00:04.2; p090, p091)
3. Click on a file such as CONTRIBUTING.md or cssnano.config.js. The file menu opens with Open Preview, Open to the Side, Open With..., Select for Compare, Find File References, Open Timeline, Add File to Chat, Download... and Delete Permanently. (00:10.9; p280, p281)
4. Repeat on .sonarcloud.properties, .npmignore, .gitignore and .escheckrc. Each time the menu lists 'Delete Permanently' with Del, and 'Download...'. (00:13.8; p291, p292, p293, p307, p456, p458, p520, p524)

Expected (implied): A local or WSL workspace context menu would normally offer a regular 'Delete' (move to trash) and no 'Download...'. This is inferred from the screen, since the author says nothing.

Actual: The menus show 'Delete Permanently' (Del) and 'Download...' for every item. 'Paste' is greyed out on the folder menu. The menus also appear and disappear repeatedly while the author clicks around. The video ends with a click on the title bar at [844,65] and no visible failure.

Key events: p034, p057, p048, p281, p293, p307, p524

Missed by the author:

- The menu text carries no error. No action visibly fails. The exact problem the author wants to show cannot be determined from the video. The best candidate is the 'Delete Permanently' and 'Download...' entries in the context menu of a WSL window (p057, p048, p293, p307).
- A flash of the Explorer header at 00:04.0 and 00:05.3 (p063, p120) coincides with menu closing. It looks like a short re-render of the sidebar between menus, with no lasting effect.
