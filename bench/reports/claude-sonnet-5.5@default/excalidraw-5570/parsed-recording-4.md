# real/excalidraw-5570

_claude-sonnet-5.5@default, 19 s; looked at: frames/000055.jpg, frames/000079.jpg_

On excalidraw.com in a mobile browser, a rectangle sits near the bottom of the canvas. The element context menu (Cut, Copy, Paste, ... Delete) opens over it, then closes, and this repeats about every 4.5 s through the whole 23 s video. The touch input is not visible, so the trigger is unknown.

## Mobile: element context menu repeatedly pops up and closes over a selected rectangle

Class: **intermittent**

Environment: excalidraw.com in a phone browser (portrait 480x800, status bar shows 8:58 AM). The canvas holds a single rectangle at the bottom-left. The select tool is active. The bottom toolbar shows the menu, undo, redo and eraser buttons.

Steps:

1. Open excalidraw.com on a phone with a rectangle drawn on the canvas and the select tool active. The rectangle is shown selected, with handles, once the menu appears. (00:00.0; p001)
2. A tooltip 'Hold Ctrl to deep select, and to prevent dragging' appears. Immediately afterwards the context menu opens over the rectangle (the trigger is not visible, most likely a long-press or tap). (00:01.7; p001, p003)
3. The menu closes and a 'Press Enter to add text' hint flashes, so the screen returns to the plain canvas. The menu then reopens in the same way, about every 4.5 s (at 4.4, 6.7, 8.9, 11.2, 13.3, 15.5, 17.7, 19.9 and 22.0 s). (00:02.7; p004, p005, p009, p015, p021, p026, p031, p037, p044, p050, p056)

Expected (implied): The context menu should open once, only on a deliberate long-press or right-click. It should stay until dismissed. The selection tooltips for Ctrl and Enter shouldn't flash on a touch device.

Actual: The same cycle repeats about every 4.5 s: the tooltip appears, the context menu opens, the 'Press Enter to add text' hint flashes, and the menu closes. The menu opens and closes by itself in the video, with the trigger not visible. The author says nothing about it, and the only speech is 'Thank you.'

Key events: p001, p003, p004, p005, p009, p015, p056, p058

Missed by the author:

- Keyboard-only hints ('Hold Ctrl to deep select...', 'Press Enter to add text') flash on a touch device in every cycle (p001, p004, p006, p010).
- In frame 000055 the rectangle is selected and the context menu overlaps the bottom toolbar.
- In the later cycles (p037 to p050) the URL/tab bar status text reorders and the menu text is misread in OCR, which may be a flicker of the layout (p030).
