# real/gshell-9522

_claude-sonnet-5.5@default, 28 s; looked at: frames/0006.0.jpg, frames/0015.5.jpg, frames/0012.5.jpg, frames/0014.0.jpg, frames/0017.0.jpg, frames/0004.5.jpg_

In GNOME Settings > Power, choosing Power Saver shows the banner "Performance mode temporarily disabled due to high operating temperature" while the Resources app beside it shows a normal 56–58 °C. Performance can still be selected right afterwards and the banner then goes away. The warning is misleading, because nothing is actually disabled.

## Power Saver selection shows a 'Performance mode temporarily disabled (high temperature)' banner at normal temperature; Performance stays selectable

Class: **wrong-data**

Environment: GNOME Settings > Power (Power Mode list: Performance/Balanced/Power Saver) next to the Resources app (Processor page, Intel Core i5-10210U). Battery 70 %. Overview clock shows Nov 6 10:24 PM. The Fedora version and extension state are not visible in the video. No audio, so nothing was said.

Steps:

1. Settings > Power is open with Power Mode = Balanced and no banner. Resources shows 58 °C (highest 93 °C). (00:04.5; p012)
2. Select Power Saver (the click is inferred from the radio button changing). The banner appears under the list, while Resources shows 58 °C. (00:05.8; p015)
3. The banner stays for about 7.5 s while Resources shows 56–58 °C. (00:09.5; p015, p027)
4. Select Balanced. The banner disappears. (00:13.3; p038)
5. Select Performance. It becomes selected with no banner, so it was not disabled. (00:13.6; p039)
6. Repeat: Power Saver again shows the banner (Resources 67 °C). Then select Performance again, which works and removes the banner. Remaining time changes from 2 h 12 min to 1 h 58 min. (00:15.3; p043, p046, p049, p050, p052)

Expected (implied): No thermal warning at a normal CPU temperature. The banner should appear only when Performance is really unavailable because of thermal throttling.

Actual: Selecting Power Saver shows the "temporarily disabled due to high operating temperature" banner at 56–67 °C. It showed up on both of the two Power Saver selections in the video. Performance remains selectable, so the claim is false.

Key events: p015, p038, p039, p046, p052, p027

Missed by the author:

- The banner appeared on the second Power Saver selection too (p046), so it repeated.
- The banner disappears when Balanced or Performance is picked (p038, p052), so it is tied to the Power Saver selection.
- Resources shows 'Highest: 93 °C', so the CPU was hot earlier. The banner may reflect a stale thermal state, but the video cannot confirm this.
- Remaining time changes from 2 h 12 min to 1 h 58 min once Performance is selected (p050).

Claims:

- "The banner appears when choosing Power Saver" [ticket]: confirmed - It appeared at 5.8 s and again at 15.3 s, each time after Power Saver was selected.
- "The high-temperature condition is not true" [ticket]: confirmed - Resources shows 56–58 °C, and 67 °C at the second appearance. The 'Highest: 93 °C' is a past peak, so a stale thermal state is possible but not shown.
- "Performance can still be picked" [ticket]: confirmed - Performance was selected at 13.6 s and again at 16.1 s, and the banner went away.
- "Happens without extensions enabled" [ticket]: not shown - Extension state is not visible.
- "Fedora 45" [ticket]: not shown - No version is visible.
