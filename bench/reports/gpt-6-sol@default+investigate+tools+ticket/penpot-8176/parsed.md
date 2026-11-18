# real/penpot-8176

_gpt-6-sol@default, 56 s; looked at: frames/0009.0.jpg, frames/0010.0.jpg, frames/0026.0.jpg, frames/0027.0.jpg, frames/0040.0.jpg, frames/0058.0.jpg, frames/0060.0.jpg, frames/0037.0.jpg, frames/0041.0.jpg, frames/0055.0.jpg, frames/0056.0.jpg, frames/0057.0.jpg, frames/0033.0.jpg, looks/0018.70-0019.00-790_280_290_360/sheet.jpg, looks/0050.70-0051.00-770_125_390_520/sheet.jpg, frames/moments/p472.jpg_

In Penpot’s Bug 1 card, narrowing the card makes its description wrap beyond the selected HeaderWrapper bounds while the wrapper still reports a height of 94. The overflow crowds the following “Text:” block; the video also shows a gap remaining after a tag row is removed until a layout control is changed.

## HeaderWrapper height stays stale when card text reflows

Class: **silent-fail**

Environment: Penpot editor, Bug 1 page, Card with nested TextWrapper and HeaderWrapper. The ticket reports macOS and Chrome 143.0.7499.193; the video does not show the browser version.

Steps:

1. Remove the Board row containing the sporty, weekend and pink tags; the row disappears, but Card still shows H 645. (00:09.6; p099, p103, p112)
2. Select Card and click the Flex Board control that changes its height from 645 to 597. (00:26.6; p220, p221, p222)
3. With the card widened, select HeaderWrapper and click its height control; its displayed height changes from about 116 to 94. (00:40.2; p302, p304, p312, p319)
4. Narrow Card from width 433 to about 296 by dragging its right edge. (00:57.6; p456, p481, p482, p485)

Expected (implied): The HeaderWrapper should grow to contain the reflowed description and preserve spacing before the next text block.

Actual: At the wider width, the description fits inside HeaderWrapper. After narrowing, it extends below the selected bounds toward “Text:”, while the properties panel still shows H 94 [p304, p319, p482, p485]. The frames settle the visible overflow; the timeline supplies the control changes and dimensions.

Key events: p099, p112, p220, p222, p304, p319, p482, p485

Missed by the author:

- After the tag row disappears, Card still reads H 645; clicking a Flex Board control later changes it to H 597 [p099, p112, p220, p222].
- After narrowing, HeaderWrapper still reads H 94 although the description extends below its selected bounds [p319, p482, p485].

Claims:

- "Hug Content containers do not update correctly after layout changes." [ticket.md: Describe the bug]: confirmed - The selected HeaderWrapper retains H 94 after the narrower card makes its description extend beyond the wrapper [p319, p482, p485].
- "Fill containers also fail to update." [ticket.md: Steps to Reproduce, step 4]: not shown - The visible overflow establishes a stale HeaderWrapper height, not a separate Fill failure.
- "The failure is triggered by interactions." [ticket.md: Describe the bug]: not shown - The video shows edits in the design editor, including removal and resizing, rather than a running prototype interaction.
- "The recording was made on macOS in Chrome 143.0.7499.193." [ticket.md: Desktop]: not shown - Those details are reported in the ticket but are not visible in the editor recording.
