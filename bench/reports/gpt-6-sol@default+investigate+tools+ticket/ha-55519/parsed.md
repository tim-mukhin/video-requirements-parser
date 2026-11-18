# real/ha-55519

_gpt-6-sol@default, 47 s; looked at: frames/0004.0.jpg, frames/0025.0.jpg, frames/0028.0.jpg, frames/0032.0.jpg, frames/0060.0.jpg, frames/0063.0.jpg, frames/moments/p049.jpg, frames/moments/p155.jpg, frames/moments/p251.jpg, frames/0061.0.jpg, frames/0064.0.jpg, frames/0065.0.jpg, frames/moments/p238.jpg, frames/moments/p246.jpg, frames/0070.0.jpg, frames/0073.0.jpg, frames/0076.0.jpg, frames/0079.0.jpg, frames/moments/p002.jpg, frames/moments/p040.jpg, frames/0007.0.jpg, frames/0012.0.jpg, frames/0033.0.jpg, frames/0043.0.jpg_

The Add condition chooser in the Presence automation responds slowly: a click on By type takes about 2.7 seconds to show its list, while a later switch to Blocks takes about 0.3 seconds. Clicks on Night Lux also leave the pane saying “Select a target,” making it difficult to choose a condition. The video supports the reported sluggishness but does not establish that the clicks were lost.

## Add condition chooser is slow and sometimes gives no visible response to selection

Class: **stuck**

Environment: Home Assistant desktop window on macOS, editing the Presence automation. The ticket identifies a Safari WebKit PWA, macOS 15.8.1, Safari 27.0 and Home Assistant Core 2026.11.0b2; those versions are not visible in the video.

Steps:

1. In the Presence automation, open Add condition; the chooser opens on By target. (00:04.3; p003, p006)
2. Click Night Lux in the target list; the adjacent pane remains on “Select a target.” (00:24.8; p055, p056, p057)
3. Click By type; its condition list appears about 2.7 seconds later. (01:00.4; p201, p204, p205, p209)

Expected (implied): The chooser should respond promptly to clicks and allow a condition to be selected.

Actual: After the By type click at 60.4 seconds, By target remains displayed until the By type list appears at 63.1 seconds. Clicking Night Lux at 24.8 seconds produces a brief tooltip, but the adjacent pane still says “Select a target.” By contrast, clicking Blocks at 70.2 seconds displays its list at 70.5 seconds [p235, p236].

Key events: p006, p055, p056, p057, p061, p201, p204, p205, p235, p236

Missed by the author:

- A CPU menu opened during the stalled chooser shows Home Assistant Web Content at 110.7% process usage [p061]; this is an observation, not proof of the cause.
- The chooser does eventually switch to By type [p204, p205], and a subsequent Blocks click responds much faster [p235, p236].
- The timeline's supposed errors at [p146, p234] are ordinary tab labels, not error messages; frames settle the ambiguity. Its apparent value reversion at [p191] is the entity list scrolling, as the moment frames around [p155] show.

Claims:

- "Adding a condition makes the frontend unusably slow." [ticket: Describe the issue you are experiencing]: confirmed - The chooser takes about 2.7 seconds to show By type after a recorded click [p201, p204]; it does eventually respond.
- "Some mouse clicks are not registered." [ticket: Additional information]: not shown - Recorded Night Lux clicks do not open a condition pane [p055, p148, p249], but the video cannot establish whether the application discarded the clicks rather than responding differently.
- "The issue does not reproduce in Opera." [ticket: Additional information]: not shown - No Opera comparison appears.
- "The installation has a lot of entities." [ticket: Steps to reproduce the issue]: not shown - An entity list is visible, but its total size is not established.
- "The browser console shows no JavaScript errors." [ticket: JavaScript errors shown in your browser console/inspector]: not shown - The console is not visible.
