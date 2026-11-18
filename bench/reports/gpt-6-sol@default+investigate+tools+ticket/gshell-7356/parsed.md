# real/gshell-7356

_gpt-6-sol@default, 56 s; looked at: frames/moments/p008.jpg, frames/moments/p010.jpg, frames/moments/p017.jpg, frames/moments/p022.jpg, frames/0002.5.jpg, frames/0003.0.jpg, frames/0003.5.jpg, frames/0004.0.jpg, frames/0004.5.jpg, frames/0005.5.jpg, frames/0006.5.jpg, frames/0007.0.jpg, frames/0007.5.jpg, frames/0008.0.jpg, looks/0006.80-0007.90-0_0_490_405/sheet.jpg, frames/000198.jpg, frames/000208.jpg, frames/000228.jpg, frames/000084.jpg_

Enabling Proton VPN shifts the still-open GNOME Quick Settings menu about 14 pixels to the right as a VPN indicator appears in the panel. Controls move while the user is interacting with the menu; the video establishes the timing, not the underlying cause.

## Quick Settings menu shifts when VPN indicator appears

Class: **silent-fail**

Environment: GNOME Shell Quick Settings in a left-side panel layout; Proton VPN CA and Wi-Fi network Rogers01840 are visible.

Steps:

1. Open Quick Settings from the panel indicators. (00:00.4; p001, p002)
2. Click the VPN tile to enable Proton VPN CA. (00:02.7; p006, p007)
3. Observe the open menu shift about 14 pixels right while the VPN indicator appears in the panel. (00:02.7; p008, p010)

Expected (implied): The open Quick Settings menu should remain in place when a setting adds a panel indicator.

Actual: The menu moves right without closing. After VPN is turned off, it remains shifted until it is closed and reopened.

Key events: p006, p008, p010, p012, p014, p015, p017

Missed by the author:

- The menu is still shifted after VPN is turned off; closing and reopening it restores its earlier position [p012, p014, p015, p017]. The timeline and frames settle this persistence, which the ticket does not mention.
- The watcher describes a second menu shift, but the timeline's later movement events concern panel indicators, and the inspected frames do not establish another menu shift [p021, p022].

Claims:

- "The Quick Settings menu changes position when changing settings." [ticket.md]: confirmed - The VPN tile is activated and the open menu shifts right [p006, p008].
- "The shift occurs because a VPN icon is added to the panel." [ticket.md]: not shown - The menu shifts during activation and the panel indicators change [p008, p010], but the video cannot establish the underlying cause.
- "The issue greatly affects accessibility." [ticket.md]: not shown - The moving controls are visible, but no specific accessibility failure is demonstrated.
