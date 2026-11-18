# real/excalidraw-5570

_claude-sonnet-5.5@default, 16 s; looked at: nothing_

On some Android devices, the Excalidraw context menu first appears and is then repositioned, and scrolling it does not work reliably. It reproduces on a Pixel 4A and with Chromium-based browsers on Xiaomi and Motorola phones, but not on a Samsung Note 8 or an iPhone. Users on affected devices may be unable to reach all menu items.

## Context menu positioning and scrolling inconsistent on Android (Chromium)

Class: **intermittent**

Environment: Pixel 4A (affected), Chrome 104.0.5112.69. Samsung Note 8 with the same Chrome version (OK). iPhone 5SE (OK). Per a commenter, Xiaomi Redmi Note 8 Pro and Motorola E4 Plus are OK with Firefox and Mi Browser but affected with a Chromium browser. Seen through the Obsidian Excalidraw plugin and in Excalidraw itself.

Steps:

1. Open Excalidraw on an affected Android device, such as a Pixel 4A in Chrome. (00:00.0; )
2. Open the context menu, for example with a long press on the canvas. The ticket does not say how the reporter opened it. (00:00.0; )
3. Observe that the menu is displayed and then jumps to a different position. (00:00.0; )
4. Try to scroll the menu. Scrolling does not work consistently. (00:00.0; )

Expected (implied): The context menu appears once at a stable position, stays within the viewport, and scrolls normally.

Actual: The context menu is displayed and then repositioned. Scrolling inside it is inconsistent on affected Android devices.

Key events: 

Claims:

- "Works on Samsung Note 8" [ok on Samsung Note 8]: not shown - No video; based on the ticket text only.
- "Fails on Pixel 4A" [NOT OK on Pixel 4A]: not shown - The recording is not available.
- "Works on iPhone 5SE" [ok on iPhone 5SE]: not shown - No video.
- "The issue appears only with Chromium browsers" [it did appear when using a chromium browser]: not shown - Second-hand report from a commenter. Chrome 104 on the Note 8 is Chromium and works, so the browser alone does not explain it.
