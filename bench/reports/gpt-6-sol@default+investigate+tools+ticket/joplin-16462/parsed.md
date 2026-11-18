# real/joplin-16462

_gpt-6-sol@default, 49 s; looked at: frames/moments/p015.jpg, frames/moments/p063.jpg, frames/0001.5.jpg, frames/0002.0.jpg, frames/0004.0.jpg, frames/0004.5.jpg, frames/0005.0.jpg, frames/0006.0.jpg, frames/0007.0.jpg, frames/0008.5.jpg, frames/0009.0.jpg, frames/000304.jpg, looks/0004.30-0005.10-865_1440_175_185/sheet.jpg, looks/0008.50-0009.60-865_1440_175_185/sheet.jpg_

The hide-keyboard control is unreliable while the note search field is focused. On the first recorded tap, the keyboard changes layout and closes after a delay; on the second, it remains visible through the end of the recording.

## Hide-keyboard control intermittently fails with note search focused

Class: **intermittent**

Environment: Joplin on iOS, dark mode, note “Testing!” in “Mess”. The ticket reports Joplin 13.7.3; the version is not shown in the video.

Steps:

1. Open the note search field (the trigger is not visible); the field has a caret and the keyboard is shown. (00:01.8; p002)
2. Tap the toolbar's keyboard-with-down-arrow icon. (00:04.4; p019)
3. Refocus the search field (the trigger is not visible); the keyboard returns. (00:07.5; p039, p041)
4. Tap the same hide-keyboard icon again. (00:08.6; p064)

Expected (implied): Tapping the hide-keyboard control should dismiss the keyboard even when search, rather than the editor, has focus.

Actual: After the first tap, the search caret disappears and the keyboard changes to a regular Return layout but remains visible until about 5.9 s. After the second tap, the search caret and keyboard remain visible through 9.6 s. The frames identify the tapped control as the hide-keyboard icon, resolving the timeline's incorrect “H” label for the first tap.

Key events: p002, p019, p022, p037, p039, p041, p064

Missed by the author:

- The first tap changes the keyboard from a blue Search key to a regular Return key before it closes [p019, p022, p037].
- The keyboard is fully hidden at 5.9 s, contrary to the ticket's unqualified description [p037].

Claims:

- "The keyboard remains visible after clicking Hide keyboard." [ticket: Current behaviour, steps 2–3]: confirmed - It remains visible after the second recorded tap through the end of the video; after the first tap, it remains briefly but later closes.
- "The button does nothing." [ticket: title]: refuted - Following the first tap, the search caret and keyboard layout change, and the keyboard eventually closes. The second tap does not dismiss it during the recorded interval.
- "The recording shows Joplin 13.7.3." [ticket: Joplin version]: not shown - No version screen appears.
