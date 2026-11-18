# real/lo-174269

_claude-sonnet-5.5@default, 16 s; looked at: nothing_

In LibreOffice Writer's Insert > Bookmark dialog, typing a semicolon in the Name field shows no warning, yet the Insert button stays disabled. The warning text under the field also leaves out the semicolon. Users get no explanation for why the bookmark can't be inserted.

## Bookmark name with semicolon: no warning shown, Insert button disabled, and semicolon missing from forbidden-characters message

Class: **silent-fail**

Environment: LibreOffice Writer, Insert > Bookmark dialog. Version, OS and build are not given. Reporter has a recording.mp4, which was not available here.

Steps:

1. In Writer, open Insert > Bookmark. (00:00.0; )
2. In the Name field, type each of the characters / \ @ * ? " , # one at a time. Each one shows a warning. (00:00.0; )
3. Type a semicolon (;) in the Name field. (00:00.0; )
4. Observe that no warning appears, the Insert button is disabled, and the warning message lists no semicolon. (00:00.0; )

Expected (speech): Semicolon triggers the same warning as the other forbidden characters. The warning message lists all forbidden characters, including the semicolon.

Actual: Semicolon gives no warning, but the Insert button stays inactive, so the bookmark can't be inserted. The message under the Name field does not mention the semicolon.

Key events: 

Claims:

- "Semicolon is the only forbidden character that gives no warning." [All characters, EXCEPT semicolon, generates a warning]: not shown - Ticket text only; there is no video to check against.
- "bookmark.hxx line 91 omits ';' from aForbiddenChars, which is why no warning appears." [We are missing from here some forbidden characters: I inserted here ';' and if inserted we get a warning]: not shown - Code-level hypothesis from the reporter. It was not checked.
- "content.cxx lists '.' and ':' as forbidden, but the UI accepts bookmarks containing them." [But in UI we can insert bookmarks with dots and colon.]: not shown - Not verifiable from the ticket alone.
- **R1** [stated] Typing a semicolon in the bookmark Name field shows the same warning as the other forbidden characters. (proposed by reporter) - 
- **R2** [stated] The warning message lists every forbidden character, including the semicolon. (proposed by reporter) - 
- **R3** [open_question] Decide whether '.' and ':' are allowed in bookmark names. The code in content.cxx, the code in bookmark.hxx and the documentation disagree. Is there a standard or documentation for permitted characters? (proposed by reporter) - 
