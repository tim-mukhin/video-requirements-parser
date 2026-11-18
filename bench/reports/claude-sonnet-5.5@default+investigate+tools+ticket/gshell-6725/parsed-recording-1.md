# real/gshell-6725

_claude-sonnet-5.5@default, 25 s; looked at: frames/0002.0.jpg, frames/0005.5.jpg, frames/0007.0.jpg_

In GNOME Shell's Overview search, Enter does not launch the app the results show as selected. In the first attempt the search field reads "ca" with Celluloid selected, and Celluloid launches. In the second attempt "cal" selects Calculator, the Overview closes, and no Calculator appears in the 10 s video. This matches the ticket's stale-result report, but the keypresses and the exact text at the moment of Enter are not visible.

## Overview search: Enter launches a stale/wrong result (Celluloid) instead of the selected Calculator

Class: **wrong-data**

Environment: GNOME Shell on Wayland (version 44.1 / Fedora Silverblue 38 come from the ticket and are not visible in the video). Overview search, 3840x2160 recording, Sat 27 May 19:06. Dock and results show Celluloid, Calculator, Calendar and other apps. The Overview is empty of windows at the start.

Steps:

1. Open the Overview and type a search; the field shows "ca" with Celluloid selected first and Calculator second (frame 0002.0). The opening and typing are not visible, as the video has no cursor or key input. (00:01.9; p001)
2. Press Enter (the key is not visible). Celluloid launches: its name appears in the top bar and then a Celluloid window. (00:02.4; p002, p003)
3. Repeat: open the Overview and type again. At 5.5 s the field shows "cal" and Calculator is selected first (frame 0005.5). (00:05.4; p008, p009)
4. Press Enter (the key is not visible). The Overview closes. No Calculator window or launch indicator appears; the top bar still shows Celluloid with a spinner through the end (frame 0007.0). (00:05.6; p010, p011, p012)

Expected (implied): Enter launches the application currently shown as selected in the search results (Calculator for "cal").

Actual: In the first attempt Enter launched Celluloid, the selection for the partial query "ca". In the second, Calculator was selected on screen but never opened. The video does not show whether Enter launched a stale result or nothing.

Key events: p001, p002, p003, p008, p009, p010, p011

Missed by the author:

- After the second search the Overview closes with Calculator selected, but Calculator never appears and only the Celluloid spinner stays in the top bar for the remaining ~4 s (p010-p013).
- Search results lag behind typing: at 5.1 s the Overview shows "Searching..." with an empty result area (p008), so a result list can be stale relative to the field.

Claims:

- "GNOME very often opens the wrong search result when typing quickly; Celluloid opens even though Calculator is selected." [ticket]: not shown - The first launch happens with "ca" visible and Celluloid selected, so that screen is consistent. The video does not show the final query before Enter or any key press. In the second attempt Calculator is selected but nothing launches, so no wrong app opens there. 'Very often' cannot be checked from two attempts.
- "Visually everything is shown correctly (search term and selection) while the wrong app opens." [ticket]: not shown - At 5.5 s the screen does show "cal" with Calculator selected, and nothing launches afterwards, which fits a desync. The first attempt's text just before Enter was not captured.
- "This did not happen on Fedora 36 / GNOME 42." [ticket]: not shown - A claim about the past and another version; the video shows only one system.
