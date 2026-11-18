# real/gshell-9522

_gpt-6-sol@default, 33 s; looked at: frames/0005.0.jpg, frames/0006.0.jpg, frames/0013.0.jpg, frames/0014.0.jpg, frames/moments/p043.jpg, frames/moments/p049.jpg, frames/moments/p028.jpg, frames/moments/p014.jpg, frames/0013.5.jpg, frames/0015.5.jpg, frames/0016.5.jpg, frames/0005.5.jpg_

Selecting Power Saver in GNOME Settings displays a warning that Performance mode is temporarily disabled due to high operating temperature. The warning disappears after switching modes, and Performance can subsequently be selected, making the warning's relationship to the selected mode unclear; the video does not establish whether a thermal restriction exists.

## Power Saver selection displays a warning that Performance mode is disabled

Class: **wrong-data**

Environment: GNOME Settings > Power > General, beside Resources > Processor for an Intel Core i5-10210U. The ticket identifies Fedora 45, but the version is not visible in the video.

Steps:

1. In Settings > Power > General, start with Balanced selected. (00:04.0; p012)
2. Select Power Saver; the selection changes, though the activating click or key is not captured. (00:05.8; p014, p015, p016)

Expected (implied): Selecting Power Saver should not present a warning that Performance mode is disabled unless that restriction applies.

Actual: Power Saver is selected and the warning “Performance mode temporarily disabled due to high operating temperature” appears. It disappears after a mode change, returns with Power Saver selected again, and Performance is subsequently shown as selected.

Key events: p012, p015, p038, p039, p046, p049, p052

Missed by the author:

- Resources shows a recorded highest CPU temperature of 93 °C, so the video cannot rule out a thermal restriction (p015).
- The warning disappears after switching modes and reappears when Power Saver is selected again (p038, p046, p052). The timeline captures these changes, and the frames show their meaning.

Claims:

- "Choosing Power Saver displays the high-temperature Performance warning." [ticket:summary]: confirmed - The selected Power Saver row and warning are visible together at p015; the warning returns at p046.
- "High operating temperature is not the cause." [ticket:title]: not shown - Resources shows a current temperature around 57–58 °C when the warning appears, but also a recorded high of 93 °C. The thermal-restriction state is not shown.
- "The warning does not stop Performance from being selected." [ticket:summary]: confirmed - Performance is visibly selected after the warning at p039 and p049; the video does not measure delivered hardware performance.
- "This happens without extensions enabled." [ticket:affected-version]: not shown - Extension status is not visible.
