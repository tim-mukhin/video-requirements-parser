# real/gshell-9532

_claude-sonnet-5.5@default, 23 s; looked at: frames/0020.5.jpg, frames/0021.5.jpg_

The recording shows the GNOME Shell overview and workspace switching being toggled repeatedly. During the transitions the screen shows mixed states: the workspace strip is clipped, the search bar and dock are half-drawn, and workspace windows are still full size while overview widgets are visible. The video ends on a clean desktop, so the ticket's 'stuck between 2 states' is not shown persisting.

## Overview/workspace switcher shows broken intermediate animation states when toggled during a workspace gesture

Class: **intermittent**

Environment: GNOME Shell on a 1920x1200 screen (ticket says GNOME 51.1 on CachyOS; the video shows no version). Dock with an app-grid button, 13 Nov 11:46 clock, screen-recorder timer in the top bar, at least 2 workspaces with a wallpaper and a Zed/app grid. No accounts or orgs. No audio and no cursor or keys visible.

Steps:

1. Start in the overview and switch workspace; the workspace content slides sideways and the overview begins to close (trigger not visible; gesture or Super per ticket). (00:02.6; p015, p016, p018, p021)
2. The app grid appears (0:08 recorder time) and slides in/out; the overview is toggled again (trigger not visible). (00:09.2; p027, p028, p029)
3. Overview/app grid is toggled again and the layout slides (trigger not visible). Repeat: another workspace switch and overview toggle follow about every 2-3 s. (00:12.1; p034, p036, p038, p039)
4. Toggled during an animation, the screen shows a mixed state: the workspace strip is clipped by the left window, the search bar and dock are drawn over the two windows, and the dock's app-grid icon is partly faded to three dots. (00:20.5; p040, p041, p042, p043)
5. The animation ends on the plain desktop. There is no persisting stuck state. (00:21.2; p045)

Expected (implied): Pressing Super in the middle of a workspace gesture animation should end in a consistent state (overview fully open or fully closed) with a smooth animation and no clipped or half-faded elements.

Actual: Toggling the overview mid-gesture produces inconsistent intermediate visuals, e.g. at about 20.5 s, with the strip clipped and the dock and search bar half-drawn. The last frame (21.5 s) is a clean desktop, so the video does not show a persistent stuck state.

Key events: p021, p027, p029, p034, p039, p043, p045

Missed by the author:

- The video has no narration. It does not show which gesture or key was used, or whether the stuck state occurred at all.
- The dock's app-grid icon is drawn as three dots mid-transition (frame 0020.5, near p041).

Claims:

- "The switcher can be left stuck between 2 states" [ticket]: not shown - Only transient mixed states are seen. The video ends on a normal desktop (frame 0021.5).
- "Weird animations throughout" [ticket title]: confirmed - Many MOVED/FLICKER events and clipped or half-faded strip, dock and search bar (frame 0020.5).
- "Pressing Super during the gesture animation triggers it" [ticket]: not shown - No keys or cursor are visible. Overview changes follow no visible input.
