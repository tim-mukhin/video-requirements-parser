# real/zed-62058

_claude-sonnet-5.5@default, 13 s; looked at: nothing_

In Zed, typing a backtick, clicking elsewhere in the document and typing a second backtick puts the second backtick next to the first one. It does not go at the new cursor position. This corrupts text entry, and the cause may be stale dead-key or IME composition state on macOS.

## Backtick is inserted at the previous backtick position after moving the cursor with the mouse

Class: **wrong-data**

Environment: Zed 1.13.1 on macOS Tahoe 26.6. Default keymap and settings, apart from theme One Dark, the JetBrains New UI Icons (Dark) icon theme and font sizes. Any file. The keyboard layout is not stated.

Steps:

1. Open any file in Zed. (00:00.0; )
2. Type a backtick character (`). (00:00.0; )
3. Click elsewhere in the document to move the cursor. Do not use the arrow keys. (00:00.0; )
4. Type another backtick character (`). (00:00.0; )

Expected (speech): The second backtick is inserted exactly at the current cursor position, independent of where the previous backtick was typed.

Actual: The second backtick is inserted next to the first backtick, not at the new cursor position.

Key events: 

Claims:

- "Moving the cursor with the mouse, rather than the arrow keys, triggers the bug." [move the cursor to a different position in the document (e.g. click elsewhere - do not use arrow keys)]: not shown - There is no video. The ticket does not say whether arrow keys avoid the bug.
