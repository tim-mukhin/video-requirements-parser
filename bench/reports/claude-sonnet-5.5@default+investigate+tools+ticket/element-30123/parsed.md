# real/element-30123

_claude-sonnet-5.5@default, 21 s; looked at: nothing_

On the last step of Settings → Encryption → Set up recovery, the user clicks 'Finish set up' and the screen shows no progress. A 'Recovery key' prompt then opens and ends in a 'Failed to set up secret storage' error. The same prompt and error come back a second time after OK is clicked. The ticket's 'multiple modals and errors' is therefore confirmed on screen.

## Finish set up on recovery setup gives no progress feedback, then repeated 'Recovery key' prompts and 'Failed to set up secret storage' errors

Class: **error-shown**

Environment: Element Web at app.element.io (URL has ?error=access_denied#/home), macOS browser, logged-in user (avatar 'T'), Settings dialog → Encryption. App version and homeserver are not visible. There is no audio.

Steps:

1. Click 'Set up recovery' in Settings → Encryption; the 'Set up recovery' intro screen opens with a Continue button (the click on 'Set up recovery' is not shown). (00:02.1; p001, p004)
2. Click 'Continue'; the generated recovery key is shown on 'Save your recovery key somewhere safe'. (00:02.4; p005, p007, p009)
3. Click the button at the bottom of that screen (not read as text); the 'Enter your recovery key to confirm' screen opens with a 'Finish set up' button. (00:05.7; p015, p016, p018)
4. Click 'Finish set up' with the key entered in the field (key entry is not visible). The button shows no disabled or loading state. (00:08.3; p031, p032)
5. Click again at about the same place (repeat). A 'Recovery key' modal ('Make sure nobody can see this screen!') opens, although the key was already entered. (00:11.6; p034, p035)
6. After about 9 s the modal is replaced by the error 'Failed to set up secret storage – Error: Secret storage access canceled'. (00:20.4; p036)
7. Click OK on the error. The 'Recovery key' prompt appears again, followed by the same error a second time. Another OK closes it and Settings → Encryption is visible again. (00:21.0; p037, p038, p039, p047, p048)

Expected (implied): Once 'Finish set up' is pressed the button is disabled or shows progress, repeated clicks are ignored, and setup finishes once with no extra Recovery key prompt and no error.

Actual: 'Finish set up' shows no feedback. After repeated clicks a 'Recovery key' prompt (empty field, Continue disabled) opens and stays for about 9 s. It is replaced by 'Failed to set up secret storage: Secret storage access canceled'. After OK the prompt and the error appear a second time.

Key events: p031, p032, p034, p035, p036, p037, p038, p039

Missed by the author:

- The error text is 'Secret storage access canceled' (p036).
- The 'Recovery key' modal asks for a key that was already entered on the confirm screen (p035).
- The modal and the error come back a second time after OK is clicked (p037–p039).
- The URL contains ?error=access_denied before the test starts (p003). Its effect is unknown.

Claims:

- "Pressing Finish several times causes recovery-key modals or errors to pop up several times." [ticket]: confirmed - The timeline shows the Recovery key modal twice (p035 at 11.7 s, p038 at 22.2 s) and the error dialog twice (p036 at 20.4 s, p039 at 23.9 s). Only one click on Finish is read as text (p031); the second click (p034) is a click with no text.
- "The Finish button is not disabled or given a loading state after being pressed." [ticket]: confirmed - The screen states after p031 (s014, s015, 8.3–11.6 s) show no change in the button.
- "Finishing takes at least a few seconds, which invites more clicks." [ticket]: confirmed - There are about 3 s with no visible change between the click at 8.3 s and the next click at 11.6 s, then about 9 s until the error at 20.4 s.
- "The button is labelled 'Finish the setup'." [ticket]: refuted - On screen it reads 'Finish set up' (p016, p031). This is only a wording difference.
