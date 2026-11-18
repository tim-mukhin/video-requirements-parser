# real/gshell-7356

_claude-sonnet-5.5@default, 22 s; looked at: frames/moments/p008.jpg, frames/moments/p017.jpg_

In an RTL GNOME Shell session, turning on VPN from the open Quick Settings menu adds a VPN icon to the panel. In the same frame the whole menu content jumps 14 px right under the pointer. This matches the ticket, and it makes toggles hard to hit.

## Quick Settings menu shifts 14 px when a VPN icon appears in the panel (RTL)

Class: **wrong-data**

Environment: GNOME Shell, panel status area at top left (RTL-like layout), keyboard layout indicators (en/it). Quick Settings: Tether (iPhone), Wi-Fi (Rogers01840), Power Mode (Balanced), VPN (Proton VPN CA), Dark Style, 4 Background Apps; battery 85%. No audio, no version shown.

Steps:

1. Open the Quick Settings menu from the panel status area (menu open at 1.5-2.6 s; the opening click is a panel click at 0.4 s/1.5 s). (00:01.5; p004, p005)
2. Click the VPN tile (Proton VPN CA). The tile turns blue and a VPN icon appears in the panel. In the same frame the menu content (area 53,42,427,357) moves 14 px right. (00:02.7; p006, p007, p008, p009)
3. Panel icons then shift 28 px in one frame at 3.2 s, after the icon change. (00:03.2; p010, p011)
4. Repeat: reopen the menu and click the VPN tile. At 5.3 s the click is followed by a 28 px panel shift and the menu fading out. At 7.5 s the click on the tile is followed by another 28 px panel shift. The VPN panel icon changes each time, so the layout moves again. (00:07.5; p015, p017, p021, p022, p023)

Expected (implied): The open Quick Settings menu stays in place when a status icon is added to or removed from the panel.

Actual: The menu content jumps 14 px horizontally in a single frame when the VPN icon is added. The panel icons also shift by 28 px when icons change. The controls move under the pointer.

Key events: p006, p007, p008, p010, p017, p022

Missed by the author:

- The menu jumps in the same frame as the VPN icon appears, not afterwards (p007, p008).
- The panel itself shifts 28 px in separate steps (p010, p017, p022).
- In the span checked (2.7-7.5 s) the video does not clearly show the VPN toggle turning off with the menu staying open. At 5.3 s the menu fades out (p017 moment). The watcher's note that the menu 'returns' at 5.0 s is therefore not confirmed.

Claims:

- "The menu changes position when an icon is added to the panel after the toggle is activated (VPN icon)." [ticket]: confirmed - p008 moment shows the menu jump right in the frame where the VPN icon appears (p007).
- "It happens in RTL." [ticket]: not shown - No language or direction setting is visible. The status area is at the top left, which is consistent with RTL.
- "Reproducible by the ticket author too." [ticket]: not shown - The video has no speech. It shows one session.
