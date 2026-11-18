# real/penpot-8176

_claude-sonnet-5.5@default, 43 s; looked at: frames/0000.0.jpg, frames/0006.0.jpg, frames/0012.0.jpg, frames/0018.0.jpg, frames/0024.0.jpg, frames/0030.0.jpg, frames/0036.0.jpg, frames/0042.0.jpg, frames/0048.0.jpg, frames/0054.0.jpg, frames/0060.0.jpg, frames/0009.0.jpg, frames/0015.0.jpg, frames/0045.0.jpg, frames/0051.0.jpg, frames/0057.0.jpg, frames/0021.0.jpg, frames/0039.0.jpg, frames/0033.0.jpg, frames/0003.0.jpg_

In Penpot, a Card board with nested flex layouts (Hug/Fill sizing) does not recompute its size after the tags Board is removed or after the card is resized. A gap is left where the tags were, and after narrowing the card the text blocks overlap. The hug/fill settings still show as applied in the UI.

## Nested flex Hug/Fill containers do not re-layout after child removal or parent resize (stale height, overlapping content)

Class: **wrong-data**

Environment: Penpot design editor (Italian UI) in a browser, project page 'Bug 1', board 'Card' with TextWrapper, HeaderWrapper, Divider, Wrapper and a Button / ButtonFilled instance. The ticket says macOS and Chrome 143; the video does not show this.

Steps:

1. The Card is selected (W 343, H 645). Its layout includes a tags Board (sporty/weekend/pink) inside TextWrapper. I infer the selection from the layer highlight and the design panel. (00:03.0; 0003.0)
2. Select the Text and TextWrapper layers; the Board with the tags is still present. (00:09.0; 0006.0, 0009.0)
3. The Board (tags) layer is gone. I infer it was deleted, because I did not see the action itself. TextWrapper is now H 196.5, but an empty gap remains between the text and the Divider, and the Card is still 645 tall with the Add button at the same position. (00:12.0; 0012.0)
4. Select the Card and hover the layout padding and gap values, with the card still at H 645 and the gap still visible. (00:15.0; 0015.0, 0018.0)
5. The Card's vertical sizing control (in Flex Board) is clicked. I infer this from the changed panel and the cursor on the control. The Card then shrinks and the gap closes. (00:24.0; 0024.0, 0030.0)
6. Resize the Card by dragging its right edge to widen it (W 343 to 433). Children Fill the width, but the stars stay at their old positions and the Card keeps H 597. (00:33.0; 0033.0, 0036.0, 0042.0)
7. Select HeaderWrapper and shrink the card width again. HeaderWrapper becomes W 248 and the texts wrap. The 'Text:' block now overlaps the Lorem text, and the stars overlap the price. (00:48.0; 0048.0, 0054.0)
8. The Card is selected and shows W 433 and H 597, but the rendered card is visibly narrower, with the stars squeezed together. The panel and the canvas disagree. (00:57.0; 0057.0)

Expected (implied): Hug and Fill containers recompute their size and child positions immediately after a child is removed or the parent is resized. No stale gaps or overlaps should remain, and the displayed values should match the rendering.

Actual: After deleting the tags Board, TextWrapper and the Card keep their old height until the sizing is toggled again, leaving a blank gap. After resizing, the children overlap (text over text, stars over price). The panel reports W 433 for the Card while the rendered card is narrower.

Key events: 0012.0, 0018.0, 0048.0, 0057.0

Missed by the author:

- The gap after Board removal only closes after the Card's vertical sizing control is clicked (0018.0 to 0024.0).
- TextWrapper reports H 196.5 after the removal, but its content is shorter, so the height is stale (0012.0, 0039.0).
- At 0057.0 the design panel shows W 433 while the rendered card is narrower.

Claims:

- "Hug and Fill settings do not update correctly even though they appear applied in the UI" [The Hug and Fill settings do not update correctly, even though they appear as applied in the UI.]: confirmed - The gap stays after the removal (0012.0–0018.0). The panel shows W 433 while the canvas is narrower (0057.0).
- "The problem is triggered by removing an element or extending the card content" [Trigger different interactions (e.g. remove an element or extend the card content).]: confirmed - The Board removal is inferred from the missing layer (0012.0). Card resizing is visible at 0033.0–0057.0. The video does not show extending the content.
