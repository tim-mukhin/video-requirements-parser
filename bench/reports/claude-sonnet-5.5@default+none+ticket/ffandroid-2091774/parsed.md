# real/ffandroid-2091774

_claude-sonnet-5.5@default, 15 s; looked at: nothing_

In Firefox Nightly on Android, tapping "Off" in the VPN menus (HNT, Trust Panel, Existing Tab) shows "Connecting" for only a moment before the "On" state appears. The text can't be read, so the UI flickers. The ticket doesn't say whether the connection itself works correctly. It does, since the "On" state is reached.

## VPN 'Connecting' state flashes too briefly to read after tapping Off in IPProtection menus

Class: **intermittent**

Environment: Firefox Nightly 162.0a1 (Build 2016195671); Google Pixel 7a on Android 16; Samsung Galaxy S24 on Android 17. Signed in to VPN, VPN initially off. Menus: HNT, Trust Panel, Existing Tab.

Steps:

1. Sign in to VPN and make sure the VPN is turned off. (00:00.0; )
2. Open one of the menus: HNT, Trust Panel, or Existing Tab. (00:00.0; )
3. Wait a few seconds, about as long as the Shield animation in the address bar takes to finish. (00:00.0; )
4. Tap "Off". (00:00.0; )

Expected (speech): The "Connecting" state stays visible long enough to read, or is not shown at all if the connection is instant.

Actual: "Connecting" shows for a very short time, then the "On" state appears. The "Connecting" text disappears before it can be read.

Key events: 

Claims:

- "Rapid On/Off taps do not reproduce the issue; it only appears after waiting a few seconds before tapping." [Rapid On/Off taps do not reproduce it; it only appears when a few seconds are waited before tapping.]: not shown - No video is available, so this can't be checked from the ticket alone.
