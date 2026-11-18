# real/ff-2092119

_gpt-6-sol@default, 39 s; looked at: frames/0004.5.jpg, frames/0007.0.jpg, frames/0016.0.jpg, frames/0019.0.jpg, frames/0021.0.jpg, frames/moments/p137.jpg, frames/moments/p125.jpg, frames/0021.5.jpg, frames/0022.0.jpg, frames/0022.5.jpg, frames/moments/p056.jpg, frames/moments/p057.jpg, frames/0003.0.jpg, frames/0012.5.jpg_

Moving a selected Wikipedia region to a Firefox Mini Window opens the window at the article header instead of the selected paragraphs and diagram. A Monkeytype attempt shows the selected words briefly, then shows the page header, so the selected position is not reliably retained.

## Mini Window does not retain the selected page region

Class: **wrong-data**

Environment: Firefox on Windows; en.wikipedia.org and monkeytype.com. The ticket reports Firefox 160.0, but the version is not visible in the video.

Steps:

1. On the Wikipedia article, open the context menu and choose “Move Section to Mini Window.” (00:01.6; p005, p031)
2. With “Move selection” selected, draw a region around the middle article paragraphs and part of the diagram. (00:04.2; p031, p046, p050)
3. Choose “Move to Mini Window.” (00:05.7; p046, p055, p056)

Expected (implied): The Mini Window keeps the selected region visible rather than opening at another part of the page.

Actual: The Wikipedia Mini Window shows the Wikipedia header and article title, not the selected middle section [p066]. On Monkeytype, the window is initially blank [p126], briefly shows the selected words [p137], then shows the Monkeytype header [p144].

Key events: p031, p046, p050, p055, p066, p126, p137, p144

Missed by the author:

- “Move selection,” not the available “Move full tab” option, is selected [p031].
- The Monkeytype selection is resized to approximately 1,280 × 146 before submission [p102, p108].
- The Monkeytype Mini Window briefly displays the selected words before showing the page header [p137, p144].
- The ticket places the desired cropped-region behavior under “Actual results” and the reported failure under “Expected results”; the video supports the reverse [p050, p066].

Claims:

- "Selecting a region opens a Mini Window at another part of the page." [ticket: Expected results; on-screen caption [p067, p068]]: confirmed - The Wikipedia selection covers middle article content [p050], while the Mini Window shows the article header [p066].
- "The Mini Window contains the entire page and can be scrolled up and down." [ticket: Expected results]: not shown - Content outside the selection is visible, but the video does not show scrolling through the Mini Window.
- "The cropped selection is not shown." [on-screen caption [p129, p130]]: refuted - The Monkeytype Mini Window briefly displays the selected words [p137], though it later shows the page header [p144].
