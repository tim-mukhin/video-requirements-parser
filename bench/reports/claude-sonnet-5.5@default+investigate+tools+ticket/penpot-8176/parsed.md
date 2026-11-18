# real/penpot-8176

_claude-sonnet-5.5@default, 26 s; looked at: frames/0012.0.jpg, frames/0057.0.jpg, frames/0026.0.jpg_

In Penpot (Italian UI), a Card board with nested flex layouts (Hug/Fill) does not re-layout correctly. After a child was removed, a blank gap stayed until the layout sizing was toggled. After the card was resized, the text blocks overlapped and the panel showed a width that did not match the canvas. The video has no audio, so every fact comes from the screen.

## Nested flex Hug/Fill board keeps stale size after child removal and parent resize

Class: **wrong-data**

Environment: Penpot editor in a browser, Italian UI. Project page 'Bug 1', board 'Card' with Image, TextWrapper (HeaderWrapper with Title and Text, plus a Text), Divider, Wrapper and a Button / ButtonFilled instance. The video does not show the OS or the browser version.

Steps:

1. Card layout is shown with TextWrapper selected. The tags Board layer is gone from the layer tree, but its deletion is not visible. TextWrapper shows H 196.5 with empty space left below the text. (00:12.0; p107, p110)
2. Select Card (W 343, H 645 per the OCR); the gap is still there. Click layout and flex sizing controls in the design panel. (00:13.1; p110, p118, p135)
3. After the sizing control is clicked, the card shrinks to H 597 and the gap closes. The frame at 26.0 s shows H 597. (00:24.1; p181)
4. Drag the Card's right edge to widen it from W 343 to about 433. The children Fill the width, but the stars stay at their old positions. (00:32.4; p286, p287)
5. Select HeaderWrapper and Text layers, then narrow the card again. The 'Text:' block overlaps the Lorem text and the stars overlap the price. This is from the watcher's reading of frames 0048.0–0054.0; I did not open those frames. (00:48.1; p419, p446)
6. Select Card and drag the edge again. The panel shows W 433 and H 597, but the rendered card is narrower (about 343 wide), so the panel and the canvas disagree. (00:57.3; p470, p478)

Expected (implied): Hug and Fill containers recompute their size and child positions right after a child is removed or the parent is resized. No gaps or overlaps remain, and the panel values match the canvas.

Actual: After the child was removed, the Card and TextWrapper kept their old height, leaving a gap until the sizing control was clicked. After resizing, content overlapped. At 57.0 s the panel says W 433 while the canvas draws a narrower card.

Key events: p107, p110, p181, p286, p478

Missed by the author:

- The gap after the removal closes only after a click on the flex sizing control, around 22–24 s (p135, p181).
- At 57.0 s the panel shows W 433 while the canvas card is narrower.

Claims:

- "Hug and Fill settings do not update correctly even though they appear applied in the UI" [ticket]: confirmed - Frame 0012.0 shows the stale gap and frame 0057.0 shows W 433 against a narrower canvas.
- "The problem is triggered by removing an element or extending the card content" [ticket]: not shown - The removal is not visible and is inferred from the missing layer. Resizing is visible. Extending the content is not shown.
- "macOS, Chrome 143" [ticket]: not shown - The OS and browser version are not visible in the video.
