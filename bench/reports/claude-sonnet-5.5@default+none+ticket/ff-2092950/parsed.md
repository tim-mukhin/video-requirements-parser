# real/ff-2092950

_claude-sonnet-5.5@default, 15 s; looked at: nothing_

In Firefox, dragging the thumb of a custom-shaped CSS range slider that has an output tooltip makes the thumb flicker. It happens mostly at high values, on the right side. The reporter says it needs the output element with a counter value, which suggests a rendering or layout interaction.

## Custom shape range slider with tooltip causes range-thumb to flicker

Class: **intermittent**

Environment: Firefox (version and OS not stated). Reproduced on CodePen demos: a full demo and a simplified one. The CSS for Chromium was removed from the simplified one. No accounts or organizations involved.

Steps:

1. Open the simplified CodePen demo (https://codepen.io/t_afif/pen/YPZMPre/e69d82ea69d78d1c100535d34f625128) in Firefox. (00:00.0; )
2. Drag the range thumb, especially towards high values on the right side. (00:00.0; )
3. Watch the thumb while dragging. (00:00.0; )

Expected (implied): The thumb moves smoothly while dragging, with no flicker.

Actual: The thumb flickers while it is dragged, mostly at high values on the right side. The reporter says the flicker only occurs when the output tooltip showing the counter value is present.

Key events: 

Claims:

- "The flicker happens mostly on the right side (high values)." [the flicker that happens mostly on the right side (high values)]: not shown - There is no video to check. The ticket text is the only source.
- "The output tooltip with the counter value is needed to trigger the flicker, not just the input." [the issue is not only related to the input. The output (the tooltip) needs to be present with the counter value to activate the flicker]: not shown - The claim rests on the reporter's reduction work. It was not verified here.
