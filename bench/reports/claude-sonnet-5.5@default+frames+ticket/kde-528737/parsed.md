# real/kde-528737

_claude-sonnet-5.5@default, 31 s; looked at: frames, frames/0000.0.jpg, frames/0003.0.jpg, frames/0006.0.jpg, frames/0009.0.jpg, frames/0012.0.jpg, frames/0015.0.jpg, frames/0018.0.jpg, frames/0020.0.jpg, frames/0004.5.jpg, frames/0007.5.jpg, frames/0010.5.jpg, frames/0016.5.jpg, frames/0005.0.jpg_

In Dolphin's Columns view, a folder holding a file with a very long name makes the column grow to the full window width instead of truncating the name. Opening a subfolder then pushes the newer columns off screen, and the view only returns to a normal truncated layout after the window is resized. The reporter's claim about the resize is confirmed. The claims about the scroll bar and clicking another folder are not shown clearly.

## Columns view: column with a very long file name expands to full width, hides the next columns, and only truncates after a window resize

Class: **wrong-data**

Environment: Dolphin file manager in Columns view, single window, dark theme, KDE. Path /tmp/bug report/sub folder/. /tmp/bug report contains a folder 'sub folder' and a file named 'Lorem Ipsum is simply dummy text...'. The ticket gives Arch Linux, Wayland, Dolphin 27.03.70, Plasma 6.8.2. The video does not show these versions.

Steps:

1. Dolphin is in Columns view at /home/. The user navigates to /tmp (inferred click on 'tmp'). The /tmp column is shown with normal-width names. (00:03.0; 0000.0, 0003.0)
2. The user opens 'bug report' (inferred click). The /tmp column widens to about half the window. The next column shows 'sub folder' and the very long-named file, whose name is cut off at the right window edge, with a horizontal scroll bar at the bottom. (00:04.5; 0004.5, 0005.0)
3. The user clicks 'sub folder' (inferred). The long-name column grows to the full window width and the view scrolls right. The 'sub folder' column holding compact, detials and icons is squeezed at the far right edge. (00:07.5; 0006.0, 0007.5, 0009.0)
4. The view scrolls further right. Only the 'sub folder' column (compact, detials, icons) is visible, with 'compact' selected. All parent columns are scrolled out of view and the path bar reads /tmp/bug report/sub folder/. (00:10.5; 0010.5, 0012.0)
5. The window is resized (inferred from the window buttons shifting left). All columns now fit with truncated names (for example 'pms-1d11bd3c-657a...bc97-09dccdda7ea0' and 'Lorem Ipsum ... took a.'), giving the normal view. (00:15.0; 0015.0, 0016.5)

Expected (implied): Long names are truncated with an ellipsis the whole time. Columns keep a bounded width and the next column stays visible without a resize, matching the layout shown after the resize.

Actual: With a very long file name in the current folder, the column expands to the full window width. The following column is pushed off screen or squeezed, and the view scrolls horizontally. Resizing the window recomputes the layout and shows truncated names.

Key events: 0005.0, 0007.5, 0012.0, 0016.5

Missed by the author:

- The long file name is already cut off at the window edge in the first frame it appears (0004.5).
- The folder 'detials' (misspelled) is a test-data typo and not part of the bug (0009.0).
- The path bar and title say 'sub folder' while the visible content is that folder's children, so the long-name column is scrolled out of view (0012.0).

Claims:

- "The current folder fills the screen and the next layer is not visible" [The current folder fills the screen with the next layer not visible.]: confirmed - At 0007.5 the long-name column spans the whole window. At 0004.5 the next column is cut off at the right edge.
- "Resizing the window truncates the long name and shows a normal view" [Resizing the window in this state truncates the really long name and shows a much more normal view.]: confirmed - At 0015.0–0016.5 the window is narrower, all columns are visible and the long names are truncated with an ellipsis.
- "Clicking another folder after sliding the scroll bar scoots the column instead of opening it" [Sliding the scroll bar a little ways over and clicking on another folder doesn't open it, but scoots the column to fit the window.]: not shown - The frames show the view scrolling right and the pointer hovering over 'icons' at 0009.0. No folder is opened and no click on a second folder is visible.
