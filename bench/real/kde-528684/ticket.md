# Pinned app disappears from Task Manager when its window is moved to another virtual desktop

Source: https://bugs.kde.org/show_bug.cgi?id=528684  (reporter: <email>, filed 2026-11-11)

[attachment: recording.mp4]
A video showcasing the issue

SUMMARY
When the window of a pinned app is moved to another virtual desktop with a keyboard shortcut, the app disappears completely from the Task Manager instead of going back to being a normal pinned launcher. The icon only comes back after switching virtual desktops or pressing Meta

This is a regression on current git master.

STEPS TO REPRODUCE
1. Use the Icons-Only Task Manager with at least one pinned app, e.g. Konsole.
2. Have at least two virtual desktops.
3. Open Konsole by clicking its pinned icon.
4. Move the Konsole window to another virtual desktop with a keyboard shortcut (e.g. "Window to Next Desktop").

OBSERVED RESULT
The Konsole icon disappears from the Task Manager completely. It comes back only after switching to another virtual desktop or pressing Meta.

EXPECTED RESULT
The Konsole icon stays in the Task Manager as a normal pinned launcher, because its window is no longer on the current desktop.

SOFTWARE/OS VERSIONS
Operating System: KDE Linux 2026-11-09
KDE Plasma Version: 6.8.80
KDE Frameworks Version: 6.33.0
Qt Version: 6.12.0
Kernel Version: 7.2.11-arch1-1 (64-bit)
Graphics Platform: Wayland
Graphics Processor: Intel Iris Xe Graphics
