# real/treeherder-2092716

_claude-sonnet-5.5@default, 26 s; looked at: frames/0002.5.jpg, frames/0006.0.jpg, frames/0004.0.jpg, frames/000030.jpg_

In TreeHerder's Failure Summary panel, a gray icon button loses its icon while the cursor is over it. The video shows this on the top-left alert button (about 2.2 s) and the bug button at the right (about 5.3–6.9 s). The icon returns when the cursor leaves. This matches the ticket.

## TreeHerder Failure Summary: button icon disappears while the button is hovered

Class: **wrong-data**

Environment: TreeHerder (treeherder.mozilla.org) with a bottom panel on the Failure Summary tab. The failure shown is 'AssertionError: in-tree files should pass the linter' (i2009222 Perma [tier 2] clang-tidy). The video is 510x220 and 8 s long, and has no audio. The browser, color scheme and login state are not visible. The color scheme looks dark (dark tab bar), but that is not confirmed.

Steps:

1. Failure Summary tab is open with a failure already selected. The alert, pin, clipboard, log and bug buttons all show their icons. The video does not show how the failure was selected. (00:00.0; s001)
2. Move the cursor onto the gray alert button at the top left of the failure line. Its icon is gone and the button looks blank (frame 000030.jpg). Cursor position is followed here, but the click is not seen and no click is shown. (00:02.2; p001, p002)
3. Move the cursor off the button. The icon comes back. (00:02.9; p003, s004)
4. Move the cursor onto the bug button at the right of the failure line. A tooltip starting 'File a…' appears. The button is blank, with no icon (frame direct/frames/0006.0.jpg). (00:05.3; p004, p005, p006, p007)
5. Move the cursor away. The icon returns. (00:07.5; p010, s008)

Expected (implied): The icon stays visible while the button is hovered.

Actual: While hovered, the gray button's icon turns white or blank on a light hover background and cannot be seen. It returns after the cursor leaves.

Key events: p002, p003, p007, p010

Missed by the author:

- The tooltip on the bug button starts with 'File a…' (p006). It shows alongside the blank icon.
- The watcher says the pin button lost its icon at 3.0 s. The frames show it visible, so that claim is dropped.

Claims:

- "The icon disappears while hovering a gray button (file-bug, pin)" [ticket]: confirmed - Seen on the alert button (000030.jpg, p002) and the bug button (0006.0.jpg, p007). Both are visible without hover (0002.5.jpg, 0004.0.jpg). The pin button was not shown hovered: the cursor sits beside it at 2.5 s and the icon is visible.
- "It happens in Chrome and Firefox, in both color schemes" [ticket]: not shown - The video shows one browser and one theme, and the browser is not identified.
- "Click a red or orange task first" [ticket]: not shown - The video starts with a failure already selected.
