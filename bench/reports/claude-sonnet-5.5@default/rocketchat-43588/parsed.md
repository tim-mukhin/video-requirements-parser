# real/rocketchat-43588

_claude-sonnet-5.5@default, 27 s; looked at: nothing_

In Rocket.Chat running locally, the author starts a video message recording in #general and then switches to another room, #test, without cancelling. The recorder unmounts, but the console shows its interval timer still ticking, which is a memory leak. The author then shows a code change in stopVideoRecording that clears the interval.

## Video message recorder interval keeps running after the component unmounts (memory leak)

Class: **silent-fail**

Environment: Chrome with DevTools docked (Console), Rocket.Chat at localhost:3000, rooms #general and private group #test, and an editor open on VideoMessageRecorder.tsx (Working Tree). The author added console.log lines with the prefix [video-recorder].

Steps:

1. Open #general with DevTools Console open. The author says they opened inspect elements; the page is the chat room. (00:04.0; u001, p028)
2. Open the video message recorder in the composer. The Cancel and Send buttons and a 00:00 timer appear. Console logs 'timer started 795' and then ticks every second. (00:10.1; u003, p084, p085, p087, p088, p120, p121, p138)
3. While the recording is running (timer at about 00:09–00:15), click another room, #test, in the sidebar. The trigger is not visible because the cursor is not followed. The URL changes from /channel/general to /group/test. (00:26.0; u006, p200, p244, p277, p290)
4. The recorder UI disappears (Cancel, Send, 00:15 gone). Console logs 'unmounted while timer still running 795' (VideoMessageRecorder.tsx:121). (00:29.1; p279, p280, p285, p289)
5. The Console keeps printing 'tick ... interval 795' for the same interval id after the unmount (00:16, 00:17, 00:18, ... later 00:35 and 00:37). (00:29.9; p281, p294, u007, p324, p527, p543)

Expected (implied): When the recorder component unmounts, its recording interval is cleared and the ticks stop, so nothing leaks.

Actual: The interval with id 795 keeps ticking after the component is unmounted. The console logs 'unmounted while timer still running' and the counter goes on past 00:35. The cleanup code that would clear the interval is missing from the unmount and stop path. This is a leak: a timer that runs forever with no UI.

Key events: p121, p279, p281, p294, p324, p527, p543, u007, u008

Missed by the author:

- The Console shows 2 issues and a react-i18next warning (missing i18next instance) at the start [p016, p022]. It is unrelated and the author does not mention it.
- The diff in the editor has a typo-like variant clearInterVal/itervalId in the OCR text [p433, p464]. It may be an OCR misread and needs checking in the code.
- The unmount message is logged at VideoMessageRecorder.tsx:121, which suggests an unmount cleanup effect already exists but does not clear the interval [p280].

Claims:

- "Intervals keep going after the component is unmounted." [u007]: confirmed - The log shows 'unmounted while timer still running 795' at 00:29 [p279], followed by ticks 00:16, 00:17, 00:18 and later 00:35 and 00:37 [p281, p294, p324, p527, p543].
- "There is no clearInterval for this particular interval in the component." [u008]: not shown - The log supports it indirectly because the interval keeps running. The editor frames show a diff with a clearInterval(intervalId) block in stopVideoRecording [p174, p464], but the original code is not read out in the timeline.
- "The change in the stop video recording function clears the interval, so there should be no memory leak." [u010]: not shown - The video shows only the diff in the editor. The author never rebuilds or reruns after the change. Ticks are still printed at 00:35 and 00:37 near the end [p527, p543], but this is from the earlier recording, so it does not confirm or refute the fix.
