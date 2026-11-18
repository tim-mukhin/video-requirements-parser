# real/joplin-16462

_claude-sonnet-5.5@default, 25 s; looked at: frames/0008.5.jpg, frames/0004.5.jpg, frames/0009.5.jpg_

In the Joplin iOS note editor with the search panel focused, tapping the toolbar's hide-keyboard button does not leave the keyboard hidden. After a first tap around 4.4 s the keyboard first stays up with focus apparently moved to the editor. It then slides away for about 1 s and comes back with the search field focused again. A second tap at 8.6 is followed by the keyboard still showing at 9.5 s, so the user cannot dismiss the keyboard while searching.

## Hide-keyboard toolbar button does not dismiss the keyboard while the search field is focused

Class: **state-revert**

Environment: Joplin mobile on iOS (portrait iPhone, dark theme, 5G, screen recording 12:33). Note 'Testing!' in notebook 'Mess', Markdown editor with the formatting toolbar and the search panel open. The app version is not visible; the ticket says 13.7.3.

Steps:

1. Note is open in the editor with the keyboard and formatting toolbar up. Search panel opens, with the 'Search for...' field and a caret, above the toolbar (the trigger is not visible, most likely the toolbar search button). (00:01.8; p002, p003)
2. Tap the hide-keyboard toolbar button. The tap is not drawn at this moment. The search caret disappears and the keyboard changes to a lowercase layout with a Return key, which suggests focus moved to the editor. The keyboard stays on screen. (00:04.4; p019, p020, p022, p025, p029)
3. The keyboard slides away and the search panel and toolbar drop to the bottom, for about 1 s. (00:05.9; p037, p038)
4. The keyboard comes back on its own with no visible trigger. The editor briefly shows a caret, then the search field is focused again with the capital-letter keyboard and a blue Search key. (00:07.4; p039, p040, p041, p056)
5. Tap the hide-keyboard button again (TAP at [936,1539], which is the keyboard icon in the toolbar). The keyboard is still visible with the search caret at 9.5 s. (00:08.6; p064)

Expected (implied): Tapping hide-keyboard hides the keyboard and keeps it hidden, even when the search field, not the editor, has focus.

Actual: The keyboard stays up after the first tap and focus moves away from the search field. It hides only briefly, then reappears with the search field refocused. After the second tap it is still visible. The net result is that the keyboard is never dismissed.

Key events: p019, p029, p037, p039, p056, p064

Missed by the author:

- The keyboard hides for about 1.5 s (p037, p038) and then reappears by itself, which the ticket does not mention.
- After the first tap the keyboard turns lowercase with a Return key and the search caret disappears (p022 to p029). This looks like focus moving to the editor before the keyboard hides. This is inferred from frame 0004.5 and the watcher notes.
- The video shows two taps on the button, the first at about 4.4 s and the second at 8.6 s. The ticket describes one.

Claims:

- "Clicking Hide keyboard with the search panel focused leaves the keyboard visible (ticket)." [ticket]: confirmed - Frames 0004.5 and 0008.5 to 0009.5 show the keyboard up after a tap on the hide-keyboard icon.
- "The button does nothing (ticket title)." [ticket]: refuted - The keyboard layout changes and the keyboard slides away at about 5.9 to 7.4 s, so the button has some effect before focus returns. This is a hide-then-reappear revert, a slightly different symptom from the ticket's 'remains visible'.
