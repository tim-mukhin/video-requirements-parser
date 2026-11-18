# real/excalidraw-5570

_claude-sonnet-5.5@default, 17 s; looked at: nothing_

On some Android devices running Chromium-based browsers, the Excalidraw context menu is first shown and then repositioned, and scrolling it is inconsistent. It reproduces on a Pixel 4A but not on a Samsung Note 8 with the same Chrome version, so it makes the menu hard to use on affected phones.

## Context menu is repositioned after opening and scrolls inconsistently on some Android Chromium browsers

Class: **intermittent**

Environment: Pixel 4A, Chrome 104.0.5112.69: NOT OK. Samsung Note 8, Chrome 104.0.5112.69: OK. iPhone SE (written '5SE'): OK. Per a commenter: Xiaomi Redmi Note 8 Pro and Motorola E4 Plus were OK with Firefox and Mi Browser, but the issue appeared with a Chromium browser. Seen through the Obsidian Excalidraw plugin and probably also the Excalidraw web app (not stated).

Steps:

1. On an affected Android device (e.g. Pixel 4A) in a Chromium-based browser, open Excalidraw. (00:00.0; )
2. Open the context menu (the ticket does not say how, probably a long-press or right-click on the canvas). (00:00.0; )
3. Watch the menu appear, then jump to a new position. Try to scroll it. (00:00.0; )

Expected (implied): The context menu appears once at a stable position and scrolls reliably on all devices.

Actual: The context menu is displayed and then repositioned on the Pixel 4A. Menu positioning and scrolling are inconsistent between devices and browsers, and the repositioning is not seen on the Note 8.

Key events: 

Claims:

- "The issue does not occur on the Samsung Note 8." [ok on Samsung Note 8 ... I can't observe this repositioning on the Note 8.]: not shown - There is no video, and the ticket gives no details of how it was tested.
- "The issue is specific to Chromium browsers." [it did appear when using a chromium browser]: not shown - This comes from a commenter's report. The reporter's own results (Note 8 OK and Pixel 4A not OK on the same Chrome version) contradict a pure browser explanation.
