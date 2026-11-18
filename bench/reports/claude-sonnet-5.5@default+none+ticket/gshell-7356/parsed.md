# real/gshell-7356

_claude-sonnet-5.5@default, 13 s; looked at: nothing_

In GNOME Shell with a right-to-left (RTL) language, the Quick Settings menu changes position when a new icon appears in the panel after a toggle is activated. The reporter saw it when a VPN icon appeared. The shifting menu moves under the pointer, which hurts accessibility.

## Quick Settings menu shifts when a new icon appears in panel in RTL

Class: **wrong-data**

Environment: GNOME Shell, RTL layout (from the ticket title). Quick Settings menu with a VPN toggle. The GNOME Shell version, distro, language and account are not given.

Steps:

1. Run GNOME Shell with an RTL language or layout. (00:00.0; )
2. Open the Quick Settings menu from the top panel. (00:00.0; )
3. Activate a toggle that makes a new icon appear in the panel, e.g. the VPN toggle. (00:00.0; )
4. Watch the menu's position as the new panel icon appears. (00:00.0; )

Expected (implied): The open Quick Settings menu stays where it is when a new panel icon appears.

Actual: The Quick Settings menu changes position when a new icon (e.g. VPN) is added to the panel after the toggle is activated.

Key events: 

Claims:

- "The menu changes position when settings are changed." [the quick settings menu changes position when changing settings]: not shown
- "It happens when an icon is added to the panel after a toggle is activated, e.g. a VPN icon." [seems to occur when an icon gets added in the panel after the toggle is activated]: not shown - There is no video. The reporter says they reproduced it, but only as a hypothesis ('seems to').
