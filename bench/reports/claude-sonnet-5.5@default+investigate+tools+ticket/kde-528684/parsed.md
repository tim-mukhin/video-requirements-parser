# real/kde-528684

_claude-sonnet-5.5@default, 39 s; looked at: frames/0005.5.jpg, frames/0006.5.jpg, frames/0004.5.jpg, frames/0009.5.jpg, frames/0013.5.jpg, frames/0011.5.jpg, frames/0008.0.jpg, frames/0022.5.jpg_

In the Icons-Only Task Manager, the pinned Konsole icon disappears right after its window is moved to another virtual desktop. It comes back, greyed out like a normal launcher, only after a desktop switch or after the Meta/launcher menu opens. The same thing happens a second time. This was not shown for Serein, a second app that appears to be pinned.

## Pinned Konsole icon vanishes from Task Manager after its window is moved to another virtual desktop

Class: **state-revert**

Environment: KDE Plasma (Wayland per the ticket) with a vertical Icons-Only Task Manager on the left. Pinned icons: file manager, blue asterisk app, Telegram, purple app, Konsole. Serein is shown later. Several virtual desktops, user matthew@kde-linux, clock 12:49-12:50, date 11/10/26. The video has no audio and no visible cursor or keys. The ticket gives Plasma 6.8.80, Frameworks 6.33.0, Qt 6.12.0 and KDE Linux 2026-11-09; none of these is visible in the video.

Steps:

1. Konsole is open on the current desktop (window 'zsh — Konsole', 'Size: 90 x 28' overlay). Its pinned icon is in the Task Manager, shown highlighted as an open window (frame 0004.5). The click that launched it is not visible. (00:04.4; p044, p046)
2. The Konsole window disappears from this desktop (the trigger is not visible; the ticket says a 'Window to Next Desktop' shortcut). At the same time the Konsole icon disappears from the Task Manager, leaving only four icons (frames 0005.5, 0006.0, 0006.5). (00:05.2; p047, p056, p067, p068)
3. After a desktop switch the Konsole icon is back in the Task Manager, greyed out, with no window on this desktop (frames 0009.0, 0009.5). The Konsole window with its tooltip is seen on the other desktop (frame 0008.0, p069, p072). (00:09.0; p069, p071, p072)
4. Repeat: the Konsole window leaves again. The icon is gone again (four icons only, frame 0011.5). It returns greyed out after the Meta/launcher menu opens and closes (frame 0013.5). (00:11.4; p073, p074, p075, p076, p077)

Expected (implied): After the window moves to another desktop, the Konsole icon should stay in the Task Manager as a normal pinned launcher.

Actual: The Konsole icon vanishes completely while its window is on another desktop. It reappears (greyed out) only after a desktop switch or after the Meta menu opens. This happens in both moves shown.

Key events: p056, p067, p068, p071, p073, p074, p075, p076, p077

Missed by the author:

- The icon returns greyed out, as a normal launcher should look (frames 0009.5, 0013.5). Only the period right after the move is wrong.
- The first reappearance is during a desktop switch. The Konsole window and tooltip are seen on the other desktop at 8.0 s (p069, p072).
- The second reappearance coincides with the Meta/launcher menu opening at 12.3 s (p076), which matches the ticket's 'pressing Meta' workaround.
- The video shows no shortcut overlay, so the exact shortcut used is unknown.

Claims:

- "A pinned app moved with a keyboard shortcut disappears from the Task Manager (ticket; on-screen caption 'If I have an app pinned, and move it with a keyboard shortcut - it will disappear')" [ticket / caption at 0:00]: confirmed - The Konsole icon is present at 4.5 s, absent at 5.5-6.5 s and at 11.5 s, after the window left. This is shown for Konsole only.
- "The icon returns only after switching to another virtual desktop or pressing Meta" [ticket]: confirmed - The icon is back at 9.0-9.5 s after a desktop change, and at 13.0-13.5 s right after the Meta menu appears at 12.3 s. The Meta key press itself is not visible.
- "Konsole was opened by clicking its pinned icon" [ticket]: not shown - No clicks are visible. Konsole is already open when it first appears at 4.4 s.
- "It sometimes happens with other apps that are minimized to tray (on-screen caption)" [caption 0:15-0:19]: not shown - Serein's icon is visible in the Task Manager after its window action (frame 0022.5), so the video does not show the failure for it.
- "It is a regression on current git master" [ticket]: not shown - The video has no version information and no earlier behaviour to compare.
