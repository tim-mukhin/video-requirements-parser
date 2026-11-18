# real/element-30123

_gpt-6-sol@default, 51 s; looked at: frames/moments/p006.jpg, frames/moments/p014.jpg, frames/moments/p025.jpg, frames/moments/p028.jpg, frames/0008.5.jpg, frames/0011.5.jpg, frames/0016.5.jpg, frames/0020.5.jpg, frames/0022.5.jpg, frames/0026.5.jpg, frames/0007.5.jpg, frames/0009.5.jpg, frames/0010.0.jpg, frames/0010.5.jpg, frames/0011.0.jpg, frames/0023.0.jpg, frames/0024.0.jpg, frames/0017.0.jpg, frames/0019.5.jpg, frames/0023.5.jpg, frames/0027.5.jpg_

After the recovery key is entered, Finish set up remains available during repeated presses. A recovery-key prompt opens, and after it is dismissed an access-canceled error appears; both dialogs recur, interrupting setup. The frames confirm the repeated presses noted by the watcher, while the timeline identifies the resulting dialogs and error.

## Repeated Finish set up presses lead to recurring recovery-key and error dialogs

Class: **error-shown**

Environment: Element at app.element.io in a browser on macOS, with Settings > Encryption open. The address bar contains ?error=access_denied; its relevance is not established.

Steps:

1. In Settings > Encryption, proceed through Set up recovery to the recovery-key confirmation screen. (00:02.4; p004, p005, p009, p015, p018)
2. Enter the recovery key shown on the previous screen. (00:07.5; p007, p029)
3. Press Finish set up repeatedly while it remains available; the timeline records presses at 8.3s and 11.6s, and intervening frames show further press indicators. (00:08.3; p031, p034)
4. The recovery-key prompt opens. Its field is empty and Continue is disabled; it is subsequently dismissed, but the dismissal trigger is not visible. (00:11.7; p035, p036)

Expected (implied): Once pressed, Finish set up should indicate progress and prevent duplicate submissions, or handle them without extra prompts or errors.

Actual: Finish set up stays available during repeated press indicators. An empty recovery-key prompt opens at 11.7s. After it closes, “Failed to set up secret storage — Error: Secret storage access canceled” appears at 20.4s; the recovery-key prompt and error appear again at 22.2s and 23.9s.

Key events: p029, p031, p034, p035, p036, p038, p039

Missed by the author:

- The recovery-key prompt has an empty field and disabled Continue button before the access-canceled error; the ticket does not mention this intervening prompt dismissal [p035, p036].
- The address bar shows ?error=access_denied, but the video does not establish a connection to this failure [p003].

Claims:

- "Repeated presses can lead to multiple recovery-key or error dialogs." [ticket: Outcome]: confirmed - The frames show repeated press indicators on Finish set up, and the timeline records a second recovery-key prompt and error dialog [p031, p034, p035, p036, p038, p039].
- "Finishing takes at least a few seconds." [ticket: Steps to reproduce, note]: not shown - The video does not show setup completing, so its completion time cannot be measured.
- "Repeated presses alone cause the error." [ticket: Steps to reproduce and Outcome]: not shown - The first error follows dismissal of an empty recovery-key prompt; the video does not isolate repeated presses from that dismissal [p035, p036].
