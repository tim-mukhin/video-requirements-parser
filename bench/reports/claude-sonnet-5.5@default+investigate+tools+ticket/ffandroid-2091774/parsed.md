# real/ffandroid-2091774

_claude-sonnet-5.5@default, 247 s; looked at: looks/0003.90-0004.60-0_380_526_300/sheet.jpg, looks/0027.70-0027.90-0_380_526_120/sheet.jpg_

In the Firefox Nightly Android main menu, tapping the VPN row's Off toggle shows 'Connecting' for a single video frame (about 20 ms) before 'On' appears. The label can't be read. The video confirms the ticket's flash. The ticket expects it either to stay readable or not to be shown.

## VPN menu row: 'Connecting' flashes for one frame (~20 ms) after tapping Off, then 'On'

Class: **intermittent**

Environment: Firefox Nightly for Android, portrait 526x1170 screen recording, signed in as <email>. Menus seen: main menu over the Firefox home page (HNT) and main menu over mullvad.net/en. The device model and OS are not visible. The ticket names a Pixel 7a and a Galaxy S24, which the video does not confirm.

Steps:

1. Open the main menu on the home page (HNT) with the VPN row showing 'Off'. The video starts with 'On'; taps at 0.3 s switch it to 'Off' and the row stays 'Off' until about 4.1 s. (00:03.5; p019, p021)
2. Wait a few seconds, then tap the 'Off' pill. A ripple shows at 4.138 s. The row shows 'Connecting...' in exactly one frame at 4.204 s, then 'On' from 4.225 s. (00:04.2; p021)
3. Open the main menu over mullvad.net/en. The VPN row shows 'Off'. The tap at 24.9 s turned it from 'On' to 'Off', and the pill reads 'VPN off'. After a pause, tap 'Off' again. 'Connecting...' shows in one frame at 27.789 s (the frames at 27.725 and 27.807 s show 'Off' and 'On'), then the row reads 'On'. (00:27.8; p072, p076, p080)
4. Repeat in the same menu: further single-frame 'Connecting' hits at 32.489 s, 37.331 s and 41.039 s, next to the toggle taps at 31.3 s, 34.8 s and 38.4 s. These matched only by text search; I did not open their frames. (00:32.5; p089, p097, p102)

Expected (implied): 'Connecting' stays visible long enough to read, or is not shown if the connection is instant.

Actual: 'Connecting...' shows in one video frame, about 20 ms, and is replaced by 'On'. The 'On' toggle animation then slides in over about 0.3 s.

Key events: p021, p072, p080, p089, p097, p102

Missed by the author:

- The row is in the 'Connecting' state for only one frame (~20 ms), and a toggle animation slides in after it.
- The address-bar pill changes 'VPN off' / 'VPN on' and goes back to the bare URL (p076, p080, p082), a separate status indication.

Claims:

- "'Connecting' shows very briefly, then 'On'." [ticket]: confirmed - vrp find found 'Connecting' in one frame at 4.204 s and one at 27.789 s. I opened both frames: 'Off' → 'Connecting...' → 'On' within about 20 ms.
- "It reproduces in the HNT, Trust Panel and Existing Tab menus." [ticket]: not shown - Only the HNT menu (4.2 s) and the existing-tab menu over mullvad.net (27.8 s and later) were toggled. The Trust Panel (about 11 to 12 s) was opened but its VPN was not toggled.
- "A wait of a few seconds before the tap is required; rapid taps don't reproduce it." [ticket]: not shown - The video has no rapid-tap comparison. The toggles shown follow pauses, but the video does not test the rapid case.
- "The VPN starts Off." [ticket]: refuted - The video starts with the VPN 'On'. The first tap (0.3 s) turns it Off, and the repro starts from that Off state.
