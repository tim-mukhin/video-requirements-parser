# real/element-30123

_claude-sonnet-5.5@default, 34 s; looked at: frames, frames/0000.0.jpg, frames/0005.0.jpg, frames/0010.0.jpg, frames/0015.0.jpg, frames/0020.0.jpg, frames/0025.0.jpg, frames/0028.5.jpg, frames/0003.0.jpg, frames/0011.0.jpg, frames/0012.0.jpg, frames/0013.0.jpg, frames/0018.0.jpg, frames/0023.0.jpg_

On the last step of Settings → Encryption → Set up recovery, the user clicks "Finish set up" and nothing shows that work is in progress. A "Recovery key" prompt, which the user did not ask for, then opens over the settings. A "Failed to set up secret storage" error follows. This matches the ticket's report of unwanted modals and errors after pressing Finish.

## Finish set up during recovery setup gives no progress feedback and ends in an unexpected Recovery key prompt, then a 'Failed to set up secret storage' error

Class: **error-shown**

Environment: Element Web at app.element.io in a Brave-style browser on macOS. The URL is app.element.io/?error=access_denied#/home. A logged-in user, avatar 'T', is in Settings → Encryption. Key storage is on and Recovery is shown as 'Recommended'. App version and homeserver are not visible.

Steps:

1. Open Settings → Encryption. The Recovery section shows the 'Set up recovery' button, with the cursor on it. The click itself is inferred. (00:00.0; 0000.0)
2. The 'Save your recovery key somewhere safe' screen shows the key. The cursor moves to 'Continue'. The click is inferred. (00:03.0; 0003.0, 0005.0)
3. On 'Enter your recovery key to confirm', the full key is already in the field. The cursor is on 'Finish set up' and the click marker is visible. The click, and the pasting or typing of the key, are inferred. (00:10.0; 0010.0, 0011.0)
4. The user keeps pressing 'Finish set up'. The click marker is visible at 10.0 s and 11.0 s. The button shows no disabled or loading state in those frames. Further clicks after 11.0 s are inferred, as the screen has already changed. (00:11.0; 0010.0, 0011.0)
5. A 'Recovery key' modal ('Make sure nobody can see this screen!') opens over the settings, with an empty key field and a disabled Continue button. It stays open for several seconds. The cursor shows a not-allowed icon. (00:12.0; 0012.0, 0013.0, 0015.0, 0018.0)
6. The prompt is replaced by an error dialog: 'Failed to set up secret storage – Error: Secret storage access canceled'. The click marker is visible again below it. The user then closes the dialog with OK (inferred). (00:20.0; 0020.0, 0020.5)
7. With the dialog closed, the settings page is visible again, scrolled down to Advanced. The Recovery state cannot be checked in these frames. (00:25.0; 0025.0, 0028.5)

Expected (implied): After 'Finish set up' is pressed, the button should be disabled or show progress, and repeated clicks should be ignored. Setup should finish once, with no extra Recovery key prompt and no error.

Actual: The button gives no visible feedback after the click. A second 'Recovery key' modal, which asks for the key the user just entered, opens over the settings. It is later replaced by 'Failed to set up secret storage: Secret storage access canceled'.

Key events: 0010.0, 0011.0, 0012.0, 0018.0, 0020.0

Missed by the author:

- The error text is 'Secret storage access canceled' (0020.0).
- The recovery-key modal appears even though the key was already entered on the confirm screen (0012.0).
- The URL contains '?error=access_denied' before the test starts (0000.0). It is unknown whether this affects the result.
- No click-count or timing evidence is visible in the frames, so the exact number of clicks is not shown (0010.0, 0011.0).

Claims:

- "Pressing 'Finish the setup' several times causes modals to pop up to enter the recovery key, or error messages." [Modals popping up several times to enter the recovery key or with error messages.]: confirmed - One recovery-key modal (12.0–18.0 s) and one error dialog (from 20.0 s) are visible. The frames do not show several copies of each.
- "The button is not disabled while finishing is in progress." [The 'Finish the setup' button gets disabled once pressed]: confirmed - At 10.0 s and 11.0 s the button looks the same as before the click, with no disabled or spinner state.
- "Finishing takes at least a few seconds, which invites repeated clicks." [finishing the setup will take time (at least a few seconds)]: not shown - The frames show a delay of about 10 s between the click and the error, but the repeated clicks cannot be told apart in the frames. The recording has no sound.
- "The button is labelled 'Finish the setup'." [Press the "Finish the setup" button]: refuted - On screen the button reads 'Finish set up'.
