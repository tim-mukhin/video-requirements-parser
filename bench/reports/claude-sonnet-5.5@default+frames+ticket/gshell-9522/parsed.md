# real/gshell-9522

_claude-sonnet-5.5@default, 32 s; looked at: frames, frames/0000.0.jpg, frames/0003.0.jpg, frames/0006.0.jpg, frames/0009.0.jpg, frames/0012.0.jpg, frames/0015.0.jpg, frames/0018.0.jpg, frames/0021.0.jpg, frames/0004.5.jpg, frames/0005.5.jpg, frames/0013.5.jpg, frames/0019.5.jpg, frames/0013.0.jpg_

In GNOME Settings > Power, selecting Power Saver shows an info banner saying 'Performance mode temporarily disabled due to high operating temperature'. The Resources app beside it reads 56–58 °C, and Performance can still be selected afterwards. The banner contradicts the screen and the ticket, so it looks like a wrong thermal-throttle message.

## Power Saver selection shows 'Performance mode temporarily disabled due to high operating temperature' while temperature is normal and Performance remains selectable

Class: **wrong-data**

Environment: GNOME Shell on Fedora (per ticket; the video does not show the version). Settings > Power next to the Resources app (Intel Core i5-10210U, 70% battery). The overview at 21.0 s shows Nov 6, 10:24 PM, and a screen-recording indicator is on.

Steps:

1. Open Settings > Power with Power Mode = Balanced. No banner is shown. The Resources Processor page shows about 56–60 °C. (00:03.0; 0003.0, 0004.5)
2. Click 'Power Saver' (inferred from the radio button changing). The banner 'Performance mode temporarily disabled due to high operating temperature' appears under the list. (00:05.5; 0005.5, 0006.0)
3. Leave the banner on screen. Resources keeps showing a normal temperature (56–58 °C, highest 93 °C). (00:09.0; 0009.0, 0012.0)
4. Click 'Balanced' (inferred). The banner disappears. (00:13.0; 0013.0)
5. Click 'Performance' (inferred). It becomes selected and no banner is shown, so Performance was not actually disabled. (00:15.0; 0015.0, 0018.0)

Expected (implied): No 'performance mode disabled due to high temperature' notice when the CPU temperature is normal. The notice should appear only when the system is actually thermally throttled.

Actual: Choosing Power Saver shows the thermal-disabled banner while the CPU is at about 56–58 °C, and Performance can still be selected afterwards.

Key events: 0003.0, 0006.0, 0012.0, 0015.0

Missed by the author:

- The banner disappears once Balanced is selected, so it is tied to the Power Saver selection (0013.0).
- The 'Highest: 93 °C' in Resources shows the CPU was hot earlier in the session. The banner may reflect a stale or latched thermal state (the most likely candidate), but the video cannot confirm this.
- Time remaining changes from 2 h 12 min to 1 h 58 min once Performance is selected (0018.0).

Claims:

- "The banner appears when choosing Power Saver" [pick power saver mode]: confirmed - The banner appears at 5.5–6.0 s right after Power Saver is selected.
- "The high-temperature condition is not true" [despite that not being the case]: confirmed - Resources shows 56–58 °C while the banner is visible. The 93 °C 'Highest' value is a past peak.
- "The user can still pick performance mode" [it doesnt really stop me from picking the performance mode anyways]: confirmed - Performance is selected at 15.0 s and stays selected through 21.0 s.
- "Reproduces without extensions" [happens even without any extensions being enabled]: not shown - The video does not show whether extensions are enabled.
- "Reproduced on Fedora 45" [Affected version Fedora 45]: not shown - No version information is visible.
