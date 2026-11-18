# [IPProtection] 'Connecting' state disappears too quickly to read after tapping Off in VPN menus

Source: https://bugzilla.mozilla.org/show_bug.cgi?id=2091774  (reporter: <email>, filed 2026-11-11)

### Prerequisites
- Signed in to VPN
- VPN turned off

### Steps to reproduce
1. Open one of the menus: HNT, Trust Panel, or Existing Tab
2. Wait a few seconds (about as long as the Shield animation in the address bar takes to finish)
3. Tap "Off"

### Expected behavior
The "Connecting" state stays visible long enough to read, or is not shown at all if the connection is instant.

### Actual behavior
"Connecting" shows for a very short time, then the expected "On" state appears. The "Connecting" text disappears before it can be read.

### Device information
* Firefox version: Nightly 162.0a1 (Build #2016195671)
* Android device model: Google Pixel 7a; Samsung Galaxy S24
* Android OS version: Android 16 (Pixel 7a); Android 17 (Galaxy S24)

### Any additional information?
- Rapid On/Off taps do not reproduce it; it only appears when a few seconds are waited before tapping.
- See attached media;

## Reporter's follow-ups

[attachment: recording.mp4]
VPN Connecting flash screen recording
