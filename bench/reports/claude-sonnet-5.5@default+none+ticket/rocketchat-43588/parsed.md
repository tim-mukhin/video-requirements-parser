# real/rocketchat-43588

_claude-sonnet-5.5@default, 16 s; looked at: nothing_

In the Rocket.Chat video message recorder, the timer and the "recording" activity status are not cleaned up when the user switches channels while recording. The timer keeps firing and other users still see the user as recording until the page is reloaded. This is a leaked-state bug with no visible error.

## Video recorder timer and recording status keep running after leaving the room

Class: **silent-fail**

Environment: Rocket.Chat Server 9.1.0-develop (local source, yarn dsv), Community license, 1 user, single instance, Meteor local MongoDB, Node 22.22.3. Client: Chrome on macOS.

Steps:

1. Open a channel and start a video message. (00:00.0; )
2. Allow camera access and click Record so the timer starts counting. (00:00.0; )
3. Without clicking Cancel or Send, switch to another channel. (00:00.0; )

Expected (speech): The timer stops and the recording status clears when the recorder dialog closes.

Actual: After switching channels, the recorder's timer keeps firing and other users still see the user as recording until the page is reloaded. No error appears in the server or browser logs.

Key events: 

Claims:

- "The timer is not cleared when VideoMessageRecorder unmounts." [The timer is started in VideoMessageRecorder.tsx and is not cleared when the component unmounts.]: not shown - This is the reporter's code diagnosis from the ticket. There is no video or code check to back it up.
- "UserAction.stop is not called on unmount, so the recording activity keeps being renewed." [UserAction.stop is not called either, so the recording activity keeps being renewed.]: not shown - This is the reporter's hypothesis. The ticket gives no evidence for it.
- "Other users still see the reporter as recording." [other users can still see you as recording until the page is reloaded]: not shown - The ticket says only 1 user is on the server, so it is unclear how a second viewer observed this.
- **R1** [stated] When the recorder dialog closes or unmounts, including on a channel switch, the timer must stop and the recording activity status must be cleared. - 
