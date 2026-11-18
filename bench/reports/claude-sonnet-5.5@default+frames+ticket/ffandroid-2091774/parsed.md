# real/ffandroid-2091774

_claude-sonnet-5.5@default, 46 s; looked at: frames/0000.0.jpg, frames/0003.0.jpg, frames/0006.0.jpg, frames/0009.0.jpg, frames/0012.0.jpg, frames/0015.0.jpg, frames/0018.0.jpg, frames/0021.0.jpg, frames/0024.0.jpg, frames/0001.0.jpg, frames/0002.0.jpg, frames/0027.0.jpg, frames/0030.0.jpg, frames/0033.0.jpg, frames/0036.0.jpg, frames/0040.0.jpg, frames/0045.0.jpg, frames/0002.5.jpg, frames/0028.5.jpg, frames/0029.0.jpg, frames/0029.5.jpg, frames/0038.0.jpg, frames/0043.0.jpg, frames/0003.5.jpg, frames/0037.0.jpg, frames/0037.5.jpg_

On a Nightly Android build, the recording toggles the VPN row in the main menu from the home page and from a Mullvad page. The VPN row goes straight between 'Off' and 'On'. No frame shows the 'Connecting' label, so the video neither shows nor disproves that it flashes too briefly to read. At a 0.5 s step it is gone before any frame catches it.

## VPN menu row: 'Connecting' state not visible (or too brief to read) when toggling VPN from Off to On

Class: **not-a-bug**

Environment: Firefox Nightly for Android, signed in as <email>. Screens: the main menu over the Firefox home page (HNT), the main menu over mullvad.net/en, and the site Trust Panel on mullvad.net. The device model and OS are not visible; the ticket names a Pixel 7a and a Galaxy S24.

Steps:

1. The main menu is open over the home page. The VPN row shows 'On' with a purple pill. (00:00.0; 0000.0, 0001.0)
2. Inferred tap on the VPN row's toggle pill. A touch ripple is visible on it. (00:02.0; 0002.0, 0002.5)
3. The row now reads 'Off' and stays 'Off' for the next few seconds. No 'Connecting' text appears in any frame between 'On' and 'Off'. (00:03.0; 0003.0, 0003.5, 0006.0)
4. The menu is dismissed and the mullvad.net page is opened. The Trust Panel shows VPN 'Off'. (00:12.0; 0012.0, 0015.0, 0018.0)
5. The main menu is opened over mullvad.net with VPN 'Off'. After a pause of about 9 s, the toggle is tapped (inferred from the next frames). (00:27.0; 0027.0)
6. The row jumps to 'On' and the address bar shows a 'VPN on' pill. The row is never seen in a 'Connecting' state. (00:28.5; 0028.5, 0029.0, 0030.0)
7. The VPN is toggled back to 'Off' (the address bar pill reads 'VPN off'), then to 'On' again at about 37.5 s. Again no 'Connecting' text is visible in the sampled frames. (00:29.5; 0029.5, 0036.0, 0037.0, 0037.5)

Expected (implied): After the toggle is tapped, 'Connecting' is shown long enough to read, or not shown at all if the connection is instant (from the ticket).

Actual: In the sampled frames the VPN row goes directly between 'Off' and 'On'. No 'Connecting' text is visible. The ticket says it flashes for a very short time. This is not confirmed visually, but a flash shorter than 0.5 s would be consistent with the frames.

Key events: 0002.0, 0003.0, 0028.5, 0037.0, 0037.5

Missed by the author:

- The first toggle at 0002.0 goes from 'On' to 'Off', the opposite direction to the ticket's repro. The ticket says to start with the VPN off.
- The address bar 'VPN on' and 'VPN off' pill appears at about 0029.0 and 0029.5, so a status label is visible there even though the menu row never shows 'Connecting'.

Claims:

- "'Connecting' appears briefly and then 'On' appears too quickly to read." [ticket: 'Connecting' shows for a very short time, then the expected 'On' state appears]: not shown - No frame at the 0.5 s step contains 'Connecting'. The state change from Off to On falls between 0037.0 and 0037.5. The label may have been shown for less than one frame.
- "It happens in the HNT, Trust Panel and existing-tab menus." [ticket: Open one of the menus: HNT, Trust Panel, or Existing Tab]: not shown - The video toggles VPN only in the HNT menu (0002-0003) and the existing-tab main menu (0027-0037). The Trust Panel (0015) is opened but the VPN is not toggled there.
- "The tester waits a few seconds before tapping." [ticket: Wait a few seconds ... Tap 'Off']: confirmed - The menu at 0027.0 sits for about 1 to 2 s before the toggle. At 0036.0 the toggle sits at 'Off' for several seconds before the tap.
