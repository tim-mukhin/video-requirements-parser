# real/commons-t146747-scroll

_gpt-6-sol@default, 50 s; looked at: frames/moments/p021.jpg, frames/moments/p065.jpg, frames/moments/p066.jpg, frames/0007.5.jpg, frames/0010.0.jpg, frames/0010.5.jpg, frames/0011.0.jpg, frames/0012.0.jpg, frames/0024.0.jpg, frames/0027.0.jpg, frames/000311.jpg, frames/000244.jpg, frames/000783.jpg, frames/000201.jpg, frames/000077.jpg, frames/000070.jpg, frames/000613.jpg, frames/000668.jpg, frames/000873.jpg, frames/000833.jpg, frames/moments/p033.jpg, frames/moments/p036.jpg, frames/0025.0.jpg, frames/0025.5.jpg, frames/0026.0.jpg, frames/moments/p011.jpg_

Opening a wikilink from a scrolled Wikipedia article can leave the destination far below its title, making readers scroll back to find the start. The video shows this with Pentobarbital; it does not establish that the destination position is calculated from the previous page's scroll position.

## Linked article opens below its beginning

Class: **state-revert**

Environment: German-language Wikipedia Android app. The ticket reports app version 2.3.152-r-2016-08-18, Android 6.0 and LG G4 H815; those details are not visible in the video.

Steps:

1. From the Hydromorphon article scrolled to “Sonstiges”, open the Pentobarbital link preview (the trigger is not visible). (00:04.7; p012, p014)
2. Open the full Pentobarbital article from its “ARTIKEL LESEN” preview (the trigger is not visible). (00:06.1; p014, p018)

Expected (implied): The newly opened article starts at its title.

Actual: At 7.5 s, the full Pentobarbital article is positioned at “Sicherheitshinweise” and “Verwendung”, well below its beginning [p018]. An upward scroll at 8.5 s [p021] brings its title into view at 9.5 s [p022].

Key events: p012, p014, p018, p021, p022, p067, p072

Missed by the author:

- The link opens a preview with a separate “ARTIKEL LESEN” action before the full article appears [p014].
- The later view of Pentobarbital at its title follows an upward scroll [p021, p022]; it is not evidence that the article initially opened there. The timeline settles the watcher’s contrary reading of the sampled frames.
- A later linked article, Technische Universität, is shown at its beginning [p067, p072], so the video does not support saying every link opens below the top.

Claims:

- "A new page opens somewhere below its beginning." [ticket: Actual results]: confirmed - Pentobarbital is shown below its title after opening [p014, p018].
- "The destination position is related to the former page's scroll position." [ticket: Actual results]: not shown - The source is scrolled, but the video does not establish how the two positions are related.
- "The recording uses the reported app version, Android version and device model." [ticket: Environments observed]: not shown - No version or device-details screen appears.
