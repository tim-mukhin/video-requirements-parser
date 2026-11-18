# real/gshell-6725

_claude-sonnet-5.5@default, 16 s; looked at: nothing_

In GNOME Shell 44.1, typing a search term quickly in the Overview and pressing Enter opens the application from an earlier, stale result set (e.g. Celluloid) instead of the one shown as selected (e.g. Calculator). The display is correct but the activation is wrong, so users must type slowly to launch the right app. The ticket says this is a regression from GNOME 42.

## Overview search activates a stale result instead of the selected one when typing quickly

Class: **wrong-data**

Environment: GNOME Shell 44.1 on Wayland, Fedora Silverblue 38.20230509.0. Overview app search. The reporter did not see this on Silverblue 36, which they believe ran GNOME 42. No accounts or organizations involved.

Steps:

1. Open the Overview. (00:00.0; )
2. Type one letter of the search term, e.g. 'c'. Celluloid is shown as the first and selected result. (00:00.0; )
3. Quickly type the rest of the term, e.g. 'alc' to make 'calc'. The search field shows 'calc' and Calculator is shown as the selected result. (00:00.0; )
4. Press Enter right away. (00:00.0; )
5. Alternative: open the Overview, type a whole search term quickly and press Enter. (00:00.0; )

Expected (speech): Pressing Enter opens the result that is shown as selected (Calculator).

Actual: Celluloid, the result for the earlier partial query 'c', opens instead of Calculator. The on-screen results and search text are correct, but Enter activates the older result.

Key events: 

Claims:

- "The bug did not occur on Fedora Silverblue 36 (believed to be GNOME 42)." [I did not experience this bug when using Fedora Silverblue 36, which I believe was running GNOME 42.]: not shown - No video or evidence. The reporter is also unsure of the GNOME version.
- "GNOME acts on older search results that are out of sync with what is displayed." [It's like GNOME is delayed and acting on the older search results]: not shown - This is the reporter's guess at the cause. It is not verified.
- "The bug is easy to reproduce and happens often." [This is very easily reproducible for me]: not shown - No recording is available to check this, and no reproduction rate is given.
