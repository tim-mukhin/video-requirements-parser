# real/kde-528737

_claude-sonnet-5.5@default, 25 s; looked at: frames/0007.5.jpg, frames/0016.5.jpg_

In Dolphin's Columns view, a folder containing a file with a very long name gets a column as wide as the window, and the long name is not elided. Opening 'sub folder' scrolls the view right, so only the child column is visible and the parent columns are off screen. After the window changes size, around 15.2–15.7 s, the same columns appear at bounded width with the name elided. This matches the ticket.

## Columns view: column with a very long file name expands to full window width, hides neighbouring columns, and is only truncated after a window resize

Class: **wrong-data**

Environment: Dolphin, Columns view, dark theme, single window, 1920x1080 recording. Path /tmp/bug report/sub folder/. 'bug report' contains the folder 'sub folder' and a file named 'Lorem Ipsum is simply dummy text...'. 'sub folder' contains compact, detials and icons. The versions in the ticket (Arch, Plasma 6.8.2, Dolphin 27.03.70) are not visible in the video.

Steps:

1. Click 'tmp' in the root column. The /tmp column opens with normally elided names. (00:01.6; p005, p008)
2. Click 'bug report'. Its column shows 'sub folder' and the long-named file. The title becomes 'bug report'. (00:03.0; p026, p030)
3. Click 'sub folder' (the click is at [1149,145]). The path becomes /tmp/bug report/sub folder/. The long-name column spans the whole window with the name unelided to the right edge, and the view scrolls right (a horizontal scroll bar appears). The other columns are off screen. Frame 0007.5 shows this. (00:06.7; p051, p052, p053, p055, p060)
4. Only the 'sub folder' column (compact, detials, icons) is reachable. The author clicks 'compact' and hovers the items. The two clicks near the bottom of the window ([1090,1020] and the 'compact' click) do not obviously open a column. The ticket's 'scoots instead of opening' behaviour is not clearly shown. (00:08.4; p061, p065, p068, p069)
5. The window is resized (the trigger is not visible: the cursor is not followed 14.8–16.1 s). All columns now fit, and the names are elided ('pms-1d11bd3c-657a...bc97-...', 'Lorem Ipsum ... took a.'). Frame 0016.5 shows this. (00:15.7; p089)

Expected (implied): Long names are elided with an ellipsis and column widths stay bounded, so the next column stays visible without a resize. This is the layout shown after the resize.

Actual: While the long-named file is in the current folder, its column grows to the full window width and the name is not elided. Navigating into the sub folder scrolls the view so that only the child column is visible. Only the window resize recomputes the layout with elided names.

Key events: p035, p052, p055, p060, p069, p089

Missed by the author:

- The video has no speech. The long name is already cut off at the window edge in the first frame where it appears, before any subfolder is opened (p035, about 4.3 s).
- The path bar and title say 'sub folder' while the visible content is that folder's children, so the user loses the parent context (p053, p054).

Claims:

- "The current folder fills the screen and the next layer is not visible." [ticket]: confirmed - At about 7.5 s the long-name column spans the window, and in the 7.2–15 s span the other columns are scrolled out of view.
- "Resizing the window truncates the long name and gives a normal view." [ticket]: confirmed - At 16.5 s all columns are visible and the long name is elided with '...'.
- "Sliding the scroll bar and clicking another folder does not open it but scoots the column to fit the window." [ticket]: not shown - The view scrolls right and the author clicks 'compact' and 'detials', but no clear click-then-scoot sequence is visible. The cursor is also not followed at 14.8–16.1 s.
- "The file name is about 200 characters, in a nested folder." [ticket]: confirmed - The file is in /tmp/bug report/, which contains 'sub folder'. The visible name is very long.
