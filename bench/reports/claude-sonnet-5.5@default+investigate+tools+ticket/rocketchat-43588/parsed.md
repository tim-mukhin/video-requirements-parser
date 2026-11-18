# real/rocketchat-43588

_claude-sonnet-5.5@default, 22 s; looked at: nothing_

With the video message recorder open and its timer running in #general, switching to the 'test' room closes the recorder. The console shows 'unmounted while timer still running 795', and interval 795 keeps ticking until the end of the video. The interval is never cleared, so this is a leak. The video does not show the 'recording' status for other users.

## Video message recorder interval keeps ticking after the recorder unmounts on room switch

Class: **silent-fail**

Environment: Chrome on macOS, Rocket.Chat dev build at localhost:3000, narrow viewport (671x705) with DevTools console open. User 'thakur'. Rooms #general and the private group 'test' (topic 'Memory Leak'). The console shows '[video-recorder]' debug logs, which look like local instrumentation. VS Code shows a diff that adds recordingIntervalRef and clearInterval in stopVideoRecording.

Steps:

1. Open #general with the console open. The console already shows an older log '[video-recorder] unmounted, timer already cleared'. (00:10.1; p089)
2. Open the video message recorder and start recording (the trigger is not visible). The recorder shows 00:00 with Cancel and Send, and the console logs 'timer started 795'. (00:13.0; p090, p092, p093, p127, p128)
3. Leave the recorder running without pressing Cancel or Send. The console logs one tick per second from interval 795. (00:14.3; p145, p152)
4. Switch to the 'test' room via the sidebar (the click is not visible because the cursor is not followed here). The URL changes to /group/test, and the recorder, its timer, Cancel and Send disappear. The console logs 'unmounted while timer still running 795'. (00:28.7; p277, p292, p295, p301, p305)
5. Wait. Ticks from interval 795 keep appearing in the console with no recorder on screen. The ticks reach about 00:30 or later, and the video ends with the console still active. (00:34.0; p295)

Expected (implied): When the recorder unmounts, the interval is cleared and the recording activity is stopped, so no more ticks occur.

Actual: After the recorder unmounts, interval 795 keeps firing every second. The console logs 'unmounted while timer still running 795' and no clearInterval call. No error appears.

Key events: p128, p145, p277, p292, p295, p301, p305

Missed by the author:

- The recorder runs with locally added console.log instrumentation, so the logs are not stock behaviour (p128, p145, p295).
- An older log, 'unmounted, timer already cleared', is already present before the recording starts (p089). It suggests the cleanup works on other unmount paths, which the video does not show.
- VS Code shows an uncommitted diff that already adds the ref and clearInterval. It is unclear whether the build under test includes it (p182, p496).

Claims:

- "The timer keeps firing after leaving the room" [u007]: confirmed - Ticks from interval 795 continue after the unmount log (p295 onward).
- "Other users still see the reporter as recording, and UserAction.stop is not called" [u006]: not shown - No second user or status indicator is shown. UserAction is not visible in the console.
- "The timer is not cleared on unmount, so there is no clear interval" [u008]: confirmed - The log 'unmounted while timer still running' appears and the ticks continue. The author's mentions of 'no clear interval' and a 'PR' are claims about the code, not shown beyond the VS Code diff.
- "The fix is clearing the interval in the stop video recording function" [u009]: not shown - VS Code shows a diff with clearInterval (p182, p450, p496). The video never re-runs the scenario with it, so it is not shown to work.
