# real/excalidraw-5570

_claude-sonnet-5.5@default, 26 s; looked at: looks/0001.50-0004.50/sheet.jpg_

On excalidraw.com in Brave on a phone, a context menu for a selected rectangle near the bottom of the canvas opens clipped. It closes and reopens at a different position in a loop for about 15 s, and the 'Copy to clipboard as PNG' items are cut off. This matches the ticket's 'displayed, then repositioned' symptom on Chromium Android.

## Context menu near the bottom edge opens clipped and keeps repositioning or reopening (Android Chromium)

Class: **intermittent**

Environment: Android phone (portrait 480x800), Brave browser (Brave icon in the address bar), excalidraw.com, one rectangle selected near the bottom of the canvas, clock 8:55 AM. The device model and browser version are not visible. The ticket says Pixel 4A and Chrome 104 for recording-1, but this is recording-2, from a commenter, so its device is not identified.

Steps:

1. A rectangle is selected near the bottom of the canvas and no menu is shown (the first frames show the 'Hold Ctrl to deep select' hint). (00:00.0; s001, p001)
2. Context menu opens (the long-press trigger is not visible). Only Cut, Copy and Paste show, and the menu is cut off at the bottom by the toolbar and screen edge. (00:01.6; p002)
3. The menu disappears (about 3.5 s). It then reappears at 3.7 s, shifted up and left, and now includes 'Copy to clipboard as PNG', which is still cut off at the bottom. (00:03.4; p005, p006)
4. Repeat: the menu closes and reopens roughly every 3.5 s with a different size and position each time, cut off at the bottom each time (cycles at about 4.8, 6.2, 7.7, 9.1, 10.5, 11.8, 13.1 and 14.3 s). The hint at the top alternates between 'Press Enter to add text' and 'Hold Ctrl to deep select' in step with each cycle. (00:04.8; p010, p014, p018, p022, p026, p030, p034, p038)
5. The recording ends with the menu closed and the 'Press Enter to add text' hint showing. (00:16.0; p042, p043)

Expected (implied): The context menu opens once, stays in one place, and is fully visible or scrollable so that every item, including the clipboard-as-PNG items, can be reached.

Actual: The menu opens cut off at the bottom and its position and size change from one cycle to the next. It closes and reopens repeatedly, and the bottom items are never fully shown. The menu's first appearance shows only three items. Later appearances add 'Copy to clipboard as PNG', with different offsets.

Key events: p002, p005, p006, p010, p014, p022, p030, p038

Missed by the author:

- The menu does not just reposition once. It closes and reopens in a loop, and the loop shows no visible user action (no touch marks are followed in this video) (p005, p009, p013, p017).
- The first appearance has only Cut, Copy and Paste, while later ones add the clipboard-as-PNG items (p002 vs p006, p014).
- The top hint toggles in sync with each menu cycle (p003, p004, p007, p008 and later).

Claims:

- "The context menu is displayed, then repositioned (ticket)." [ticket]: confirmed - Frames at 2.1 s and 3.7 s show the menu at different positions and sizes. The menu closes and reopens many times, shifting each time.
- "Reproduces on Pixel 4A with Chrome 104 (ticket)." [ticket]: not shown - The device and browser version are not identifiable. The video shows Brave, which is Chromium-based.
- "Menu scrolling is inconsistent (ticket title)." [ticket]: not shown - No scroll gesture is visible. Only the clipping and the repositioning are shown.
- "Speech: 'Thank you.'" [u001]: not shown - The only speech is a likely speech-recognition artifact and says nothing about the problem.
