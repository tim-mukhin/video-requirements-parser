# real/rocketchat-43588

_gpt-6-sol@default, 42 s; looked at: frames/0013.0.jpg, frames/0029.5.jpg, frames/moments/p321.jpg, frames/0009.0.jpg, frames/0010.5.jpg, frames/0028.0.jpg, frames/moments/p361.jpg, frames/moments/p523.jpg, frames/0051.5.jpg_

After a video message is started in #general, switching to #test closes the recorder but its timer continues firing. The watcher identified the persistent console ticks; the timeline establishes that they continue after the recorder unmounts, and the short-event frames show further ticks rather than a separate UI flash.

## Video-message timer continues after leaving the room

Class: **silent-fail**

Environment: Rocket.Chat at localhost:3000 in Chrome on macOS, with DevTools open in a 671 × 705 responsive viewport; #general and #test are visible.

Steps:

1. In #general, open the video-message recorder (the trigger is not visible). (00:10.1; p090, p092, p093)
2. Start the video message; the trigger is not visible, but the timer-start diagnostic appears. (00:13.0; p127, p128)
3. Open the sidebar and switch to #test (the triggers are not visible). (00:28.7; p277, p286, p292, p294)

Expected (implied): Leaving the room closes the recorder, stops its timer and clears recording status.

Actual: The recorder closes in #test, but the console reports that it unmounted while timer 795 was still running. Ticks continue from 00:16 to at least 00:38; the video does not show another user's recording status.

Key events: p089, p128, p281, p292, p294, p295, p297, p311, p361, p565

Missed by the author:

- An earlier console entry says the timer was already cleared on an earlier unmount; the later unmount reports timer 795 still running [p089, p295].
- The destination is #test at localhost:3000/group/test, and its composer is visible without the recorder [p292, p294].

Claims:

- "The timer keeps firing after leaving the room." [u007]: confirmed - The #test view shows the recorder gone, an unmount diagnostic and subsequent ticks; the short-event strip at p361 also shows continuing ticks.
- "Other users can still see the author as recording until reload." [ticket.md: Actual behavior]: not shown - Neither another user's view nor a reload appears.
- "The interval is not cleared on recorder unmount." [ticket.md: Additional context]: confirmed - The unmount diagnostic names running interval 795 and later ticks retain that interval ID.
- "UserAction.stop is not called, so recording activity keeps being renewed." [ticket.md: Additional context]: not shown - The video demonstrates timer ticks, not activity-renewal requests or another user's indicator.
- "Camera access was allowed and a button labeled Record was clicked." [ticket.md: Steps to reproduce]: not shown - The preview and timer start are visible, but a permission prompt and the triggering click are not.
