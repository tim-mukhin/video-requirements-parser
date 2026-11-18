# real/kde-528737

_gpt-6-sol@default, 34 s; looked at: frames/0007.0.jpg, frames/0008.0.jpg, frames/0009.5.jpg, frames/0011.5.jpg, frames/0014.0.jpg, frames/0016.0.jpg, frames/moments/p060.jpg, frames/moments/p063.jpg, frames/moments/p071.jpg, frames/moments/p072.jpg, frames/moments/p088.jpg, frames/0008.5.jpg, frames/0009.0.jpg, frames/0010.0.jpg, frames/0011.0.jpg, frames/moments/p069.jpg, frames/moments/p086.jpg_

In Dolphin's Columns view, a folder containing a very long filename expands to occupy nearly the whole window, hiding its child-folder column. After horizontal scrolling reveals that column, clicking a child folder shifts the columns but does not open it.

## Long filename hides the next column and child-folder click only repositions it

Class: **silent-fail**

Environment: Dolphin in Columns view, browsing /tmp/bug report/ on a Linux desktop. The ticket reports Arch Linux, Plasma 6.8.2, Wayland and Dolphin 27.03.70; those versions are not visible in the video.

Steps:

1. In Columns view, open the existing /tmp/bug report/ folder. (00:03.0; p026, p030)
2. Click sub folder beside the long-named file. (00:06.7; p051, p053, p054)
3. Move the bottom horizontal scrollbar right to reveal the child folders. (00:08.4; p060, p061, p062)
4. Click compact in the revealed column. (00:09.4; p068, p069, p070)

Expected (implied): Keep the child-folder column visible without excessive scrolling, and open the child folder when clicked.

Actual: Opening sub folder leaves its child folders off-screen while the column containing the long filename fills the view. Clicking compact after scrolling shifts the child-folder column to the left, but the path remains /tmp/bug report/sub folder/ and compact does not open. After the window is resized, narrower columns show both the long-named file and the child folders.

Key events: p051, p053, p060, p062, p068, p069, p070, p089

Missed by the author:

- The filename is already middle-ellipsized before resizing; the oversized column is the visible issue [p053, p063].
- The video records a click on compact, not icons; pointing at icons beforehand is not evidence of a click [p065, p068].

Claims:

- "A roughly 200-character file was created for this reproduction." [ticket: STEPS TO REPRODUCE 1]: not shown - The long-named file is visible, but its creation and exact length are not shown.
- "The current folder fills the screen and hides the next layer." [ticket: OBSERVED RESULT]: confirmed - The child folders are absent after opening sub folder [p053] and appear after horizontal scrolling [p062].
- "Clicking another folder after scrolling shifts the column rather than opening it." [ticket: OBSERVED RESULT]: confirmed - The recorded click is on compact [p068]; the columns shift [p069, p070] while the path remains unchanged.
- "The long name is not truncated until the window is resized." [ticket: title and OBSERVED RESULT]: refuted - The filename already contains a middle ellipsis before resizing [p053, p063]. Resizing produces a shorter display and narrower columns [p089].
