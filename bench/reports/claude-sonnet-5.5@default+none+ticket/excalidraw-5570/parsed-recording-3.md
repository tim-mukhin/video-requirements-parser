# real/excalidraw-5570

_claude-sonnet-5.5@default, 18 s; looked at: nothing_

On some Android devices, the Excalidraw context menu is first displayed and then repositioned, and scrolling inside it is inconsistent. The reporter saw this on a Pixel 4A but not on a Samsung Note 8 or an iPhone SE. It makes the menu hard to use on affected phones, especially in Chromium-based browsers.

## Context menu is repositioned after opening and scrolling is inconsistent on Android (Pixel 4A, Chromium browsers)

Class: **intermittent**

Environment: Pixel 4A with Chrome 104.0.5112.69 (affected). Samsung Note 8 with the same Chrome version (OK). iPhone SE (OK). Xiaomi Redmi Note 8 Pro and Motorola E4 Plus with Firefox or Mi Browser (not affected), but affected with a Chromium browser, according to pikatwinky. Reached through the Obsidian Excalidraw plugin (issue 742) and also seen in Excalidraw itself. Operating system versions are not given.

Steps:

1. Open Excalidraw (or the Obsidian Excalidraw plugin) in a Chromium-based browser on an affected Android device such as a Pixel 4A. (00:00.0; )
2. Open the canvas context menu, probably with a long press. The ticket does not say how it was opened. (00:00.0; )
3. Watch the menu position, and try to scroll the menu if it does not fit on screen. (00:00.0; )

Expected (implied): The context menu appears once at a stable position, and it scrolls consistently when it does not fit on screen.

Actual: The context menu is displayed and then repositioned (visible on the Pixel 4A). Scrolling in the menu works inconsistently. The ticket gives no further detail.

Key events: 

Claims:

- "Pixel 4A shows the issue, while Samsung Note 8 and iPhone SE do not." [ok on Samsung Note 8; NOT OK on Pixel 4A; ok on iPhone 5SE]: not shown - There is no video. This rests on the reporter's testing alone.
- "Both Android devices ran the same Chrome version, so the version is not the cause." [on both the Samsung Note 8 and the Pixel 4A the browser was the same Chrome version: 104.0.5112.69]: not shown - Not verifiable without the recording.
- "Chromium browsers show the issue, while Firefox and Mi Browser do not." [did not appear on Xiaomi Redmi Note 8 Pro and Motorola E4 plus with Firefox and Mi browser, but it did appear when using a chromium browser]: not shown - This is a second-hand report. Its recordings are not available.
