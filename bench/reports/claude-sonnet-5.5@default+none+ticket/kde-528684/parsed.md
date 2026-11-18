# real/kde-528684

_claude-sonnet-5.5@default, 13 s; looked at: nothing_

With a pinned app (Konsole) running, moving its window to another virtual desktop via keyboard shortcut makes the icon vanish from the Icons-Only Task Manager. It should remain as a pinned launcher. The icon reappears only after switching desktops or pressing Meta. It is reported as a regression on git master.

## Pinned app disappears from Task Manager when its window is moved to another virtual desktop

Class: **state-revert**

Environment: KDE Linux 2026-11-09, Plasma 6.8.80, Frameworks 6.33.0, Qt 6.12.0, kernel 7.2.11-arch1-1, Wayland, Intel Iris Xe. Icons-Only Task Manager with pinned Konsole, at least two virtual desktops. No account or organization involved.

Steps:

1. Use the Icons-Only Task Manager with at least one pinned app, e.g. Konsole. (00:00.0; )
2. Have at least two virtual desktops. (00:00.0; )
3. Open Konsole by clicking its pinned icon. (00:00.0; )
4. Move the Konsole window to another virtual desktop with a keyboard shortcut (e.g. 'Window to Next Desktop'). (00:00.0; )

Expected (speech): The Konsole icon stays in the Task Manager as a normal pinned launcher, because its window is no longer on the current desktop.

Actual: The Konsole icon disappears from the Task Manager completely. It reappears only after switching virtual desktops or pressing Meta.

Key events: 

Claims:

- "This is a regression on current git master." [This is a regression on current git master.]: not shown - No video or bisect info; the ticket gives no last-good version.
