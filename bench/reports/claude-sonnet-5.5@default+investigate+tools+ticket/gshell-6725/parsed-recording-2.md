# real/gshell-6725

_claude-sonnet-5.5@default, 24 s; looked at: looks/0001.00-0002.50-800_0_2200_900/sheet.jpg_

In the GNOME Overview search, the field reads "cal" and the results update to show Calculator as selected. Enter then launches Celluloid, the top result for the earlier query "c". The result shown as selected is not the one that opens, so fast typing followed by Enter launches the wrong app.

## Overview search: Enter launches stale first-letter result (Celluloid) although Calculator is shown selected for "cal"

Class: **wrong-data**

Environment: GNOME Shell Overview (Wayland, Fedora Silverblue 38, GNOME 44.1 per the ticket only; not visible in the video). Recording recording-2.webm, 3840x2160, 6.5 s, no audio, no cursor or keys visible. Results seen: Celluloid, Calculator, Calendar, Code - OSS, Connections, PulseAudio Volume Control, plus Settings entries.

Steps:

1. Overview opens with an empty "Type to search" field (the trigger is not visible). (00:00.9; p001)
2. Type "c". "Searching..." shows, then results appear with Celluloid selected first. (00:01.4; p002, p003)
3. Quickly type "al". The field reads "cal" at about 1.9-2.1 s while the list still shows the "c" results. By about 2.23 s the list updates and Calculator is selected first. (00:02.2; p003)
4. Press Enter (the key is not visible). The Overview closes at about 2.47 s and Celluloid launches instead of Calculator. (00:02.5; p004, p005)

Expected (implied): Enter opens the result shown as selected for the typed text: Calculator for "cal".

Actual: Calculator is highlighted for "cal" in the last frames before the Overview closes (about 2.38 and 2.41 s). Celluloid then opens: its window and top-bar entry appear at 2.5-2.8 s. Enter acted on the stale selection from the "c" query.

Key events: p003, p004, p005

Missed by the author:

- The list for "c" stayed on screen for roughly 0.5 s after the text changed to "cal" (about 1.9-2.2 s). This is the window in which Enter hits stale results.
- Celluloid shows an empty window, then a bare desktop at about 5.5 s with the top-bar entry still showing (p008, p009). This is probably just Celluloid starting or closing, not the bug.

Claims:

- "Enter opens the wrong result when typing quickly" [ticket]: confirmed - Celluloid opens (p004, p005) after typing "cal".
- "Visually everything is shown correctly (term and selected result) but Enter opens the previous result" [ticket]: confirmed - Frames at about 2.23-2.41 s show "cal" in the field and Calculator highlighted. The watcher's reading that the list was still stale and the text was "ca" is wrong. The list had updated by about 2.23 s, shortly before Enter.
- "It worked in Silverblue 36 / GNOME 42" [ticket]: not shown - Only one version context, and it is not visible in the video.
