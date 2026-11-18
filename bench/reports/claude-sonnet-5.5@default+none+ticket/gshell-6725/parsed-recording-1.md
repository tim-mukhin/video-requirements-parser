# real/gshell-6725

_claude-sonnet-5.5@default, 14 s; looked at: nothing_

In GNOME Shell 44.1 on Wayland, typing a search term quickly in the Overview and pressing Enter opens a stale result from an earlier query (e.g. Celluloid instead of Calculator). The on-screen selection is correct, so users must type slowly to avoid launching the wrong app. The reporter says this is a regression from GNOME 42.

## Overview search launches previous query's result when typing quickly

Class: **wrong-data**

Environment: GNOME Shell 44.1, Fedora Silverblue 38.20230509.0, Wayland. Single user; no accounts or organizations. The ticket does not say whether the bug is tied to specific hardware or to the number of installed apps.

Steps:

1. Open the Overview. (00:00.0; )
2. Type one letter (e.g. 'c'); Celluloid is shown as the selected first result. (00:00.0; )
3. Quickly type the rest of the term ('alc' to make 'calc'); the search field and results show Calculator selected. (00:00.0; )
4. Press Enter right away. (00:00.0; )
5. Alternative path: open the Overview, quickly type a full search term and press Enter. (00:00.0; )

Expected (speech): The app shown as selected (Calculator) opens.

Actual: The app from the earlier, stale search result (Celluloid) opens, although the UI shows the new results correctly.

Key events: 

Claims:

- "Regression: did not happen on Fedora Silverblue 36 (believed to be GNOME 42)." [I did not experience this bug when using Fedora Silverblue 36, which I believe was running GNOME 42.]: not shown - No video. The reporter is unsure of the GNOME version, and no comparison was provided.
- "The bug is easily reproducible and happens often." [This is very easily reproducible for me, and happens often enough to be frustrating.]: not shown - No recording was available to check. The reporter gives no exact frequency, so the class could also be 'intermittent'.
- "GNOME acts on older, out-of-sync search results." [It's like GNOME is delayed and acting on the older search results.]: not shown - This is the reporter's guess at the cause. It has not been checked.
