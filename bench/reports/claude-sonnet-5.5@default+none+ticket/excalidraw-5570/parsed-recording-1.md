# real/excalidraw-5570

_claude-sonnet-5.5@default, 16 s; looked at: nothing_

On some Android devices, the Excalidraw context menu first appears and is then repositioned, and scrolling inside it doesn't work consistently. Reports say it happens on Pixel 4A and on Chromium-based Android browsers, but not on Samsung Note 8 or iPhone. This makes the menu hard to use on affected devices.

## Context menu repositions and scrolls inconsistently on Android (Pixel 4A, Chromium browsers)

Class: **intermittent**

Environment: Android Chrome 104.0.5112.69 on Pixel 4A (affected) and Samsung Note 8 (not affected). iPhone SE (5SE) is fine. Xiaomi Redmi Note 8 Pro and Motorola E4 Plus: fine in Firefox and Mi Browser, affected in Chromium browsers. Also reported through Obsidian Excalidraw plugin.

Steps:

1. Open Excalidraw on an affected Android device in a Chromium-based browser (e.g. Chrome on Pixel 4A). (00:00.0; )
2. Open the context menu (the ticket does not say how, probably a long-press on the canvas). (00:00.0; )
3. Watch the menu: it appears, then is repositioned. Try scrolling it. (00:00.0; )

Expected (implied): The context menu appears once at a stable position and scrolls normally.

Actual: The context menu is displayed, then jumps to a different position. Scrolling inside it does not work consistently. This does not happen on the Samsung Note 8.

Key events: 

Claims:

- "The issue does not occur on Samsung Note 8 or iPhone SE, but does on Pixel 4A." [ok on Samsung Note 8 - NOT OK on Pixel 4A - ok on iPhone 5SE]: not shown - No video was available; this is the reporter's own testing.
- "The issue appears on Chromium browsers but not Firefox or Mi Browser." [it did appear when using a chromium browser]: not shown - Second-hand report from pikatwinky; the recordings were not available.
