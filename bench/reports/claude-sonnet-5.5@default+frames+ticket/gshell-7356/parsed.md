# real/gshell-7356

_claude-sonnet-5.5@default, 24 s; looked at: frames, frames/0000.0.jpg, frames/0002.0.jpg, frames/0003.0.jpg, frames/0004.0.jpg, frames/0005.0.jpg, frames/0006.0.jpg, frames/0007.0.jpg, frames/0009.0.jpg_

In an RTL GNOME Shell session the Quick Settings menu is open on the left. When the VPN toggle is turned on, a VPN icon is added to the panel and the whole menu jumps about 14 px to the right. It jumps back when VPN is turned off. The menu moves under the pointer, which makes it hard to click and is an accessibility problem.

## Quick Settings menu shifts horizontally when a panel icon appears or disappears (RTL)

Class: **wrong-data**

Environment: GNOME Shell, RTL layout (status area at the top left). Quick Settings menu with Tether (iPhone), Wi-Fi (Rogers01840), Power Mode (Balanced), VPN (Proton VPN CA), Dark Style and 4 Background Apps. Battery at 85%. No version is visible.

Steps:

1. Open the Quick Settings menu from the panel status area. The menu is anchored at the left edge, with its left side at about x=60. This is inferred: the click itself is not visible, but the menu is open by 2.0 s. (00:02.0; 0002.0)
2. Click the VPN toggle. The VPN tile turns blue and a VPN icon appears in the panel. The menu jumps right by about 14 px (left edge from about 60 to 74) and the panel icons shift as well. (00:03.0; 0002.0, 0003.0)
3. Click the VPN toggle again to turn it off. The VPN icon disappears from the panel and the menu returns to its original position. (00:05.0; 0004.0, 0005.0, 0006.0)
4. Turn VPN on again. The icon reappears and the menu shifts right again. The pointer is now over a different part of the tile, because the layout has moved under it. (00:07.0; 0007.0, 0009.0)

Expected (implied): The open Quick Settings menu stays in place when a status icon is added to or removed from the panel.

Actual: The menu moves about 14 px horizontally each time the VPN icon appears or disappears. This happens while the menu is open and the pointer is on it, so controls move under the pointer.

Key events: 0002.0, 0003.0, 0005.0, 0007.0

Missed by the author:

- The shift reverses when the icon is removed (0005.0), so it occurs in both directions.
- The VPN tile icon changes between frames (0007.0 vs 0009.0) while the menu is shifting. The panel icon also changes to a different glyph at 9.0 s.

Claims:

- "The menu changes position when an icon is added to the panel after the toggle is activated, e.g. a VPN icon." [seems to occur when an icon gets added in the panel after the toggle is activated, in my case when a VPN icon appears]: confirmed - The menu shifts right at 3.0 s and 7.0 s when the VPN icon appears. It returns at 5.0 s when the icon disappears.
- "This happens in RTL." [in RTL (ticket title)]: confirmed - The status area and menu are anchored at the left, which is consistent with RTL. No language setting is shown, so this is inferred from the layout.
