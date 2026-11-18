# real/ff-2092950

_gpt-6-sol@default, 49 s; looked at: frames/0003.5.jpg, frames/0004.0.jpg, frames/0020.0.jpg, frames/0027.5.jpg, frames/moments/p108.jpg, frames/moments/p095.jpg, frames/moments/p118.jpg, frames/moments/p009.jpg, frames/moments/p020.jpg, frames/moments/p024.jpg, frames/moments/p056.jpg, frames/moments/p088.jpg, frames/moments/p104.jpg, frames/0000.0.jpg, frames/0003.0.jpg, frames/0019.5.jpg, frames/0020.5.jpg, frames/0032.0.jpg, frames/0035.0.jpg, frames/moments/p145.jpg, frames/0037.5.jpg, frames/moments/p122.jpg, frames/0026.5.jpg, frames/0028.0.jpg, frames/0030.0.jpg, frames/0016.5.jpg, frames/0018.0.jpg, frames/0009.5.jpg_

The range slider thumb intermittently disappears while the track and numbered tooltip remain visible, obscuring the selected position. The video shows it return at the same value without a value change; the behavior also appears with other track shapes.

## Range slider thumb intermittently disappears during dragging

Class: **intermittent**

Environment: Fancy Range Slider in a CodePen preview; browser and version are not visible.

Steps:

1. With shape set to curve and “Keep the tooltip straight” unchecked, drag the slider from its initial value of 20 toward the right end. (00:02.2; p001)

Expected (implied): The thumb remains visible at the selected position throughout the drag.

Actual: At 3.5 s, the tooltip reads 100 but the thumb is absent; at 4.0 s, the thumb is visible again at 100. The frames settle the visual finding, while the timeline supplies the drag time. The thumb is also absent at bell value 83 and arc value 89, with “Keep the tooltip straight” checked in both cases.

Key events: p001, p005, p067, p070, p076, p103, p108

Missed by the author:

- The screen shows the thumb absent at 100 and visible again at the same value, rather than a value reverting [p005].
- The failure is visible on bell and arc with “Keep the tooltip straight” checked, as well as on the initial curve with it unchecked [p067, p076, p108].

Claims:

- "Dragging causes flickering, mostly toward high values." [ticket.md: Actual results]: confirmed - The thumb disappears at 100, 83 and 89; the frames also show it returning at the same value. The video does not establish a frequency for “mostly.”
- "The numbered tooltip must be present to trigger the flicker." [ticket.md: Expected results]: not shown - The tooltip is present during the failures, but the video never tests the slider without it.
- "The linked simplified CSS demo reproduces the issue." [ticket.md: Steps to reproduce]: not shown - The recording shows the Fancy Range Slider preview, not the simplified demo.
