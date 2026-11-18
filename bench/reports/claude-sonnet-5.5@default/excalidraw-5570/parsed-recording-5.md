# real/excalidraw-5570

_claude-sonnet-5.5@default, 19 s; looked at: frames/000036.jpg, frames/000083.jpg, frames/000138.jpg_

On excalidraw.com in a mobile browser, a curved multi-point arrow is open in point-edit mode. The author opens the context menu and taps "Flip vertical" four times. Each time the menu closes and the arrow looks unchanged, so the flip appears to do nothing in this mode. There is no audio, so the author's intent is inferred from the screen.

## "Flip vertical" in the context menu has no visible effect on an arrow being edited in point-edit mode (mobile web)

Class: **silent-fail**

Environment: excalidraw.com in a mobile browser (Android-style status bar, portrait 1440×3120). One arrow with 3 points is selected in line-editing mode (hint text: "Select a point to edit…" / "Press Delete to remove point(s)…"). The context menu lists Cut, Copy, Paste, Copy as PNG/SVG, Copy/Paste styles, Add to library, layer order, Flip horizontal, Flip vertical, Create link, Duplicate, Lock and Delete. No accounts are visible.

Steps:

1. With the arrow in point-edit mode, the context menu is open with "Flip vertical" highlighted. How it was opened is not visible. (00:01.2; p001)
2. Tap "Flip vertical". The menu closes and the arrow stays the same shape, with the same endpoints and arrowhead position. (00:02.3; p008, p005)
3. Open the context menu again (the trigger is not visible) and tap "Flip vertical" again. The menu closes and the arrow is again unchanged. The same open, tap and close cycle repeats at about 5.2 s, 8.8 s and 10.5 s. (00:04.2; p010, p011, p017, p020, p049, p057)

Expected (implied): Tapping "Flip vertical" should mirror the selected arrow vertically, or the app should say why the flip cannot be done in this mode.

Actual: After each tap on "Flip vertical" the menu closes and the arrow keeps the same shape and position. No error or message is shown, and the editor stays in point-edit mode.

Key events: p001, p008, p011, p020, p049, p057

Missed by the author:

- The author cannot be assessed here, since nobody speaks. The menu appears and vanishes within 0.5–0.6 s several times (p010, p025, p058). The point-edit hint text also flickers in and out (p012, p018, p021).
