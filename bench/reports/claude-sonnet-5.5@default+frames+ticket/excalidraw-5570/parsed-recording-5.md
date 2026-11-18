# real/excalidraw-5570

_claude-sonnet-5.5@default, 36 s; looked at: frames, frames/0000.0.jpg, frames/0002.0.jpg, frames/0004.0.jpg, frames/0006.0.jpg, frames/0008.0.jpg, frames/0010.0.jpg, frames/0012.0.jpg, frames/0005.0.jpg, frames/0005.5.jpg, frames/0011.0.jpg, frames/0006.5.jpg_

On Chrome for Android, a long-press on a selected arrow's point opens the canvas context menu. The menu is not stable: it appears fully open in one frame and in the next sits low on the screen, cut off by the bottom edge. The clipped menu hides Delete and the rest of the items. This matches the ticket's 'displayed, then repositioned' report.

## Context menu jumps between a full-height position and a position clipped by the bottom of the screen (Chrome, Android)

Class: **intermittent**

Environment: Android phone (Pixel 4A per the ticket; the video does not show the device model), Chrome, excalidraw.com, portrait. A linear/arrow element is in point-editing mode with three points and the selection tool active. The screen recording indicator is visible.

Steps:

1. An arrow with three editable points is already selected in point-edit mode (hint 'Press Delete to remove point(s)...'). Start of the recording. (00:00.0; 0000.0)
2. Tap or touch points on the arrow. A faint touch-ripple circle appears and the hint text changes between 'Select a point to edit...' and 'Press Delete to remove point(s)...'. This is inferred from the ripple circles and hint changes. (00:02.0; 0002.0, 0004.0, 0005.0)
3. Long-press near the arrow. The context menu opens fully, positioned up the screen with every item visible, from Cut down to Delete. (00:05.5; 0005.5)
4. Half a second later the menu is anchored low and clipped by the screen bottom. Only Cut, Copy, Paste and the two clipboard items are visible, and the rest is cut off. Next frame (6.5 s) the menu is gone. (00:06.0; 0006.0, 0006.5)
5. Repeat the long-press with the middle point selected. The menu is full-height again at 11.0 s and clipped at the bottom at 12.0 s. (00:11.0; 0011.0, 0012.0)

Expected (implied): The context menu opens once at a position that fits on screen, or is scrollable if taller than the viewport, and stays there.

Actual: The menu's position changes between frames. It is shown fully in one frame, and in another it is placed at the bottom of the screen with its lower items (Copy styles through Delete) off-screen. The ticket says it cannot be scrolled.

Key events: 0005.5, 0006.0, 0011.0, 0012.0

Missed by the author:

- The clipped menu hides Delete, Duplicate and Lock, so some actions are unreachable without scrolling (0006.0, 0012.0).
- The menu x-position also shifts slightly between frames (about 418 px at 0005.5, 409 px at 0011.0), as does the ripple circle (0006.0, 0012.0).

Claims:

- "The context menu is displayed, then repositioned (Pixel 4A)." [As you can see the context menu is displayed, then repositioned.]: confirmed - The menu changes position between 5.5 s and 6.0 s, and between 11.0 s and 12.0 s. The video cannot show which of the two positions comes first.
- "Scrolling inside the context menu does not work consistently." [context menu scrolling not working consistently on Android]: not shown - No scroll gesture is visible in the frames. The video only shows the clipped placement and the position change.
- "The same Chrome version appears on the Note 8 and the Pixel 4A, and Firefox and Mi browser are unaffected." [the browser was the same Chrome version: 104.0.5112.69]: not shown - Only one device is recorded. The Chrome version and the device model are not visible.
