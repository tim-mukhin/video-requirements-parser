# real/gshell-7356

_claude-sonnet-5.5@default, 23 s; looked at: frames/000098.jpg, frames/000161.jpg, frames/000228.jpg, frames/000046.jpg, frames/000084.jpg, frames/000208.jpg_

The author toggles the VPN tile in the GNOME quick-settings menu. The first attempt shows a connecting indicator and then drops back to off with no error. The second attempt connects (lock icon), and a third click turns it off. The video has no audio and no explanation, so the failure is only visible as a revert.

## VPN (Proton VPN CA) toggle reverts to off after first connect attempt, no error shown

Class: **intermittent**

Environment: GNOME Shell quick settings menu (top panel), Wi-Fi Rogers01840 connected, Tether iPhone, VPN entry 'Proton VPN CA', battery 85%. No audio.

Steps:

1. Open the system menu from the top panel; the VPN tile is off (slashed icon). (00:01.5; p004, p005)
2. Click the VPN tile. It turns blue with a connecting indicator. (00:02.7; p006, p007)
3. About 0.5 s later the tile returns to off with the slashed icon. No error is shown. (00:03.2; p009)
4. Click the VPN tile again. It shows connecting again, then connected with a lock icon at 6.9 s. (00:05.3; p013, p014, p017)
5. Click VPN again. The tile returns to off. (00:07.5; p018, p019)

Expected (implied): Clicking the VPN tile connects the VPN and keeps it connected, or shows an error if it cannot connect.

Actual: The first connect attempt silently reverts to disconnected within about 0.5 s. The second attempt connects. A later click turns it off, which is probably the user disconnecting, but the click at 6.5 s landed on the lock button, so the sequence is not fully clear.

Key events: p007, p009, p013, p017, p018, p019

Missed by the author:

- The connecting indicator flashes for only about 1.5 s and then reverts silently (p007, p009).
- The clicks at 4.2 s and 6.5 s landed in other places: the click at [92,30] is followed by a screen change to blank (p010, p011), and the click at 6.5 s hit the lock button area (p015, p016). The cursor is not followed after 7.8 s, so the end state is not confirmed.
