# real/excalidraw-5570

_claude-sonnet-5.5@default, 25 s; looked at: frames/0001.0.jpg, frames/0010.0.jpg, frames/0013.0.jpg_

On a phone in Chrome (Pixel 4A per the ticket), the Excalidraw context menu for a selected circle opens at a position that does not fit the screen and is then repositioned. Its first position is clipped at the right edge, and a later one is clipped at the bottom with Lock and Delete unreachable. The video shows a menu clipped and moving between openings. It does not show scrolling.

## Context menu opens clipped at screen edges and is repositioned after opening on Android Chrome

Class: **intermittent**

Environment: Android phone, portrait 996x2160, Chrome, excalidraw.com (12 tabs), mobile layout with a bottom action bar, one hand-drawn circle on the canvas. The device model and Chrome version are not visible (the ticket says Pixel 4A, Chrome 104).

Steps:

1. Circle is selected. A CLICK/touch at [701,77] is recorded, then the object context menu opens (Cut ... Delete). Its left edge is near x=675, so its right side is cut off by the screen edge. (00:00.7; p001, p004, p005)
2. The menu is still shown, then disappears around 3.3 s. Circle selection is lost, and about 0.7 s later (04.0) a different menu appears, the canvas menu (Paste, Select all, Show grid, Zen mode, View mode), also reaching the right screen edge. (00:03.3; p009, p016, p017)
3. The canvas menu is dismissed. The circle then appears selected near the right screen edge (8-10 s). The frame at 10.0 s shows no menu. (00:05.9; p020, p026)
4. The object menu opens again at 11.2 s, reaching the right edge, and changes at 11.5 s. At 13.0 s it is at a new position, lower and further left, and cut off at the bottom: the Lock row is half visible and Delete is out of view. (00:11.2; p043, p044, p046)
5. Repeat: the menu is closed and opened again at 14.6 s. The last entry is read as 'Elin vertical' at 14.9 s, so the menu is cut or changing at the bottom. (00:14.6; p047, p055, p056)

Expected (implied): The context menu opens fully inside the viewport, or is scrollable, in a stable position next to the touch point, so that all items including Delete can be reached.

Actual: Menus are clipped at the right edge (frame 0001.0: Delete and the right part of the items cut off) and at the bottom (frame 0013.0: Lock and Delete cut off). The position changes between and within openings. No scroll gesture is shown, so scrollability is not demonstrated.

Key events: p004, p005, p016, p017, p043, p044, p055, p056

Missed by the author:

- The first menu is clipped at the right edge from its first appearance (p005, frame 0001.0).
- The object menu is replaced by the canvas menu around 3.3-4.0 s and the circle is deselected (p009, p016).
- The menu is clipped at the bottom with Lock and Delete cut off (frame 0013.0, p056).
- The watcher's claim of a menu at 10.0 s is wrong: that frame shows no menu.

Claims:

- "The context menu is displayed, then repositioned (Pixel 4A)" [ticket]: confirmed - The menu changes between 11.2 s (p043) and 11.5 s (p044) and its position differs by 13.0 s. The frames show different positions across openings.
- "Context menu scrolling does not work consistently" [ticket]: not shown - No scroll gesture appears in the video; only clipping and repositioning are visible.
- "OK on Note 8 and iPhone, and on Firefox/Mi Browser but not Chromium" [ticket]: not shown - The video shows one device. The device model and browser version are not visible.
