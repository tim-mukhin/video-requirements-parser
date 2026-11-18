# real/gshell-6725

_claude-sonnet-5.5@default, 32 s; looked at: frames, frames/0000.0.jpg, frames/0001.0.jpg, frames/0002.0.jpg, frames/0003.0.jpg, frames/0004.0.jpg, frames/0005.0.jpg, frames/0006.0.jpg, frames/0008.0.jpg, frames/0009.5.jpg, frames/0002.5.jpg, frames/0001.5.jpg, frames/0005.5.jpg, frames/0009.0.jpg_

In GNOME Shell, the user opens the Overview and types a search for "calc"/"cal", then presses Enter (inferred). The app that opens is Celluloid, which was the selected result for the earlier partial query, not Calculator. This matches the ticket: the launched app is out of sync with the visible search state.

## Enter in Overview search launches the result of an earlier, partial query (Celluloid) instead of the currently selected result

Class: **wrong-data**

Environment: GNOME Shell on Wayland (per ticket: 44.1, Fedora Silverblue 38), Overview search, screen recording at 19:06 on Sat 27 May. Apps seen: Celluloid, Calculator and others in the dock and results.

Steps:

1. Desktop is empty, with no windows open. (00:00.0; 0000.0)
2. Open the Overview (inferred: Super key or Activities). The search field shows "Type to search". (00:01.5; 0001.5)
3. Type quickly. The field shows "ca" and the first selected result is Celluloid, with Calculator second. (00:02.0; 0002.0)
4. Press Enter (inferred; the keypress is not visible). Celluloid starts, and its name appears in the top bar at 2.5 s. (00:02.5; 0002.5, 0003.0)
5. Celluloid opens and a loading spinner appears in the top bar. (00:03.0; 0003.0, 0004.0)
6. Open the Overview again and type a new search. The field shows "c" with "Searching..." and no results. (00:05.0; 0005.0)
7. The field shows "cal" and Calculator is selected as the first result. (00:05.5; 0005.5)
8. Press Enter (inferred). The Overview closes, Calculator never appears, and Celluloid's launch spinner is still in the top bar. (00:06.0; 0006.0, 0008.0, 0009.5)

Expected (implied): Enter launches the application that is currently selected in the search results (Calculator for "cal"/"calc").

Actual: In the first attempt Enter launched Celluloid, the first result for the partial query "ca". In the second attempt the Overview closed after "cal" with Calculator selected, and no Calculator window appeared in the remaining frames. The Celluloid spinner stayed in the top bar. Whether Enter launched a stale result or nothing is not visible.

Key events: 0002.0, 0002.5, 0003.0, 0005.5, 0006.0

Missed by the author:

- After the second search ("cal", Calculator selected at 5.5) the Overview closes at 6.0, but Calculator never opens through 9.5. Only the Celluloid spinner is visible (6.0–9.5).
- At 5.0 the Overview shows "Searching..." with an empty result area after the first letter, so results lag behind typing (0005.0).

Claims:

- "Typing quickly makes Enter open a result from an earlier query." [when I press the Enter key, Celluloid still opens!]: confirmed - At 2.0 the field shows "ca" and Celluloid is selected. At 2.5–3.0 Celluloid opens. The video does not show the moment of the keypress or a final "calc" query, so the stale-result cause is inferred.
- "The on-screen search results are correct while the wrong app opens." [Visually everything is shown correctly]: not shown - The only frame with an updated query ("cal" at 5.5, Calculator selected) is followed by the Overview closing with no Calculator window. The first attempt does not show the final query before Enter.
- "The ticket's first example is that typing "c" selects Celluloid." [if I type "c", I get Celluloid appearing as the first/selcted search result]: confirmed - In the video, "ca" has Celluloid selected, and "cal" has Calculator selected.
