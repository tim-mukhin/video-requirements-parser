# real/bitwarden-6923

_gpt-6-sol@default, 32 s; looked at: frames/moments/p002.jpg, frames/moments/p009.jpg, frames/0001.0.jpg, frames/0007.5.jpg, frames/0009.0.jpg, frames/0011.0.jpg, frames/0000.0.jpg, frames/0003.5.jpg, frames/0004.0.jpg, frames/0006.5.jpg, frames/0008.0.jpg, frames/0010.5.jpg, frames/0012.5.jpg, frames/0016.5.jpg_

Toggling Bitwarden from its macOS menu bar icon can hide the window without returning focus to QuickTime Player. An earlier toggle does return focus, so the video shows inconsistent behavior.

## Hiding Bitwarden from the menu bar can leave Bitwarden focused

Class: **intermittent**

Environment: macOS; Bitwarden settings window, QuickTime Player and a Mac App Store page listing Bitwarden 2023.10.1.

Steps:

1. With Show menu bar icon, Minimise to menu bar, Close to menu bar and Start to menu bar already enabled, leave the Bitwarden window hidden while QuickTime Player is active. (00:06.3; p003, p008)
2. Click the Bitwarden menu bar icon to show its window. (00:07.0; p010, p011, p012)
3. Toggle the icon again while the window is open; the window hides, but Bitwarden remains active. (00:07.9; p013)

Expected (implied): The window hides and focus returns to the previously active app.

Actual: At 7.9 s the window is hidden but the menu bar still names Bitwarden. This recurs at 9.0, 10.8 and 12.3 s [p013, p016, p019, p022]. In contrast, the window hides and focus returns to QuickTime Player at 3.8 and 6.3 s [p005, p008].

Key events: p003, p005, p008, p010, p012, p013, p016, p019, p022

Missed by the author:

- The settings also show Always show in the Dock unchecked [p003].
- The video shows a successful return of focus to QuickTime Player at 3.8 and 6.3 s, contrasting with the later failed toggles [p005, p008, p013].

Claims:

- "The four menu bar settings are enabled." [ticket.md]: confirmed - The settings are checked on screen [p003]; the video does not show the reporter enabling them.
- "A rapid second click sometimes leaves the window open." [ticket.md]: not shown - The window remains open early in the recording, but no second click is established during that interval [p003, p005].
- "Around 9 seconds the window closes without returning focus to QuickTime Player." [ticket.md]: confirmed - At 9.0 s the window is hidden while Bitwarden remains the active app [p016].
- "The issue persisted across reinstalls and multiple client and macOS versions." [ticket.md]: not shown - The video shows one recording, not installation or version history.
