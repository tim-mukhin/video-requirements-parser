# real/excalidraw-5570

_claude-sonnet-5.5@default, 19 s; looked at: frames/000047.jpg, frames/000087.jpg_

On Excalidraw in a mobile browser, a rectangle is selected and the context menu (Cut, Copy, Paste and so on) keeps opening and closing on a loop of about 3.5 s. Hint toasts flash each time. The menu does not stay open long enough to use. The video shows no touch input, so what triggers each cycle is unknown.

## Mobile context menu for a selected shape repeatedly opens and then vanishes or is clipped

Class: **intermittent**

Environment: Excalidraw (excalidraw.com) in a mobile browser, portrait 480x800, 3 tabs open. One rectangle is selected on the canvas. No account or organization is visible.

Steps:

1. Open excalidraw.com on a phone, with a rectangle selected on the canvas. (00:00.0; p001)
2. The context menu opens over the selected rectangle (the trigger is not visible, most likely a long-press). It lists Cut, Copy, Paste, Copy as PNG/SVG, Copy/Paste styles, Add to library, layer order, Flip, Create link, Duplicate, Lock and Delete. (00:01.9; p003)
3. The menu disappears. At the same time the 'Hold Ctrl to deep select, and to prevent dragging' hint and a garbled 'G c' text flash. A 'Press Enter to add text' hint appears just before the menu closes. (00:03.6; p004, p005, p006, p007, p008)
4. The menu reappears, sometimes only partly rendered ('Cut | Copy | Paste' or 'Copy | Paste'), then vanishes again. This repeats about every 3.5 s until the end of the video. (00:04.2; p024, p032, p043, p070, p091, p099, p103)

Expected (implied): The context menu stays open until the user picks an item or dismisses it, and shows all its items consistently.

Actual: The menu opens and closes on a loop. It often renders only partially, for example 'Cut | Copy | Paste' without the lower items, or garbled OCR text. Keyboard-hint toasts ('Hold Ctrl to deep select…', 'Press Enter to add text') flash on each cycle. The author cannot use the menu.

Key events: p003, p008, p024, p032, p043, p063, p091, p103

Missed by the author:

- The keyboard-hint toasts ('Hold Ctrl to deep select…', 'Press Enter to add text') alternate with the menu in step with its open/close cycle (p001, p004, p005, p025, p026).
- The menu is often only partly rendered (p032, p037, p063, p091).

Claims:

- "'Thank you.' is the only speech and says nothing about the problem." [u001]: not shown - The speech gives no claim to check.
