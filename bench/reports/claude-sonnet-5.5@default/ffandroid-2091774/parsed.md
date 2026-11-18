# real/ffandroid-2091774

_claude-sonnet-5.5@default, 25 s; looked at: frames/000380.jpg, frames/001198.jpg, frames/000456.jpg_

In Firefox Nightly on an Android phone, the built-in VPN toggle is switched repeatedly. The toolbar badge and the menu toggle keep flipping between 'VPN on' and 'VPN off' about every 1.5 s, with no tap shown before most flips. Even while the badge says 'VPN on' and Firefox says 'You're protected', mullvad.net shows 'Not using Mullvad VPN'. The video has no audio, so there is no author commentary.

## Firefox VPN state flaps on/off every ~1.5 s and mullvad.net reports 'Not using Mullvad VPN' while the badge says 'VPN on'

Class: **intermittent**

Environment: Firefox Nightly on a portrait Android-like device. Signed in as <email>. Page: mullvad.net/en (Sofia, Bulgaria). Surfaces used: the three-dot menu with its VPN toggle and the site-info panel with its VPN toggle. Two tabs open. Taps are visible only as touch marks, and only some of them are drawn.

Steps:

1. Open the Firefox menu and tap the VPN toggle ('On'). It changes to 'Off', then back to 'On' about 1.4 s later. (00:00.3; p019, p020, p021, p022)
2. Open mullvad.net/en. The toolbar badge shows 'VPN on', but the page banner says 'Not using Mullvad VPN'. (00:09.3; p035, p037, p038)
3. Open the site-info panel, which shows 'You're protected' and the VPN toggle 'On'. Tap the toggle. (00:10.5; p039, p040, p041)
4. The badge alternates 'VPN off' and 'VPN on', each lasting about 1.4 s, and reverts to plain 'mullvad.net/en' between them. The toggle label flips On and Off in step. This repeats for about 30 s, including after taps in the three-dot menu. (00:12.1; p042, p044, p047, p051, p053, p079, p082, p086, p091, p094, p096, p106, p110, p113)
5. The page banner still reads 'Not using Mullvad VPN' while the badge says 'VPN on'. (00:31.0; p088, p093)

Expected (implied): One tap switches the VPN once and it stays in that state. The toolbar badge, the toggle and the Mullvad page banner agree with each other.

Actual: The VPN badge and toggle flip On/Off on a roughly 1.5 s cycle, often with no tap shown just before. They also flip back after taps. The Mullvad page reports 'Not using Mullvad VPN' while the badge says 'VPN on' and the panel says 'You're protected'.

Key events: p019, p020, p021, p022, p037, p040, p041, p042, p044, p047, p051, p053, p092, p096, p110, p113, p114

Missed by the author:

- The page banner 'Not using Mullvad VPN' contradicts the 'VPN on' badge and 'You're protected' (p037, p040).
- Badge text reverted to plain 'mullvad.net/en' with no click before it, for example after 1.4 s (p092, p055).
- The toggle label flashed 'Off' for 0.5 s (p101) and 'HO' for 0.2 s (p105) around taps, which suggests the state is changing between taps.
