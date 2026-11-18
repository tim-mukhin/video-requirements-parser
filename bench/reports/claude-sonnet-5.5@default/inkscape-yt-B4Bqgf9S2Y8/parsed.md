# real/inkscape-yt-B4Bqgf9S2Y8

_claude-sonnet-5.5@default, 58 s; looked at: frames/000935.jpg, frames/000888.jpg_

The video is mostly a solo developer update, not a meeting. In the first minute the author launches a freshly built Inkscape to test a stroke-to-path fix, says it "didn't work" and that "numbers are wrong". The screen shows only the circle's size readout (W/H 41.587 with a 1.587 mm stroke). No stroke-to-path run or wrong result is captured in the parsed events.

## Stroke-to-path fix test: author reports wrong size values (bounding box) after the fix

Class: **wrong-data**

Environment: Inkscape development build run from a terminal (doctormo@production-02, ~/Projects/inkscape/inkscape/build). Document t.svg with one red circle. Fill and Stroke dialog on the Stroke style tab. PathCutting.cpp open in an editor. The terminal prints many 'Looking at nl:' warnings.

Steps:

1. Launch the rebuilt Inkscape from the terminal; a new process (pid 217517) starts printing warnings and opens t.svg. (00:16.6; p106, p162)
2. Circle in Layer 1 is selected: W/H 40.000, flat red fill. (00:24.5; p219, p220, p221)
3. Open Stroke style: stroke width 1.587 mm. (00:27.4; p268)
4. Toolbar bounding box changes to X/Y -0.793 and W/H 41.587, which is the size including the stroke. (00:29.5; p300, p301, p302)
5. A 'Save changes to document t.svg before closing?' dialog appears for about a second, so the author closes the test window. (00:31.6; p317)
6. The author says it didn't work and the numbers are wrong, then returns to the terminal and code. (00:32.0; u005, u006, p394)

Expected (implied): After the fix, the geometry or bounding-box numbers should be correct. The video does not say which numbers are expected.

Actual: The author says the fix didn't work and the numbers are wrong. The only numbers visible are the 41.587 mm W/H in the toolbar. That is 40 plus the 1.587 stroke width, so it is the visual bounding box including stroke. The parsed events do not show a stroke-to-path run or a before/after comparison, so the exact wrong value is not established.

Key events: p219, p268, p301, p302, p317, u005, u006, u021

Missed by the author:

- The 'Save changes before closing?' dialog flashed for about 1 s just as the test window was closed (p317).
- The 41.587 W/H shown on screen matches 40 + 1.587 stroke width, which may be the 'wrong' bounding box (p301, p302).

Claims:

- ""No, that didn't work." The fix did not work." [u005]: not shown - The window is closed with no visible stroke-to-path result.
- ""But numbers are wrong."" [u006]: not shown - Only the 41.587 W/H and X/Y -0.793 readouts are visible. It is unclear which value the author means.
- "We currently have a bounding box issue; it will be fixed next week." [u021]: not shown - This is a future plan with no on-screen evidence.
- "The Wacom/touch problems on Windows are not fixable in Inkscape." [u062]: not shown - This is the author's opinion about another platform, and nothing about it is shown.
- "The eraser tool leaves red paint behind after the Layers dialog is opened, and swapping out the selection handling fixed it." [u070]: not shown - This is told as past work. The video does not show it.
