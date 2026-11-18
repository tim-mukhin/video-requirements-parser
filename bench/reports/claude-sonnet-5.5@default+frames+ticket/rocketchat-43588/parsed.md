# real/rocketchat-43588

_claude-sonnet-5.5@default, 36 s; looked at: frames/0000.0.jpg, frames/0005.0.jpg, frames/0010.0.jpg, frames/0015.0.jpg, frames/0020.0.jpg, frames/0025.0.jpg, frames/0030.0.jpg, frames/0035.0.jpg, frames/0040.0.jpg, frames/0045.0.jpg, frames/0051.5.jpg, frames/0013.5.jpg, frames/0028.0.jpg, frames/0027.0.jpg, frames/0012.0.jpg_

With DevTools open, the reporter starts a video message in #general, lets the timer run, then switches to another room without pressing Cancel or Send. The recorder unmounts, but the console keeps logging one tick per second from the same interval id (795) until the end of the video. Leaked timer confirmed; the 'recording' status shown to other users is not shown.

## Video message recorder interval keeps ticking after the recorder unmounts on room switch

Class: **silent-fail**

Environment: Chrome on macOS, Rocket.Chat dev build at localhost:3000, DevTools console docked next to a narrow viewport (671x705). User 'thakur', rooms #general and a private group 'test' (topic 'Memory Leak'). The console shows debug logs from VideoMessageRecorder.tsx (local instrumentation). VS Code is shown with an uncommitted diff of VideoMessageRecorder.tsx.

Steps:

1. Open #general with the console open. The console shows a prior log '[video-recorder] unmounted, timer already cleared'. (00:10.0; 0010.0)
2. Start a video message and click Record (inferred from the recorder appearing). The camera preview appears, the timer shows 00:00 and the console logs 'timer started 795'. (00:13.5; 0012.0, 0013.5)
3. Let the timer run. The console logs one tick per second from interval 795. (00:15.0; 0015.0, 0025.0)
4. Without pressing Cancel or Send, open the sidebar (about 27 s, timer at 00:13-00:14). (00:28.0; 0027.0, 0028.0)
5. Click the 'test' room (inferred). The room switches and the recorder dialog disappears. The console logs 'unmounted while timer still running 795'. (00:30.0; 0030.0)
6. Wait. The console keeps logging ticks 00:16, 00:17 and so on from interval 795, reaching 00:38 at the end of the video, with no recorder visible. (00:51.5; 0035.0, 0051.5)

Expected (implied): When the recorder unmounts after a room switch, the interval is cleared and the recording activity is stopped, so no more ticks occur.

Actual: After the recorder is gone, interval 795 keeps firing every second. The console logs ticks from 00:16 to at least 00:38, plus 'unmounted while timer still running'.

Key events: 0013.5, 0030.0, 0035.0, 0051.5

Missed by the author:

- The recorder runs with locally added console.log instrumentation, so the logs are not stock behaviour (0013.5, 0030.0).
- VS Code shows an uncommitted diff already adding recordingIntervalRef and clearInterval (0020.0, 0045.0). It is unclear whether the failing build includes it.

Claims:

- "The timer keeps firing after leaving the room" [The timer keeps firing, and other users can still see you as recording until the page is reloaded.]: confirmed - Ticks from interval 795 continue after the unmount log (0030.0 to 0051.5).
- "Other users still see the reporter as recording" [other users can still see you as recording]: not shown - No second user or status indicator is shown. UserAction.stop is also not visible in the console.
- "The cause is the missing cleanup on unmount" [not cleared when the component unmounts]: confirmed - The log 'unmounted while timer still running' fires on unmount. The VS Code diff shows a fix: a ref holding the interval id and a clearInterval call in stopVideoRecording (0020.0, 0040.0, 0045.0).
- "Steps are only: open channel, record, switch channel" [Do not click Cancel or Send. Switch to another channel.]: confirmed - Matches the video. Debug logging and a working-tree fix were added locally.
- **R1** [proposed] On unmount of the video recorder (room switch), clear the timer interval and call UserAction.stop for the recording activity. - 0030.0, 0051.5
