# Video recorder timer keeps running after leaving the room

Source: https://github.com/RocketChat/Rocket.Chat/issues/43588  (reporter: Thakur156, filed 2026-11-07)

### Description:

The video message recorder keeps its clock timer and the "recording" status alive after you leave the room.

### Steps to reproduce:

1. Open a channel and start a video message.
2. Allow the camera and click Record so the timer starts counting.
3. Do not click Cancel or Send. Switch to another channel.

### Expected behavior:

The timer stops and the recording status clears when the recorder dialog closes.

### Actual behavior:

The timer keeps firing, and other users can still see you as recording until the page is reloaded. A screen recording is attached.

### Server Setup Information:

- Version of Rocket.Chat Server: 9.1.0-develop (local source)
- License Type: Community
- Number of Users: 1
- Operating System: macOS
- Deployment Method: source (`yarn dsv`)
- Number of Running Instances: 1
- DB Replicaset Oplog: no
- NodeJS Version: 22.22.3
- MongoDB Version: Meteor's local MongoDB

### Client Setup Information

- Desktop App or Browser Version: Chrome
- Operating System: macOS

### Additional context

The timer is started in `apps/meteor/client/views/composer/VideoMessageRecorder/VideoMessageRecorder.tsx` and is not cleared when the component unmounts. `UserAction.stop` is not called either, so the recording activity keeps being renewed.

### Relevant logs:

No server or browser error. The timer continues silently after the dialog is gone.

[attachment: recording.mp4]
