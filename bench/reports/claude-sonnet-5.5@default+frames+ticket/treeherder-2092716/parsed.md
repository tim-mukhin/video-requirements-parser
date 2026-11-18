# real/treeherder-2092716

_claude-sonnet-5.5@default, 20 s; looked at: frames, frames/0000.0.jpg, frames/0002.0.jpg, frames/0003.0.jpg, frames/0004.0.jpg, frames/0005.0.jpg, frames/0006.0.jpg, frames/0007.5.jpg_

In TreeHerder's Failure Summary panel, gray icon buttons (the alert/file-bug button, the pin button and the bug button) lose their icons while the mouse hovers over them. The button turns light and the icon becomes white or invisible. The icon comes back when the pointer leaves.

## Icons in Failure Summary buttons disappear on hover

Class: **wrong-data**

Environment: TreeHerder (treeherder.mozilla.org) in a browser. The bottom panel is on the Failure Summary tab, with an AssertionError: in-tree files should pass the linter failure. The tooltip reads 'File an internal issue for this failure'. The browser and color scheme are not visible.

Steps:

1. Failure Summary tab is open with a failure selected. All buttons show their icons: alert, pin and bug. (00:00.0; 0000.0)
2. Hover the alert/file-issue button at the top left of the failure line. Its icon disappears and the tooltip 'File an internal issue for this failure' appears. (00:02.0; 0002.0)
3. Hover the pin (thumbtack) button on the failure line below. Its icon disappears and the button looks blank. (00:03.0; 0003.0)
4. Move the pointer away from the buttons. The icons are visible again. (00:04.0; 0004.0)
5. Hover the bug button on the right. Its icon disappears and the tooltip appears. (00:05.0; 0005.0, 0006.0)
6. Move the pointer away. The icon is back. (00:07.5; 0007.5)

Expected (implied): The button icon stays visible while hovering.

Actual: The icon vanishes (it turns white on a light hover background) for as long as the pointer is over the button. It reappears when the pointer leaves.

Key events: 0002.0, 0003.0, 0005.0, 0000.0

Missed by the author:

- The pin button in the nested failure line also loses its icon on hover (0003.0), not just the top-level buttons.
- The clipboard and log buttons were not hovered, so the video does not show whether they are affected.

Claims:

- "The icon disappears while hovering a gray button such as file-bug or pin" [The icon disappears while you're hovering the button.]: confirmed - The alert, pin and bug buttons all lose their icons on hover (0002.0, 0003.0, 0005.0). Each icon is visible without hover (0000.0, 0004.0).
- "Reproduces in Chrome and Firefox, and in both color schemes" [This happens in Chrome as well as Firefox, regardless of color scheme.]: not shown - The video shows one browser and one theme, and the frames do not identify the browser.
- "Click a red or orange task first" [Click some red or orange task.]: not shown - The video starts with a failure already selected.
