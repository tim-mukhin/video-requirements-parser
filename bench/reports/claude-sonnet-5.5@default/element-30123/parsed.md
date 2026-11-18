# real/element-30123

_claude-sonnet-5.5@default, 19 s; looked at: frames/000342.jpg, frames/000197.jpg_

In Element Web, the user sets up a recovery key. After they click Finish set up, a second 'Recovery key' prompt appears that asks for the key again. The setup then fails with 'Failed to set up secret storage: Secret storage access canceled'. No audio, so the author's view is unknown.

## Recovery key setup fails with 'Secret storage access canceled' after an unexpected second recovery-key prompt

Class: **error-shown**

Environment: app.element.io in a desktop browser (URL has ?error=access_denied#/home). Settings > Encryption dialog, user avatar 'T'. Account and organization not visible.

Steps:

1. Open Settings > Encryption and start 'Set up recovery'. The 'Set up recovery' dialog opens (the trigger is not visible). (00:02.1; p001, p004)
2. Click Continue. A recovery key is generated and shown (EsU1 BoWe ...). (00:02.4; p005, p007, p012)
3. Click Continue on the key screen. The 'Finish set up' screen asks the user to enter the recovery key. (00:05.7; p014, p015, p016)
4. Click 'Finish set up' with the key entered (the typing is not seen). (00:08.3; p030)
5. A second 'Recovery key' prompt ('Make sure nobody can see this screen!') appears on top of the settings page. The cursor sits over a disabled Continue button (a 'not allowed' cursor) at about 00:11.7. (00:11.7; p033, p034)
6. The prompt is dismissed or cancelled (the trigger is not visible). The error dialog 'Failed to set up secret storage / Error: Secret storage access canceled' appears. (00:20.4; p035)
7. Click OK. The prompt returns at 00:22.2 and the error dialog shows again at 00:23.9. (00:21.0; p036, p037, p038)
8. The error dialog finally closes, and the Encryption settings page shows the session key and the Import/Export keys buttons. (00:26.8; p039, p047)

Expected (implied): After the key is confirmed and 'Finish set up' is clicked, secret storage is set up and the recovery key is active. No further key prompt appears.

Actual: Finish set up leads to another recovery-key prompt with a disabled Continue button. Secret storage setup then fails with 'Secret storage access canceled'. The prompt and the error come back after OK is clicked.

Key events: p030, p034, p035, p036, p037, p038

Missed by the author:

- The recovery key text appears and disappears several times (p020, p028, p031). Fragments of the key remain visible in the background of the second prompt (p034).
- After OK at 00:21 the prompt and then the error return (p036 to p038), so the failure repeats.
