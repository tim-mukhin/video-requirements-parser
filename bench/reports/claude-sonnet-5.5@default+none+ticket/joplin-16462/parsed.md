# real/joplin-16462

_claude-sonnet-5.5@default, 13 s; looked at: nothing_

On Joplin for iOS 13.7.3, tapping the "Hide keyboard" button while the search panel's entry has focus does nothing, and the keyboard stays visible. The button appears to work only when the editor has focus. Users can't dismiss the keyboard from search.

## iOS: "Hide keyboard" button does nothing while the search entry is focused

Class: **silent-fail**

Environment: Joplin mobile on iOS, version 13.7.3. The iOS version, device model, editor type (Markdown or rich text) and account are not given. The ticket says nothing about desktop.

Steps:

1. Open the search panel. (00:00.0; )
2. Tap the "Hide keyboard" button. (00:00.0; )
3. Observe that the keyboard remains visible. (00:00.0; )

Expected (speech): Tapping "Hide keyboard" hides the keyboard even when the search panel, not the editor, has focus.

Actual: The keyboard stays visible after tapping "Hide keyboard". There is no error or other feedback.

Key events: 

Claims:

- "The button does nothing while the search entry has focus." [Observe that the keyboard remains visible.]: not shown - No video. The ticket only asserts this, and the attached recording was not available.
- **R1** [stated] The "Hide keyboard" button must dismiss the keyboard when the search panel has focus, not only when the editor does. - ticket: Expected behaviour
