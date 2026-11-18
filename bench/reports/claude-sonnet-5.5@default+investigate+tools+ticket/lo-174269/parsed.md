# real/lo-174269

_claude-sonnet-5.5@default, 28 s; looked at: looks/0009.00-0021.00-700_330_520_330/sheet.jpg_

In Writer's Insert > Bookmark dialog, a name containing ';' leaves the Insert button greyed out. The dialog shows no red warning icon and no hint text, and the hint's forbidden-characters list omits ';'. The user gets no explanation for why the bookmark can't be inserted. The video confirms the ticket's semicolon claims but does not show the other forbidden characters being tried.

## Bookmark dialog: ';' in Name disables Insert with no warning, and ';' is missing from the 'Forbidden characters' hint

Class: **silent-fail**

Environment: LibreOffice Writer on Linux (GNOME, dark theme, recorded with Kooha), document bug174271.odt (the ticket is 174269), Navigator sidebar open. The document has two existing bookmarks, both listed as comment_text_0. The document text lists the forbidden characters '/ \ @ * ? " ; , #'.

Steps:

1. Click the Insert menu in the menu bar (the document is in front). (00:01.5; p023)
2. Click the Bookmark... item. The Bookmark dialog opens with the default name 'Bookmark 1' (the click on the item is not shown; the dialog appears at 3.2 s). (00:03.1; p032, p033, p054)
3. Clear the name field. The field is empty and shows a red 'invalid' icon and the hint 'Forbidden characters: /\@*?",#', with no ';' in it. (00:05.6; p057)
4. Type ';' into the Name field. The red icon and the hint vanish, the list jumps up and Insert stays greyed out, with no message. The OCR reads the field going through "1", "", "M1", "", ";", "" (keys are not seen). (00:12.5; p061, p064, p065)
5. Move the cursor onto the disabled Insert button. ';' is still in the field and Insert is still disabled (a hover, not a click). The field is retyped several times between 13 s and 21 s with the same result. (00:21.0; p078, p079)
6. Contrast: type ':ss' as the name. Insert becomes active and is clicked, and the bookmark appears in the Navigator. (00:31.3; p086, p089, p113)
7. Contrast: a bookmark named '.....' is inserted in the same way in a second dialog. (00:46.1; p170, p200)

Expected (implied): Typing ';' should be handled like the other forbidden characters: the red warning icon shows and the hint lists ';'. Or ';' should be accepted and Insert enabled.

Actual: With ';' in the Name field there is no warning icon and no hint, so the hint list never mentions ';'. Insert stays greyed out with no explanation. ':' and '.' names insert fine.

Key events: p057, p061, p064, p065, p078, p086, p089, p170

Missed by the author:

- The red icon and the hint are already on screen with an empty Name field (p057, 5.6 s to 12.1 s), before any forbidden character is typed.
- The dialog layout jumps up when the hint disappears after ';' is typed (p064, p065).
- The document is bug174271.odt, not 174269.

Claims:

- "Semicolon gives no warning, but Insert is inactive" [ticket]: confirmed - Frames from 12.7 s to 21 s show ';' in the field, no red icon, and Insert greyed out.
- "The forbidden-characters message does not include the semicolon" [ticket]: confirmed - The hint at 5.6 s to 12.1 s reads /\@*?",# with no ';' (p057).
- "All other characters generate a warning in the Name field" [ticket]: not shown - The only character typed in the dialog's Name field is ';' (besides ':ss' and '.....'). The other forbidden characters are not tried.
- "Bookmarks with ':' and '.' can be inserted in the UI" [ticket]: confirmed - ':ss' and '.....' are inserted and listed in the Navigator (p113, p200).
- "Reproducible: Always" [ticket]: not shown - ';' is entered several times in one dialog, always with Insert disabled. Only one session is shown.
