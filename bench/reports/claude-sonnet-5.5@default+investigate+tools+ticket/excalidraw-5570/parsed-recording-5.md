# real/excalidraw-5570

_claude-sonnet-5.5@default, 27 s; looked at: frames/moments/p034.jpg, frames/moments/p010.jpg, frames/000172.jpg, frames/000190.jpg_

On Chrome for Android, long-pressing a point of a selected arrow opens the canvas context menu. The menu first appears fully visible, shifted up to fit the screen. About 0.7 s later it jumps about 1319 px down to the touch point and is cut off by the bottom edge, hiding items from Add to library through Delete. This matches the ticket's 'displayed, then repositioned' report.

## Context menu on Android Chrome opens fitted on screen, then jumps down to the touch point and is clipped by the screen bottom

Class: **state-revert**

Environment: Android phone (portrait, 1440x3120 recording) with the Chrome browser at excalidraw.com. A multi-point arrow is in point-edit mode with the selection tool active. The Pixel 4A and Chrome 104 named in the ticket are not visible in the video. The screen-recording indicator is on. No audio and no cursor; touch marks are drawn by the recorder.

Steps:

1. An arrow is in point-edit mode (hint 'Select a point to edit...'). A long-press near a point opens the context menu (the trigger is not visible). First instance: the 'Cut...Delete' menu is already on screen at 1.2 s, and the 'Flip vertical' item is clicked at 2.3 s. (00:01.2; p001, p008)
2. The user taps points. The menu is seen briefly at 4.1 s and a tap lands at [949,2483], after which the menu is gone. (00:04.1; p010, p011, p015)
3. A tap lands at [618,2459] on the arrow's point. At 6.1 s the full menu opens, shifted up to y≈1122 so every item from Cut to Delete is visible. (00:06.1; p020, p024)
4. At 6.8 s, in a single frame, the menu moves 71 px left and 1319 px down to the touch point at y≈2441. It is now cut off by the screen bottom, with only Cut through Copy to clipboard as SVG visible. The menu then disappears at about 7.4 s. (00:06.8; p025, p034, p039)
5. Repeat: a tap lands at [636,2456] and the menu opens at 9.3 s. It is a flash of 0.6 s at 11.2 s after a tap at [628,2458]. In both cases the menu is shown only briefly and then dismissed. (00:08.8; p045, p046, p053, p054)

Expected (implied): The menu opens once at a position that fits the viewport (or is scrollable if taller) and stays there until the user dismisses it.

Actual: The menu first opens in a fitted, fully visible position. One frame later (6.8 s) it jumps to the raw touch position and is clipped by the bottom edge, so Delete, Lock, Duplicate and other items are unreachable. The menu then closes within about 0.6 s.

Key events: p024, p025, p034, p039, p054

Missed by the author:

- The jump happens in a single frame with a small leftward shift of 71 px (p034, 6.8 s).
- The clipped menu hides Add to library through Delete, and the menu's lower half sits on top of the bottom toolbar (frame 000190).
- The 'Flip vertical' item is clicked at 2.3 s (p008). This click is part of the opening sequence and not of the bug.

Claims:

- "The context menu is displayed, then repositioned (Pixel 4A)." [ticket]: confirmed - The menu jumps 1319 px down in one frame at 6.8 s (p034), after being fully visible at 6.1 s (p024).
- "Scrolling in the context menu does not work consistently." [ticket title]: not shown - No scroll gesture is visible; the video shows only the position jump and the clipping.
- "The issue appears in Chrome 104 on a Pixel 4A but not on a Note 8, and not in Firefox or Mi browser." [ticket]: not shown - Only one device is recorded. The device model and the Chrome version are not visible.
