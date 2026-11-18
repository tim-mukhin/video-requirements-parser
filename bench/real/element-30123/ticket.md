# Rapidly pressing Finish after recovery setup causes an error

Source: https://github.com/element-hq/element-web/issues/30123  (reporter: mxandreas, filed 2025-06-11)

### Steps to reproduce

1. Go to Settings -> Encryption -> Set up recovery
2. Follow the process to get to the last stage.
3. Press the "Finish the setup" button multiple times.

Note that pressing the button multiple times is likely to happen, because finishing the setup will take time (at least a few seconds) so the user might click again as they were not sure if they clicked.

### Outcome

#### What did you expect?

The "Finish the setup" button gets disabled once pressed to make it clear for the user that finishing is in progress and/or multiple clicks are handled so that they do not cause any weird behavior.

#### What happened instead?

Modals popping up several times to enter the recovery key or with error messages. See screen recording below.

[attachment: recording.gif]

### Operating system

macOS

### Browser information

_No response_

### URL for webapp

app.element.io

### Application version

_No response_

### Homeserver

_No response_

### Will you send logs?

Yes
