# real/excalidraw-5570

_claude-sonnet-5.5@default, 16 s; looked at: nothing_

On some Android devices, the Excalidraw context menu first appears and is then repositioned, and scrolling it is unreliable. It reproduces on a Pixel 4A and on Chromium-based browsers, but not on the Samsung Note 8 or in Firefox/Mi browser. This makes the menu hard to use on affected devices.

## Context menu is repositioned after display and scrolling is inconsistent on Android (Chromium)

Class: **intermittent**

Environment: Pixel 4A with Chrome 104.0.5112.69 (affected). Samsung Note 8 with the same Chrome version, iPhone SE and Xiaomi Redmi Note 8 Pro / Motorola E4 Plus with Firefox or Mi browser (not affected). Also seen in the Obsidian Excalidraw plugin (obsidian-excalidraw-plugin#742). Chromium browsers on the Xiaomi and Motorola devices were affected.

Steps:

1. Open Excalidraw on an affected Android device (for example a Pixel 4A in Chrome). (00:00.0; )
2. Open the context menu on the canvas (the ticket does not say how, probably a long press). (00:00.0; )
3. Watch the menu: it appears, then jumps to a different position. Try scrolling it. (00:00.0; )

Expected (implied): The context menu appears once at a stable position and scrolls normally.

Actual: The context menu is displayed and then repositioned. Scrolling the menu does not work consistently. This happens on the Pixel 4A and on Chromium browsers, but not on the Samsung Note 8.

Key events: 

Claims:

- "The menu is displayed and then repositioned on the Pixel 4A." [the context menu is displayed, then repositioned]: not shown - The recording is not available; this is the reporter's description only.
- "The issue depends on the browser engine: Chromium browsers are affected, Firefox and Mi browser are not." [it did appear when using a chromium browser]: not shown - This is a second-hand report from pikatwinky and was not verified.
- "The Samsung Note 8 is not affected even though it runs the same Chrome version as the Pixel 4A." [ok on Samsung Note 8]: not shown - No evidence beyond the reporter's statement.
