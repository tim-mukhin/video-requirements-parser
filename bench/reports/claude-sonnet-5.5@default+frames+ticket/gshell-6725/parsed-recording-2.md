# real/gshell-6725

_claude-sonnet-5.5@default, 32 s; looked at: frames, frames/0000.0.jpg, frames/0000.5.jpg, frames/0001.0.jpg, frames/0001.5.jpg, frames/0002.0.jpg, frames/0002.5.jpg, frames/0003.0.jpg, frames/0003.5.jpg, frames/0004.0.jpg, frames/0004.5.jpg, frames/0005.0.jpg, frames/0005.5.jpg, frames/0006.0.jpg_

In the Overview the user types a search term and presses Enter almost at once. Celluloid launches although the typed text is "ca", which is not a Celluloid match. The result list on screen was still the one for the first letter and had not updated, so Enter acted on that stale selection.

## Enter in Overview search launches the stale first-letter result (Celluloid) instead of the result for the full typed text

Class: **wrong-data**

Environment: GNOME Shell (44.1 per the ticket, Wayland, Fedora Silverblue 38; none of this is visible in the video). Overview with the dash showing Firefox, Files, Steam, Discord and others. Recording dated Sat 27 May 19:07. Search results shown: Celluloid, Calculator, Calendar, Code - OSS, Connections, PulseAudio Volume Control, plus Settings entries.

Steps:

1. Desktop is empty with no Overview open. (00:00.0; 0000.0)
2. Open the Overview (inferred: Super key or Activities). The empty search field "Type to search" appears and is focused. (00:01.0; 0001.0)
3. Type a first letter ("c"). Results appear with Celluloid highlighted as the selected first result and Calculator second. (00:01.5; 0001.5)
4. Type the next letter quickly. The field reads "ca", but the result list is unchanged and Celluloid is still highlighted. The Settings row shows a partially re-rendered description, so the list is mid-update. (00:02.0; 0002.0)
5. Press Enter (inferred; keys are not visible). The Overview closes and Celluloid is launched, shown in the top bar as the active app. (00:02.5; 0002.5)
6. The Celluloid window appears (empty player). It stays up for about 2 s, then the desktop is shown again with the Celluloid top-bar entry still showing a spinner. (00:03.0; 0003.0, 0003.5, 0004.0, 0004.5, 0005.0, 0005.5, 0006.0)

Expected (implied): Enter should launch the result that matches the text currently typed and shown as selected. For "ca" this would be the first result for that query (for example Calculator or Calendar), not the stale result for "c".

Actual: With "ca" in the search box, Enter launches Celluloid, the highlighted result for the earlier query "c". The result list had not refreshed to match the typed text when Enter was pressed.

Key events: 0001.5, 0002.0, 0002.5

Missed by the author:

- The Celluloid window opens empty and is then replaced by the bare desktop at about 5.5 s while the top bar still shows a loading spinner (0005.5, 0006.0). This may be Celluloid itself starting up or closing, and is not necessarily part of the bug.
- The Settings row description re-renders mid-update at 2.0 s ("Restrict camera acc..."), which suggests the result list was in the middle of refreshing when Enter was pressed (0002.0).

Claims:

- "Quickly typing a search term and pressing Enter opens the wrong app." [GNOME very often opens the incorrect search result]: confirmed - At 2.0 s the field shows "ca" with Celluloid still selected. At 2.5 s Celluloid is what launches.
- "The screen visually shows the correct result for the full term as selected, but a different app opens." [Visually everything is shown correctly, but ... pressing the Enter key opens the previously-shown result]: refuted - In this video the list is also stale on screen. At the last frame before Enter (2.0 s) the term is "ca" and Celluloid is still highlighted. Calculator is never shown selected. Frame sampling is 0.5 s, so a brief correct display between frames cannot be excluded.
- "The term typed is "calc"." [When I add "alc" to search for "calc"]: not shown - The video only reaches "ca" before the Overview closes. The rest of the typing falls between frames.
- "The wrong app is out of sync with the search results, as if acting on older results." [It's like GNOME is delayed and acting on the older search results]: confirmed - The list in frame 2.0 is identical to the "c" list from 1.5 despite the changed text, which fits a stale-result race.
