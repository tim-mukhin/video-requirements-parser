# real/gshell-9532

_claude-sonnet-5.5@default, 22 s; looked at: frames/000121.jpg, frames/000197.jpg, frames/000276.jpg_

A silent screen recording of a GNOME-style desktop (GShell). The view goes from the app grid, to the workspace switcher, back to the app grid, to the workspace switcher again, and finally to the empty desktop. No error, no wrong value and no failing action is visible, and nothing was said, so the problem the author meant to show is unclear.

## Unclear: only shell navigation between app grid, workspace view and desktop is shown; no visible defect

Class: **not-a-bug**

Environment: GNOME-style shell (GShell) at 1920x1200, 13 Nov 11:46, screen recorder active. Four workspaces. The dock shows a browser, Obsidian, Files and a terminal. The app grid shows Zed, Blender, Discord, Spotify and others. The wallpaper is a Border Patrol / Pacifica scene. No accounts or organizations are visible.

Steps:

1. The app grid is open, with the search field and four workspace thumbnails above it. The trigger is not visible. (00:09.2; p001)
2. The view changes to the workspace switcher. The second workspace is highlighted and shown full size. The trigger is not visible. (00:15.1; p002)
3. The app grid appears again. The trigger is not visible. (00:17.0; p003)
4. The workspace switcher appears again. (00:19.4; p004)
5. The empty desktop is shown with the top bar only, and the second workspace pill is active. This is the end of the clip. (00:21.2; p005)

Expected (implied): Unknown. The author said nothing and no failure is shown. The most likely intent is that the overview, app grid and workspace transitions should work smoothly.

Actual: The shell moves between the app grid, the workspace switcher and the desktop. No error, missing icon, wrong value or stuck state is visible in the sampled frames. Only a few frames were captured, so a brief animation glitch or a transition delay cannot be ruled out. Judged from these frames, the likeliest candidate is a flicker or jump between the app grid and the workspace switcher (about 15-19 s), but this is not confirmed.

Key events: p001, p002, p003, p004, p005

Missed by the author:

- The app grid and the workspace switcher alternate twice within about 5 s (p002, p003, p004). If the author did not do this deliberately, it is worth checking.
