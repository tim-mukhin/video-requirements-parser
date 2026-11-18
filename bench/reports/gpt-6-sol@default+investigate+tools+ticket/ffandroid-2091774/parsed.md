# real/ffandroid-2091774

_gpt-6-sol@default, 107 s; looked at: frames, frames/0040.5.jpg, frames/0041.0.jpg, frames/0041.5.jpg, frames/0000.0.jpg, frames/0003.0.jpg, frames/0014.0.jpg, frames/moments/p079.jpg, looks/0040.80-0041.50-270_395_185_69/sheet.jpg, looks/0003.90-0004.60-260_615_195_75/sheet.jpg, looks/0015.40-0016.00-265_605_190_75/sheet.jpg, frames/0037.5.jpg, frames/moments/p083.jpg, frames/moments/p061.jpg, frames/moments/p040.jpg, frames/0032.5.jpg, frames/0033.0.jpg, frames/0004.0.jpg_

Firefox Nightly briefly displays “Connecting” when VPN is switched from Off to On, then replaces it with “On” about one frame later. Frame-by-frame inspection confirms the flash in the homepage menu, Trust Panel, and existing-tab menu; the timeline’s OCR missed the brief label.

## VPN “Connecting” label disappears almost immediately after tapping Off

Class: **intermittent**

Environment: Firefox Nightly on Android, signed in as <email>. The recording shows the homepage menu, Trust Panel, and an existing-tab menu over mullvad.net/en. The ticket names Nightly 162.0a1, Pixel 7a and Galaxy S24, and Android 16 and 17; those device and build details are not visible.

Steps:

1. Open the menu on the mullvad.net/en tab (tap the three-dot control); its VPN row is visible. (00:23.6; p070, p071)
2. Tap VPN On to turn it Off. (00:38.4; p102, p103, p105)
3. After leaving the menu open for a few seconds, tap VPN Off to turn it On. The touch mark and “Connecting” are visible in the 41.039 s frame. (00:41.0; p105, p106, p107)

Expected (implied): Keep “Connecting” visible long enough to read, or go directly to “On” if connection is effectively instant.

Actual: At 41.039 s the VPN row reads “Connecting”; by 41.063 s it reads “On”. Frame-by-frame inspection also finds the same brief transition at 4.204 s in the homepage menu and 15.706 s in the Trust Panel. The VPN does reach the displayed On state.

Key events: p019, p021, p035, p036, p046, p047, p070, p071, p102, p103, p105, p106, p107

Missed by the author:

- The brief label also appears during a rapid Trust Panel toggle [p046, p047]; waiting several seconds is not necessary in that observed attempt.
- The mullvad.net page says “Not using Mullvad VPN” while Firefox’s control says On [p107]. The recording does not establish whether the page refreshed or whether its message describes the same VPN service.
- The timeline’s apparent address-bar reversions, including [p092], are the temporary “VPN on/off” badge disappearing; the page remains mullvad.net/en.

Claims:

- "“Connecting” appears very briefly before “On.”" [ticket: Actual behavior]: confirmed - The 41.039 s frame shows “Connecting” and the 41.063 s frame shows “On”; the half-second frames alone could not establish this duration.
- "The issue occurs in the homepage menu, Trust Panel, or existing-tab menu." [ticket: Steps to reproduce]: confirmed - Frame-by-frame inspection captures the label in all three surfaces, at 4.204 s, 15.706 s, and 41.039 s respectively.
- "Rapid On/Off taps do not reproduce it; waiting a few seconds is required." [ticket: Any additional information?]: refuted - After the 15.5 s tap changes VPN from On to Off [p046, p047], an Off-to-On transition shows “Connecting” at 15.706 s—well under a few seconds later.
- "VPN was already off at the start of the recording." [ticket: Prerequisites]: refuted - The homepage VPN row initially reads On [p010, p019].
- "The recording establishes the listed Firefox build, phone models, and Android versions." [ticket: Device information]: not shown - Those details appear in the ticket, not on screen.
