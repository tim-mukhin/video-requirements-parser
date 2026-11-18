# real/kde-528737

_claude-sonnet-5.5@default, 31 s; looked at: frames/000205.jpg, frames/000722.jpg, frames/001158.jpg, frames/000510.jpg, frames/000565.jpg, frames/000405.jpg_

A silent screen recording of Dolphin (KDE) in Columns view, browsing /tmp → bug report → sub folder. A folder that contains a file with a very long name makes its column about as wide as the window, pushing sibling columns off-screen and forcing horizontal scrolling. Later the same long name is elided to a normal column width. The author never says what the problem is, so this is the most likely candidate, not a confirmed one.

## Dolphin Columns view: a very long filename makes the column nearly window-wide and pushes the other columns out of view

Class: **wrong-data**

Environment: Dolphin file manager (KDE), Columns view, window titled 'home' then 'tmp', 'bug report' and 'sub folder'. Folders: /tmp/bug report/ holds 'sub folder' and a file named 'Lorem Ipsum is simply dummy text…' (0 B). /tmp/bug report/sub folder/ holds 3 folders named 'compact', 'detials' and 'icons'. 1920×1080. No audio.

Steps:

1. In Dolphin's Home view, click an entry in the left column to navigate to /tmp. (00:01.6; p005, p008)
2. Click the 'bug report' folder. The next column opens showing 'sub folder' and a file with a very long Lorem Ipsum name. (00:03.0; p026, p030)
3. Click the long-named file and then the folder area several times. The columns jump and flicker between /tmp/bug report/ and the long-name column. (00:04.6; p036, p041, p045)
4. Click 'sub folder' at the top right. The folder opens (path /tmp/bug report/sub folder/). The long-name column is now almost the full window width and the 'sub folder' column holding compact/detials/icons sits at the far right, behind a horizontal scrollbar. (00:06.7; p051, p052, p053)
5. Click the horizontal scrollbar at the bottom. The view scrolls to the right edge, shows only the tail of the long filename text, and the list of the 3 sub folders. (00:08.4; p060, p068, p071)
6. Click 'compact', 'detials' and 'icons'. Each is an empty folder, shown as '3 folders'. (00:09.4; p067, p082)
7. After 15.7 s, all columns are visible at the same time, and the long filename is now elided in the middle ('t...rarian'). The window is also about 28 px narrower than before. (00:15.7; p088)

Expected (implied): Each column in Columns view keeps a reasonable width, so the path (/tmp → bug report → sub folder) stays visible without horizontal scrolling. Long names are elided, as they are in the final frame.

Actual: While browsing, the column holding the long-named file is drawn at almost the full window width with the whole name unelided (frames/000405.jpg). The parent columns scroll off to the left and the 'sub folder' column to the right (frames/000510.jpg). The layout jumps and flickers between states (many FLASHED and CHANGED events between 00:02 and 00:09). Only later (frames/000944.jpg, frames/001158.jpg) are all columns shown with the long name elided.

Key events: p035, p052, p053, p068, p070, p071, p088

Missed by the author:

- The video has no speech, so nothing is said. Between 00:04 and 00:06.5 the file list flashes in and out (p035, p038–p044, p046–p050) while the author is only clicking.
- The window geometry changes at the end. The right edge moves from about x=1900 to about x=1873 (frames/000722.jpg vs frames/001158.jpg, s062–s064).
- The sub folders are spelled 'detials' (p065, p076). This is a typo in the test data, not an app bug.
