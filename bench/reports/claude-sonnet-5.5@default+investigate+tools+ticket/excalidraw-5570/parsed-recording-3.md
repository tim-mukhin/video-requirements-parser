# real/excalidraw-5570

_claude-sonnet-5.5@default, 23 s; looked at: frames/0009.5.jpg, frames/0012.0.jpg_

On Chrome for Android (excalidraw.com), the context menu for a selected rectangle near the bottom of the canvas opens fully visible and then jumps down. It ends up clipped at the bottom edge, showing only Cut, Copy and Paste. This repeats about every 3.4 s through the 19.9 s video, so the menu cannot be used. The video matches the ticket's 'displayed, then repositioned'.

## Context menu opens fully visible, then is repositioned and clipped at the bottom edge (Chrome, Android)

Class: **intermittent**

Environment: Android phone in portrait, 480x800, status bar 8:52-8:53 AM. Chrome with excalidraw.com in a tab (3 tabs). One rectangle is selected near the bottom of the canvas, above the bottom toolbar. The device model (Pixel 4A) and Chrome version are not visible. No touch marks or cursor are shown.

Steps:

1. With the rectangle selected near the bottom of the canvas, open the context menu (the trigger is not visible, probably a long-press). The full menu (Cut ... Delete, 18 items) appears. (00:01.9; p003)
2. The menu is dismissed or re-laid out. Its items disappear and the strings 'Cut | Copy | Paste' remain, with a clipped menu at the bottom edge. In frame 0012.0 the menu sits at y~705 and only Cut, Copy and Paste are visible. (00:03.6; p005, p008, p024)
3. Repeat: the full menu returns and is clipped again each cycle (full at 9.1 s and 12.9 s, clipped again at 10.6-11.2 s and 14.5-15.2 s). The cycle length is about 3.4 s, and the menu position shifts between frames. (00:09.1; p043, p048, p063, p070, p075, p091)

Expected (implied): The context menu opens once at a stable position that fits the viewport (or can be scrolled), so every item can be reached.

Actual: The full menu appears, then within about 1.7 s it is replaced by a copy placed at the bottom edge with most items off-screen. The cycle repeats and the position shifts between frames. The 'Hold Ctrl to deep select' and 'Press Enter to add text' hints toggle in step with it.

Key events: p003, p008, p024, p043, p048, p063, p070, p075, p099

Missed by the author:

- The cycle repeats many times in 19.9 s rather than once (p003, p043, p070).
- The clipped menu overlaps the bottom toolbar (frame 0012.0).
- The only speech is an unrelated 'Thank you.' (u001).

Claims:

- "The context menu is displayed, then repositioned (Pixel 4A)." [ticket]: confirmed - Frame 0009.5 shows the full menu in place. Frame 0012.0 shows it at the bottom edge with only 3 items visible. The device model is not shown.
- "Problem occurs on Chromium browsers on Android and not on Firefox or Mi browser, and not on Note 8 or iPhone." [ticket]: not shown - Only Chrome on one phone is shown. The browser version and other devices are not visible.
- "Context menu scrolling does not work consistently." [ticket]: not shown - No scroll gesture is visible. The video shows repositioning and clipping only.
