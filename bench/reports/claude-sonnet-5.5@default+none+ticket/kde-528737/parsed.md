# real/kde-528737

_claude-sonnet-5.5@default, 15 s; looked at: nothing_

In Dolphin's Columns view, a folder containing an item with a very long name (~200 characters) is not truncated. The column grows to fill the window and the next column is pushed out of view. Clicking another folder only scrolls the column into view instead of opening it. Resizing the window makes the name truncate and the view behave normally, so the view is hard to use until the user resizes.

## Dolphin Columns view: very long file names are not truncated, column fills the screen and blocks navigation

Class: **wrong-data**

Environment: Dolphin 27.03.70 in Columns view, KDE Plasma 6.8.2 on Arch Linux (Wayland), KDE Frameworks 6.32.0, Qt 6.12.0. No accounts or organizations involved. The video was not available, so only the ticket text was used.

Steps:

1. Create a file with a ~200-character name inside a nested folder structure that has further subfolders. (00:00.0; )
2. In Dolphin's Columns view, navigate to the folder that contains the long-named file. (00:00.0; )
3. Click one of the subfolders in that folder. (00:00.0; )

Expected (implied): The long name is truncated in the column, as it is after a window resize, so columns keep a normal width and the next column stays visible. The reporter is unsure of the exact intended behavior.

Actual: The current folder's column fills the whole window and the next column is not visible. After scrolling the view a little and clicking another folder, that folder does not open. The column just scrolls to fit the window. Resizing the window truncates the long name and the view then looks normal.

Key events: 

Claims:

- "Resizing the window truncates the long name and gives a normal-looking view." [Resizing the window in this state truncates the really long name and shows a much more normal view.]: not shown - No video was available, so this could not be checked.
- "Clicking another folder after scrolling does not open it, but scrolls the column to fit the window." [clicking on another folder doesn't open it, but scoots the column to fit the window]: not shown - No video was available, so this could not be checked.
