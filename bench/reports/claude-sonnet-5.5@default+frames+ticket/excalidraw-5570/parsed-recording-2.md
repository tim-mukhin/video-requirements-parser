# real/excalidraw-5570

_claude-sonnet-5.5@default, 28 s; looked at: frames, frames/0000.0.jpg, frames/0002.0.jpg, frames/0004.0.jpg, frames/0006.0.jpg, frames/0008.0.jpg, frames/0010.0.jpg, frames/0012.0.jpg, frames/0014.0.jpg, frames/0016.0.jpg_

On Android Brave/Chromium, a long-press on a selected rectangle near the bottom of the canvas opens the context menu. The menu is cut off by the bottom of the screen, and its position shifts between frames. The bottom items, such as the clipboard options, are not reachable.

## Excalidraw context menu on mobile Chromium is clipped at the bottom and changes position (not scrollable or repositioned consistently)

Class: **wrong-data**

Environment: Android phone, Brave browser (Brave icon in the address bar), excalidraw.com, mobile layout. One rectangle is selected near the bottom of the canvas. Device and browser version are not visible. The ticket says Pixel 4A, but this recording is from a different comment and its device is not identifiable.

Steps:

1. A rectangle is selected at the bottom of the canvas and no menu is shown. (00:00.0; 0000.0)
2. Long-press on the selected shape (inferred; the touch is not visible). The context menu appears with Cut/Copy/Paste, and its lower part runs off the bottom of the screen. (00:02.0; 0002.0)
3. The menu is at a different position: moved up and left, now showing 'Copy to clipboard as PNG'. It is still clipped at the bottom. (00:04.0; 0004.0)
4. The menu is gone (dismissed or closed by the user, inferred). (00:06.0; 0006.0)
5. The menu is opened again and sits at yet another position, further left and lower. (00:08.0; 0008.0)
6. The menu moves again between frames, with x/y offsets that differ from before, and is clipped each time. The last frames repeat the open and close cycle. (00:10.0; 0010.0, 0012.0, 0014.0, 0016.0)

Expected (implied): The context menu opens once, fully inside the visible viewport or scrollable so all items can be reached, and stays at a stable position.

Actual: The menu is cut off by the bottom edge, and the clipped bottom items are never reachable. Its position changes from one frame to the next (for example x≈199 at 2.0 s, x≈214 at 4.0 s, x≈183 at 8.0 s, x≈204 at 10.0 s), so it is repositioned after it appears. It repeatedly appears and disappears.

Key events: 0002.0, 0004.0, 0008.0, 0010.0, 0012.0

Missed by the author:

- The tooltip at the top flips between 'Press Enter to add text' and 'Hold Ctrl to deep select' (0002.0, 0004.0, 0006.0). This suggests repeated pointer events or re-renders while the menu opens and closes.

Claims:

- "The context menu is displayed and then repositioned." [As you can see the context menu is displayed, then repositioned.]: confirmed - The menu's position differs across 0002.0, 0004.0, 0008.0 and 0010.0. This recording is in Brave, not the Pixel 4A video the ticket describes.
- "The problem happens on Chromium-based browsers on Android." [it did appear when using a chromium browser]: not shown - Brave is Chromium-based, which is consistent with the claim. The video does not show the engine version or the comparison with Firefox.
- "The menu scrolling does not work consistently." [context menu scrolling not working consistently]: not shown - No scroll gesture is visible. The only visible evidence is clipping at the bottom of the screen and the menu changing position.
