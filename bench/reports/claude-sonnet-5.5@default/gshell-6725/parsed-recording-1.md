# real/gshell-6725

_claude-sonnet-5.5@default, 20 s; looked at: frames/000085.jpg, frames/000165.jpg, frames/000263.jpg_

Celluloid's window opens empty, then disappears within about 2 seconds. The user opens Activities search and types "call". Later the desktop is empty, but the top bar still shows Celluloid with a busy spinner. No window ever shows any media, and the video has no audio and no visible user input.

## Celluloid window opens empty, vanishes, and the app is left in a perpetual 'launching' state with no window

Class: **silent-fail**

Environment: GNOME Shell on Linux (Wayland/X11 not determinable), Sat 27 May 19:06, screen recorder running (0:02–0:09). Celluloid media player; Activities overview search.

Steps:

1. Celluloid is opened (the trigger is not visible). Its window appears empty: black video area, 00:00 position, controls disabled. (00:02.4; p002, p003, p004)
2. The Celluloid window disappears after about 1.6 s. A frame shows the Activities overview with the search 'Searching...'. (00:04.4; p005, p006, p007, p008)
3. The user types 'call' in the Activities search, which lists Calculator, Calendar and others. The top bar still shows Celluloid with a spinner. (00:05.4; p009, p010)
4. The overview closes to an empty desktop with no windows. The top bar still reads 'Celluloid' with a spinner through the end of the video. (00:08.7; p012, p013)

Expected (implied): Celluloid opens and stays open, or closes cleanly without leaving the shell showing it as still launching or active.

Actual: The Celluloid window is shown for about 1.6 s and then disappears. For the rest of the video no Celluloid window exists, yet the top bar keeps showing 'Celluloid' with a loading spinner. No error is displayed.

Key events: p003, p006, p009, p010, p012

Missed by the author:

- The Celluloid spinner in the top bar persists on an empty desktop (p010, p011, p012; frames/000263.jpg).
- The Celluloid window flashed away at 00:04.4 (p005, p006).
- The video has no audio, so the author's intent is unknown; the typed text 'call' may not be what was meant to launch an app.
