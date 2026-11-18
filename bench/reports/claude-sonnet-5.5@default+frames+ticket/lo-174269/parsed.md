# real/lo-174269

_claude-sonnet-5.5@default, 37 s; looked at: frames, frames/0000.0.jpg, frames/0006.0.jpg, frames/0012.0.jpg, frames/0018.0.jpg, frames/0024.0.jpg, frames/0030.0.jpg, frames/0036.0.jpg, frames/0042.0.jpg, frames/0048.0.jpg, frames/0009.0.jpg, frames/0015.0.jpg, frames/0021.0.jpg, frames/0027.0.jpg, frames/0039.0.jpg, frames/0045.0.jpg, frames/0050.0.jpg, frames/0052.0.jpg, frames/0033.0.jpg, frames/0003.0.jpg_

In LibreOffice Writer's Insert > Bookmark dialog, the recording shows a semicolon typed into the Name field. The Insert button stays greyed out, and no red warning icon appears. The hint text "Forbidden characters: /\@*?",#" omits the semicolon. Colon and dot names do get inserted as bookmarks.

## Bookmark dialog: ';' disables Insert silently and is missing from the forbidden-characters hint

Class: **silent-fail**

Environment: LibreOffice Writer on Linux (GNOME, dark theme), document bug174271.odt, Navigator sidebar open. The document has two existing bookmarks, comment_text_0 and comment_text_0 Copy 1. The screen is recorded with a GNOME screen recorder.

Steps:

1. Document with the list of forbidden characters is open; the recorder start dialog is visible. Recording starts. (00:00.0; 0000.0)
2. Open Insert > Bookmark... (inferred from the Insert menu being opened later in the video and the dialog appearing at 6.0 s). The dialog opens with an empty Name field. The red 'invalid' icon and the hint 'Forbidden characters: /\@*?",#' show, and the hint has no semicolon. (00:06.0; 0006.0, 0009.0)
3. Click in the Name field and type a semicolon (inferred). The field shows ';', the red icon and the hint disappear, and Insert stays greyed out. (00:15.0; 0015.0)
4. Hover over the Insert button (the click is inferred). It is still disabled, with no message explaining why. (00:21.0; 0021.0)
5. Close the dialog without inserting a semicolon bookmark. (00:30.0; 0030.0)
6. For comparison: a bookmark named ':ss' was inserted, and a bookmark named '.....' was inserted after a second dialog opened. Both appear in the Navigator. The reporter says colon and dot work in the UI, and the video agrees. (00:39.0; 0033.0, 0039.0, 0042.0, 0045.0)

Expected (implied): A semicolon should be treated like the other forbidden characters: the red warning icon shows, the hint text lists ';', and Insert is disabled for a stated reason. Alternatively, ';' should be allowed as a bookmark character.

Actual: With ';' typed, the dialog shows no warning icon, and the hint omits ';'. Insert is disabled with no explanation, so the user cannot tell why.

Key events: 0009.0, 0015.0, 0021.0

Missed by the author:

- The red icon and the hint text already show while the Name field is empty (6.0, 9.0), before any forbidden character is typed.
- The dialog layout shifts (list moves up) when the hint disappears after typing (15.0).
- The title of the source document is bug174271.odt, while the ticket is 174269.

Claims:

- "Semicolon gives no warning but Insert is inactive" [Just semicolon is behaving different, no warning when inserted, but bookmark can not be inserted, 'Insert' button is not active.]: confirmed - At 15.0 and 21.0 the field contains ';', there is no red icon, and Insert is greyed out.
- "The warning message does not include the semicolon" [in the warning message, below the Name field, we don't have the semicolon character]: confirmed - At 6.0 and 9.0 the hint reads /\@*?",# with no ';'.
- "Other forbidden characters give a warning" [All characters, EXCEPT semicolon, generates a warning]: not shown - Only the empty field and the semicolon are shown in the dialog. The other characters are not typed on screen.
- "Colon and dot can be inserted in bookmark names" [in UI we can insert bookmarks with dots and colon]: confirmed - The Navigator lists a ':ss' bookmark (33.0) and a '.....' bookmark (42.0, 45.0).
