# real/gshell-6725

_claude-sonnet-5.5@default, 19 s; looked at: frames/000086.jpg, frames/000136.jpg, frames/000189.jpg_

The author searches for Celluloid in GNOME Activities and opens it. An empty player window appears, and the top bar shows a loading spinner next to the app name. About 3 s later the window disappears and the empty desktop is left. No error is shown. The video has no audio and no visible cursor.

## Celluloid window closes by itself a few seconds after launch, with no error

Class: **silent-fail**

Environment: GNOME Shell (Activities overview, Sat 27 May 19:07, 3840x2160 screen recording), Celluloid video player launched from app search. No account or organization visible.

Steps:

1. Open Activities and type 'Celluloid' in the search box. The results list Celluloid. The search was typed or the overview was opened without any visible trigger. (00:00.9; p001, p002, p003)
2. Launch Celluloid (the launch action is not visible). An empty player window opens with a 00:00 position and no media loaded. (00:02.8; p004, p005, p006)
3. Wait. The top bar shows a spinner next to 'Celluloid', meaning the app is still starting or busy, and the window stays empty. (00:04.5; p007)
4. At about 5.5 s the Celluloid window and its '00:00' counter disappear. Only the empty desktop remains, and the top bar still shows 'Celluloid' with a spinner. (00:05.5; p008, p009)

Expected (implied): Celluloid should stay open and ready to play media, and the launch spinner should stop. If it cannot start, it should show an error.

Actual: The window opens empty, closes after about 3 s, and no error or message is shown. The top bar still shows the Celluloid entry with a spinner after the window is gone. The video does not show whether the app crashed, hung while starting, or was closed by the user.

Key events: p005, p007, p008, p009

Missed by the author:

- The top bar still shows 'Celluloid' with a spinner after the window has vanished (p007, p008, frames/000189.jpg). This suggests the launch never finished or the process is stuck.
- The window was empty and never showed a loaded file or any content before it closed (p005, p006).
