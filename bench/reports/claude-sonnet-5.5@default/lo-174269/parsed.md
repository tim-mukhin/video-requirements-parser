# real/lo-174269

_claude-sonnet-5.5@default, 30 s; looked at: frames/000171.jpg, frames/000752.jpg, frames/001297.jpg, frames/001541.jpg, frames/000929.jpg_

In LibreOffice Writer the author tries to create bookmarks with characters that the document and the Bookmark dialog call forbidden. The dialog accepts the name ":ss" and creates the bookmark with no error. The documented list of forbidden characters therefore doesn't match what the dialog enforces. There is no audio, so everything comes from the screen.

## Bookmark dialog accepts a name with ":" although the documentation lists ":" as forbidden; the dialog's hint lists a different set

Class: **wrong-data**

Environment: LibreOffice Writer, document bug174271.odt, Ubuntu/GNOME desktop with the Navigator sidebar open. The document has a note: 'Forbidden characters are: / \ @ * ? " ; , #'. A second paragraph lists '/ \ @ : * ? " ; , . #' as characters for another bug report. Recorded with Kooha.

Steps:

1. Open Insert > Bookmark... (the menu click is the first one shown; it's the same menu path as the one used again at 00:43). (00:01.5; p023, p024)
2. The Bookmark dialog opens. Its hint reads 'Forbidden characters: \@*?",#', which does not include ':' or ';'. Two bookmarks, comment_text_0 and comment_text_0 Copy 1, already exist. (00:05.6; p033, p057)
3. Type the name ':ss' in the Name field. The Insert button stays enabled and no error appears. (00:30.9; p091, p092)
4. Click Insert. The dialog closes and ':ss' appears in the Navigator under Bookmarks, so the bookmark was created. (00:31.3; p093, p094, p148)

Expected (implied): Names with characters that the document calls forbidden (including ':') should be rejected. Alternatively, the documented list and the dialog's hint should match what is actually enforced.

Actual: A bookmark named ':ss' is accepted and appears in the Navigator, although the document lists ':' among the forbidden characters. The dialog hint and the document list differ: the dialog omits '/', ';' and ':' while the document lists them. A second new bookmark, whose name is unreadable, also appears in the Navigator at the end.

Key events: p035, p057, p091, p093, p148

Missed by the author:

- The dialog's inline hint 'Forbidden characters: \@*?",#' differs from the list in the document (p057, p033). The author never comments on this.
- While typing there are many short-lived states: the name field flashes with other contents and the red invalid-name marker shows and disappears (p063, p064, p065). It is unclear which characters were tried between 00:10 and 00:30.
- A second new bookmark appears in the Navigator at the end, with an unreadable name (frame frames/001541.jpg). It was created around 00:46, after the author selected text and reopened the dialog (p174, p199).

Claims:

- "Another issue is in the documentation: many other forbidden characters are mentioned, but some of them work." [p097]: confirmed - This is the document's own text, not speech. The screen shows ':' is listed as forbidden but ':ss' was accepted as a bookmark name.
