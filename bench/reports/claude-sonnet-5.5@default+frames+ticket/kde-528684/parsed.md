# real/kde-528684

_claude-sonnet-5.5@default, 51 s; looked at: frames, frames/0000.0.jpg, frames/0004.0.jpg, frames/0008.0.jpg, frames/0012.0.jpg, frames/0016.0.jpg, frames/0020.0.jpg, frames/0024.0.jpg, frames/0028.0.jpg, frames/0033.0.jpg, frames/0009.0.jpg, frames/0010.0.jpg, frames/0011.0.jpg, frames/0006.0.jpg, frames/0018.0.jpg, frames/0026.0.jpg, frames/0030.0.jpg, frames/0032.0.jpg, frames/0005.0.jpg, frames/0007.0.jpg, frames/0008.5.jpg, frames/0010.5.jpg, frames/0013.0.jpg, frames/0014.0.jpg, frames/0021.0.jpg, frames/0022.0.jpg_

The reporter moves the window of a pinned app (Konsole, then Serein) to another virtual desktop with a keyboard shortcut. For Konsole, the pinned icon disappears from the Icons-Only Task Manager while its window is off the current desktop. The icon comes back once desktops are switched. The Serein sequence does not clearly show the same failure.

## Pinned Konsole icon disappears from Task Manager after its window is moved to another virtual desktop

Class: **state-revert**

Environment: KDE Plasma on Wayland. Vertical Icons-Only Task Manager on the left edge with pinned apps: file manager, a blue asterisk app, Telegram, a purple app, and Konsole. Serein is also shown. Multiple virtual desktops. The clock reads 12:49-12:50 and the date 11/10/26. Version details come from the ticket only (Plasma 6.8.80, Frameworks 6.33.0, Qt 6.12.0); no version is visible in the video.

Steps:

1. Konsole is open on the current desktop. Its pinned icon is in the Task Manager and a hover tooltip titled 'Konsole' is shown. The video does not show the click that launched it (not shown; the ticket says it was opened from the pinned icon). (00:05.0; 0005.0, 0008.0)
2. Konsole is moved to another virtual desktop with a keyboard shortcut (key press inferred, not visible). The window is gone from the screen and the Konsole icon is also gone from the Task Manager, which now shows only four icons. (00:06.0; 0006.0, 0007.0)
3. The desktop switch animation plays (inferred switch of virtual desktops). The Konsole icon reappears in the Task Manager, drawn greyed out, with no window on this desktop. The Konsole window is visible on the other desktop with its icon highlighted. (00:08.5; 0008.5, 0009.0, 0010.0, 0011.0)
4. The move is repeated. The Konsole icon is missing again with an empty desktop, then reappears greyed out after the next desktop switch. (00:12.0; 0012.0, 0013.0, 0014.0)
5. Second example, Serein (also pinned, a tray-minimised app). Its window is on the current desktop and its context menu is open, showing 'Unpin from Task Manager'. After a move and desktop switches, its icon is still in the Task Manager, so the disappearance is not clearly reproduced for this app. (00:20.0; 0020.0, 0022.0, 0024.0, 0026.0, 0030.0)

Expected (implied): After the window moves to another desktop, the Konsole icon should stay in the Task Manager as a normal pinned launcher.

Actual: Right after the shortcut move, the Konsole pinned icon vanishes from the Task Manager (0006.0, 0007.0, 0012.0). It reappears only after a virtual desktop switch (0008.5, 0009.0, 0013.0).

Key events: 0005.0, 0006.0, 0007.0, 0009.0, 0012.0, 0013.0

Missed by the author:

- When the icon returns it is greyed out, like a launcher with no window on this desktop (0009.0, 0013.0). That matches the expected behaviour, so only the interval right after the move is wrong.
- Serein's icon stayed visible after its move (0022.0), so the failure is intermittent or app-specific, which the caption only hints at.
- The video shows no keyboard shortcut overlay, so which shortcut was used is unknown.

Claims:

- "A pinned app moved with a keyboard shortcut disappears from the Task Manager" [If I have an app pinned, and move it with a keyboard shortcut - it will disappear.]: confirmed - The Konsole icon is missing at 0006.0, 0007.0 and 0012.0, after it was present at 0005.0.
- "The icon returns after switching desktops" [It comes back only after switching to another virtual desktop or pressing Meta]: confirmed - The icon is back during or after the desktop switch animation (0008.5, 0009.0, 0013.0). Pressing Meta is not shown.
- "It sometimes happens with other apps minimised to tray" [sometimes, it happens with other apps which are minimized to tray.]: not shown - This is the on-screen caption at 0016.0-0018.0. Serein keeps its icon in the visible frames (0022.0, 0026.0, 0030.0, 0032.0), so the failure is not shown for it.
- "The reporter opens Konsole by clicking its pinned icon" [Open Konsole by clicking its pinned icon]: not shown - Clicks are not visible in the frames. Konsole is already open at 0005.0.
