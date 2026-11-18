# real/kde-528799

_gpt-6-sol@default, 40 s; looked at: frames/0012.5.jpg, frames/0019.0.jpg, frames/0019.5.jpg, frames/0007.5.jpg, frames/moments/p065.jpg, frames/moments/p076.jpg, frames/0010.5.jpg, frames/0013.5.jpg, frames/0017.5.jpg, frames/0021.0.jpg, frames/0023.0.jpg, frames/moments/p084.jpg, frames/moments/p083.jpg, frames/moments/p096.jpg, frames/0005.5.jpg, frames/moments/p047.jpg_

While a selected shape is repeatedly resized in Krita, its visible edge temporarily lags behind the selection outline, making precise placement difficult. The frames confirm the mismatch, and the timeline records changing geometry and brief Updating indicators; the video does not show whether snapping is enabled.

## Shape edge temporarily lags behind selection outline during resizing

Class: **intermittent**

Environment: Krita on Android, recorded with XRecorder. An unsaved document is active with the Mask layer selected.

Steps:

1. Open the Krita document with the shape already selected (the trigger is not visible). (00:05.2; p022)
2. Resize the selected shape repeatedly from its left edge; the touch gestures are not visible, but the handle position and geometry values change. (00:09.9; p031, p034, p044, p055, p071, p079, p088, p098)

Expected (implied): The shape should resize precisely, with its visible edge following the selection outline.

Actual: At 12.5 s and 19.0 s, the black edge remains separated from the moved outline. At 19.5 s, the edge and outline coincide again. Brief Updating indicators appear during the sequence, including the short event captured in the p065 moment frames. The frames establish the visual lag; they do not establish that snapping causes it.

Key events: p034, p044, p045, p055, p065, p071, p077, p079, p083, p088

Missed by the author:

- The visible shape edge temporarily differs from the selection outline, then catches up; the frames settle this distinction while geometry changes in the timeline corroborate it [p044, p079, p083].
- Krita briefly displays Updating during the resizing sequence, including in the p065 moment frames [p045, p065, p077].
- The active document is marked [Not Saved] and the selected layer is Mask [p022].

Claims:

- "The shape snaps even though all Snap To settings are off." [ticket: title]: not shown - The video shows abrupt position changes and temporary edge/outline mismatch, but never opens the snapping settings.
- "The arrow tool was clicked before stretching the layer." [ticket: steps 1–2]: not shown - The tool and resize handles are already active when Krita appears; no tool click or resize touch is visible.
- "Each stretch snaps the shape farther away." [ticket: step 3]: refuted - The left handle moves in both directions and returns near an earlier position rather than progressively moving farther away.
