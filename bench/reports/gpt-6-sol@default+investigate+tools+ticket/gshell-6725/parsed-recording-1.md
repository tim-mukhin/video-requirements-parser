# real/gshell-6725

_gpt-6-sol@default, 39 s; looked at: frames/moments/p005.jpg, frames/0002.0.jpg, frames/0005.5.jpg, frames/0006.0.jpg, frames/000165.jpg, frames/0002.5.jpg, frames/0003.0.jpg, frames/0004.0.jpg, frames/0006.5.jpg, frames/0009.5.jpg, frames/0005.0.jpg, frames/0001.5.jpg, frames/000169.jpg, frames/000207.jpg_

GNOME search highlights Calculator for the visible query “cal”, but the Overview closes without showing Calculator; the top bar continues to show Celluloid. This matters because the result presented as selected does not match the apparent launch outcome, although the recording does not show the key press or prove that a new Celluloid window opened.

## Selected Calculator search result does not open after rapid search

Class: **silent-fail**

Environment: GNOME Shell Overview with Calculator and Celluloid. The ticket reports GNOME Shell 44.1, Fedora Silverblue 38.20230509.0 and Wayland; the video does not verify those versions or the session type.

Steps:

1. Open the Overview (the trigger is not visible). (00:05.1; p008)
2. Enter the search query until “cal” is visible and Calculator is highlighted; typing is not visible. (00:05.4; p009)
3. Submit the search as described in the ticket; the Enter key is not visible, but the Overview closes. (00:05.6; p010)

Expected (implied): Submitting the search opens the highlighted Calculator result.

Actual: Calculator does not appear. Celluloid is named in the top bar with a loading indicator after the Overview closes, while only the desktop is visible through the end of the video [p010, p011, p012]. The earlier search had Celluloid highlighted and then visibly opened its window [p001, p002, p003]; that attempt is not a selection mismatch.

Key events: p001, p002, p003, p005, p008, p009, p010, p011, p012

Missed by the author:

- The first attempt shows Celluloid selected before its window opens, so it is a contrast rather than evidence of a wrong selection [p001, p002, p003].
- The Celluloid window disappears before the second search; the brief transition marked at p005 is not an error message. The later Celluloid label alone does not establish a newly opened window [p005, p009, p010].

Claims:

- "The selected Calculator result is not the application shown after submitting the search." [ticket: What happened]: confirmed - The frame at p009 shows Calculator highlighted; subsequent frames show the desktop and Celluloid in the top bar, not Calculator. They do not establish whether Celluloid was launched anew.
- "The search field shows the complete term “calc” before Enter." [ticket: Bug summary]: not shown - The available frames show “ca” on the first attempt and “cal” with Calculator highlighted on the second, not “calc”.
- "Celluloid opens despite Calculator being selected." [ticket: Bug summary]: not shown - Celluloid is shown in the top bar after the second search, but its window had already opened during the first attempt and no new Celluloid window is shown after the second.
- "This happens often and did not happen on Fedora Silverblue 36." [ticket: Affected version and Bug summary]: not shown - This ten-second recording cannot establish frequency or behavior on another release.
