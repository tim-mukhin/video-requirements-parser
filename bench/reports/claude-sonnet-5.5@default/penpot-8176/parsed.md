# real/penpot-8176

_claude-sonnet-5.5@default, 28 s; looked at: frames/001837.jpg, frames/002493.jpg, frames/001469.jpg_

The video has no audio. In Penpot, a Card is built from nested flex layouts. When the author resizes the Card, the wrapped text in HeaderWrapper does not grow its container, so it overlaps the 'Text:' block below. The price and the star row also collide. The flex layout does not recompute after the resize.

## Flex layout does not re-flow after resizing the Card: wrapped text overflows its container and overlaps the next element

Class: **wrong-data**

Environment: Penpot design editor (Italian UI), page 'Bug 1', board 'Card' (flex). Its children are Image, TextWrapper > HeaderWrapper (Title, Text) and Text, then Divider, Wrapper and Button / ButtonFilled. The cursor is followed through 90% of the video. Clicks are inferred and keys are not seen.

Steps:

1. Select the Card board; it is 343 wide and 597 high. (00:31.6; p266, p267)
2. Drag the Card's right edge to widen it. The width changes from 343 to 433. (00:32.4; p279, p280, p295)
3. Select the Card again. (00:52.9; p446, p448)
4. Drag the right edge to narrow it. The width goes from 433 to 296.04, and the text re-wraps to three lines. (00:57.3; p462, p470, p473, p474)
5. The HeaderWrapper stays 94 high, so its three-line text overflows into the bold 'Text: Lorem ipsum...' block below. The star row also overlaps '00€'. (00:58.2; p475, p481)

Expected (implied): Flex containers resize to fit the re-wrapped text, so the paragraphs stack without overlapping. The price and stars stay separate.

Actual: After the resize, 'sed do eiusmod' sits on top of the 'Text:' block (frame 002493). HeaderWrapper keeps H 94 while its text needs more height. The stars are pushed against '00€'. An earlier wider state already showed HeaderWrapper H 116 and a later H 93.78, which do not match the text height.

Key events: p295, p311, p473, p474, p475, p410

Missed by the author:

- The author did not speak, so nothing is confirmed by narration.
- Many fields flash in the right panel for 0.1–0.9 s on every selection, for example the H 57 and Y 140 values (p037, p138, p323). These may be unrelated to the layout bug.
- The HeaderWrapper H value flips between 116 and 93.78 (p030, p306, p311) while the text is unchanged. The bounding box looks wrong.
