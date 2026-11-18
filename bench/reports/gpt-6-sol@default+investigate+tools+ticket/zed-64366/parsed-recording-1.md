# real/zed-64366

_gpt-6-sol@default, 45 s; looked at: frames/0024.5.jpg, frames/0026.0.jpg, frames/0028.0.jpg, frames/0032.0.jpg, frames/moments/p088.jpg, frames/moments/p098.jpg, frames/0005.0.jpg, frames/0012.5.jpg, frames/0018.5.jpg, frames/0031.5.jpg, frames/moments/p047.jpg, frames/moments/p065.jpg, frames/moments/p109.jpg_

Zed's Project Panel context menu can extend below the window, hiding commands such as Trash and Delete. The video shows the full menu for one file, then a clipped menu for another file only slightly lower in the panel.

## Project Panel context menu is clipped at the bottom of the window

Class: **silent-fail**

Environment: Zed with the jellyfin-web project open and the Project Panel on the right. The title bar shows Ubuntu and Restart to Update; the recording does not establish the OS or Zed version.

Steps:

1. In the Project Panel, navigate until src/index.html is visible below apiclient.d.ts. (00:22.9; p123)
2. Right-click src/index.html; the menu opens beside its row with its lower commands below the window edge. (00:27.7; p129, p130)

Expected (implied): Keep the entire context menu within the window so every command remains visible.

Actual: At 27.8 s, the menu starts beside index.html but extends below the window; even Rename is at the bottom edge, while Trash and Delete are hidden. By contrast, the menu opened for apiclient.d.ts at 24.3 s shows both Trash and Delete. The watcher marked the menu at 26 s as clipped, but the frame at that time shows it fully visible.

Key events: p124, p125, p129, p130, p141, p142

Missed by the author:

- The menu is fully visible for apiclient.d.ts at 24.3 s, but clipped for index.html at 27.8 s [p124, p125, p129, p130].
- The menu briefly shifts upward and then down during earlier openings; the moment frames show the movement, not a lasting correction [p065, p088, p098].

Claims:

- "The context menu extends beyond the window and hides lower items." [ticket.md]: confirmed - The index.html menu at 27.8 s and another menu at 31.4 s are clipped; the apiclient.d.ts menu at 24.3 s is fully visible.
- "The selected file or folder must be near the bottom of the visible Project Panel." [ticket.md]: refuted - index.html is in the upper part of the panel when its menu is clipped.
- "The issue occurs with a clean Zed configuration." [ticket.md]: not shown
- "VS Code repositions the equivalent menu." [ticket.md]: not shown
- "The ticket's Zed version and Windows system specifications describe this recording." [ticket.md]: not shown - No version or system-information screen appears; the title bar displays Ubuntu.
