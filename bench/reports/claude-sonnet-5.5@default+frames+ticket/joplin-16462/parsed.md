# real/joplin-16462

_claude-sonnet-5.5@default, 44 s; looked at: frames, frames/0000.0.jpg, frames/0002.0.jpg, frames/0004.0.jpg, frames/0006.0.jpg, frames/0008.0.jpg, frames/0009.5.jpg, frames/0001.0.jpg, frames/0004.5.jpg, frames/0005.0.jpg, frames/0005.5.jpg, frames/0006.5.jpg, frames/0007.0.jpg, frames/0007.5.jpg, frames/0003.0.jpg, frames/0008.5.jpg, frames/0009.0.jpg_

In the Joplin iOS note editor, the "hide keyboard" toolbar button does not reliably dismiss the keyboard while the search entry is focused. The keyboard stays up after the tap. It then slides away and reappears within about a second, and the search field regains focus. The video shows a slightly different symptom from the ticket's "keyboard remains visible".

## iOS: "Hide keyboard" button fails to keep the keyboard hidden while the search entry is focused

Class: **state-revert**

Environment: iOS (iPhone, dark theme, 5G) with the screen being recorded. Joplin mobile, note "Testing!" in notebook "Mess", Markdown editor with the formatting toolbar and the search panel open. The app version is not visible; the ticket says 13.7.3.

Steps:

1. Note is open in the editor with the keyboard up and the formatting toolbar above it. The search panel is not open yet. (00:01.0; 0001.0)
2. Tap the search icon in the toolbar (inferred). The search panel opens above the toolbar, the search field is focused (caret, capital-letter keyboard with a blue Search key). (00:02.0; 0002.0, 0003.0)
3. Tap the "hide keyboard" button in the toolbar (inferred; taps are not marked, and it happens between the last frame with a caret and the first dismissal frame). The search caret disappears and the keyboard changes to a lowercase layout with a Return key. It does not go away. (00:04.5; 0004.0, 0004.5, 0005.0, 0005.5)
4. The keyboard finally slides away. The search panel and toolbar drop to the bottom, and the hide-keyboard icon is greyed out. It is unclear whether a second tap caused this. (00:06.0; 0006.0, 0006.5, 0007.0)
5. The keyboard comes back by itself. The editor briefly shows a caret at the end of the note text, and by 8.5 s the search field is focused again with the capital-letter keyboard. (00:07.5; 0007.5, 0008.0, 0008.5, 0009.0, 0009.5)

Expected (implied): Tapping "hide keyboard" hides the keyboard, even when the search panel and not the editor has focus. It should stay hidden until the user taps a field.

Actual: The keyboard stays visible for about 1.5 s after the first tap. It then hides for about 1 s, and reappears with focus moving to the editor and then back to the search field. Net result: the keyboard is not dismissed.

Key events: 0005.5, 0007.0, 0007.5, 0008.0, 0009.5

Missed by the author:

- After the first tap the keyboard layout changes to lowercase with a Return key and the search caret disappears, so focus appears to move to the editor first (0004.5 to 0005.5).
- The keyboard hides for about 1 s (0006.0 to 0007.0), then reappears on its own, with a caret in the editor (0008.0) before the search field is refocused (0008.5).

Claims:

- "Clicking Hide keyboard while the search panel is focused leaves the keyboard visible." [Observe that the keyboard remains visible.]: confirmed - The keyboard is up in 0005.5 after the tap. It is hidden only briefly (0006.0 to 0007.0) and is back in 0007.5 to 0009.5.
- "The button does nothing at all." ["Dismiss keyboard" button does nothing]: refuted - The keyboard does slide away at 6.0 to 7.0 s, so the button has some effect, but focus returns and the keyboard reopens.
