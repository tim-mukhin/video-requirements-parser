# real/kde-528684

_gpt-6-sol@default, 43 s; looked at: frames/0005.0.jpg, frames/0005.5.jpg, frames/moments/p070.jpg, frames/moments/p075.jpg, frames/moments/p246.jpg, frames/0019.5.jpg, frames/0020.5.jpg, frames/0021.5.jpg, frames/0022.0.jpg, frames/moments/p254.jpg, frames/moments/p269.jpg, frames/moments/p044.jpg, frames/moments/p056.jpg, frames/0007.0.jpg, frames/0008.0.jpg, frames/0010.5.jpg, frames/0024.5.jpg, frames/0004.0.jpg, frames/0011.5.jpg, frames/moments/p248.jpg, frames/moments/p249.jpg_

After a Konsole window is moved away, its pinned launcher also disappears from the Icons-Only Task Manager, leaving no Konsole icon on the visible desktop. The video shows a similar disappearance with Serein, but does not show the keys used or establish the claimed regression.

## Pinned launcher disappears when its window leaves the visible desktop

Class: **silent-fail**

Environment: KDE desktop with a left-side Icons-Only Task Manager, Konsole and Serein; the Konsole prompt shows matthew@kde-linux. The ticket lists Plasma 6.8.80 and Wayland, but those details are not visible in the recording.

Steps:

1. Start with the Konsole icon visible in the left-side Task Manager. (00:04.0; p042)
2. Open Konsole (the trigger is not visible). (00:04.4; p044)
3. Move the Konsole window to another virtual desktop, as the on-screen caption describes; the shortcut itself is not visible. The window and its Task Manager icon disappear. (00:05.4; p047, p068)

Expected (implied): Konsole remains available as a pinned launcher on the desktop where its window is no longer shown.

Actual: At 5.4 seconds the Konsole window is gone and the left-side launcher is missing. At 8.0 seconds both the window and icon are visible again. Serein is shown pinned at 19.2 seconds; after its window disappears, its icon is also absent at 21.1 seconds.

Key events: p044, p047, p068, p069, p151, p247, p250

Missed by the author:

- Serein's Task Manager menu says "Unpin from Task Manager" [p151], establishing that it too is pinned; its icon is absent after its window disappears [p247]. The frames settle this second example, whereas the timeline alone does not identify the missing icon.
- Contrary to the watcher's note, Serein's icon has not returned at 22.0 seconds [p248]; it is visible again with the window at 24.4 seconds [p250].

Claims:

- "Moving a pinned Konsole window with a keyboard shortcut removes its Task Manager icon." [ticket.md; on-screen caption p047]: confirmed - The window and icon disappear together; the recording does not show the keystroke.
- "Switching virtual desktops brings the icon back." [ticket.md]: confirmed - Following a desktop transition, the Konsole window and icon are visible at 8.0 seconds. The video does not separately show the launcher restored on the empty desktop.
- "Pressing Meta restores the missing icon." [ticket.md]: not shown - The application launcher appears later, after the Konsole icon has already returned.
- "The same issue happens with apps minimized to the tray." [on-screen caption p150]: not shown - Serein is visibly pinned and its icon disappears, but the recording does not establish that its window was minimized to the tray.
- "This is a regression on current git master." [ticket.md]: not shown - No build identification or earlier-version comparison appears in the video.
