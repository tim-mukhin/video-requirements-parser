# real/excalidraw-5570

_claude-sonnet-5.5@default, 19 s; looked at: frames/000083.jpg, frames/000052.jpg_

On excalidraw.com in a mobile browser, a rectangle is selected and the context menu (Cut/Copy/Paste/Copy to clipboard as PNG/SVG) keeps flashing, disappearing and reappearing at slightly different positions. The bottom hint toast alternates between 'Hold Ctrl to deep select…' and 'Press Enter to add text' in a loop for the whole 17 s. The menu also runs off the bottom of the screen and is partly cut off, so the UI is unusable and flickers.

## Excalidraw mobile: context menu and hint toast flicker in a loop, and the menu is clipped by the bottom edge

Class: **intermittent**

Environment: excalidraw.com in a Brave-style mobile browser on a portrait phone (480x800), 8:55 AM. One rectangle is selected. No account or organization is visible.

Steps:

1. Open excalidraw.com on the phone with a rectangle drawn and selected. How the menu was opened is not visible, so it was most likely a long-press or tap on the shape. (00:01.1; p001, p002)
2. The context menu (Cut/Copy/Paste/Copy to clipboard as PNG/SVG) appears next to the selected rectangle. Its position shifts between frames, and the toast alternates between 'Press Enter to add text' and 'Hold Ctrl to deep select…'. (00:02.1; p003, p004, p006)
3. Without further visible input, the menu disappears and reappears roughly every 3.4 s, and the toast changes each time, up to the end of the video. (00:04.3; p008, p012, p016, p020, p024, p028, p032, p036, p040, p043)

Expected (implied): The context menu stays open and stable, fully visible on screen, until the user picks an action or dismisses it. The hint toast does not alternate or flicker.

Actual: The context menu and toast cycle on and off about every 0.3–1 s for the whole video. The menu moves between frames. In frame 000083 it is cut off at the bottom of the screen, with 'Copy to clipboard as SVG' half hidden behind the bottom toolbar.

Key events: p003, p004, p006, p010, p014, p022, p030, p038, p042, p043

Missed by the author:

- The only speech is 'Thank you.' [u001]. The author says nothing about the flicker.
- OCR misreads of the menu ('Conyta allnhaard ae cavse', 'Coov to clioboard') in p006, p009 and p038 come from the menu changing mid-render. They are not real UI text.
- The menu is clipped at the bottom and overlaps the bottom toolbar [p006], frame frames/000083.jpg.
