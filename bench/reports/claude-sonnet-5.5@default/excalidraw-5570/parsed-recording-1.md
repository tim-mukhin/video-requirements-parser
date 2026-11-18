# real/excalidraw-5570

_claude-sonnet-5.5@default, 22 s; looked at: frames/000022.jpg, frames/000289.jpg, frames/000487.jpg_

On excalidraw.com in a mobile browser (Android phone, portrait), a context menu (Cut/Copy/Paste/…/Delete) pops up repeatedly over a selected hand-drawn circle. It appears at the start and again around 00:04, 00:11 and 00:14.6, each time right after a touch on the canvas. The video has no audio and no cursor, so the author's intent is not stated. The menu is the likely problem: it covers the canvas and the bottom toolbar.

## Mobile: context menu opens on touch/long-press of a selected element, interrupting selecting and moving it

Class: **intermittent**

Environment: Chrome on an Android phone (portrait 996×2160, battery 37%→36%), excalidraw.com, 12 tabs open. The Select tool is active with one ellipse on the canvas, and the mobile bottom toolbar shows undo/redo/duplicate/delete.

Steps:

1. Open excalidraw.com on the phone with a circle on the canvas. The Select tool is active. (00:00.0; p001)
2. Touch the circle (the trigger is not visible). The 'Hold Ctrl to deep select…' hint flashes and the full context menu opens next to the selected circle. (00:00.5; p002, p003)
3. The menu closes and the circle selection is lost (selection handles and bottom-toolbar icons change). The context menu then reopens on the canvas (Paste / Select all / Show grid / Zen mode / View mode / Stats for nerds) and closes again. (00:03.3; p006, p010, p014, p016, p018)
4. Further touches on the canvas repeatedly flash the 'Hold Ctrl…' hint and the canvas context menu. The circle ends up selected again. (00:06.2; p019, p022, p027, p037)
5. The element context menu opens again. After it closes, the circle is at a different position, upper-left of where it was, so it was moved at some point (frames 000289 vs 000487). (00:11.2; p038, p041, p042)
6. Another touch shows the hint again, and the full element context menu opens a third time over the selected circle. (00:14.4; p043, p050, p051, p052)

Expected (implied): Touching, selecting or dragging an element on a touch device selects or moves it. The context menu should not open unless the user deliberately long-presses, and should not repeatedly cover the canvas and toolbar.

Actual: The context menu opens repeatedly, apparently on ordinary touch interaction with the canvas or the selected circle. It covers the drawing and the bottom toolbar, and the selection is lost and regained in between. The 'Hold Ctrl to deep select' hint, a desktop-only instruction, flashes on every touch. The long-press that triggers the menu is not visible, and the cause is not provable from the video alone.

Key events: p002, p003, p014, p038, p041, p050, p051, p053

Missed by the author:

- The desktop-only hint 'Hold Ctrl to deep select, and to prevent dragging' flashes on touch many times (p002, p013, p019, p021, p024, p027, p037, p043).
- The element context menu also opens at 00:11.2 (p038) and 00:14.6 (p050), after the circle has moved on screen (p041).
