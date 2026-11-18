# real/lo-174287

_claude-sonnet-5.5@default, 21 s; looked at: frames/000130.jpg, frames/000241.jpg, frames/000209.jpg_

A silent screen recording (no audio, no visible cursor) of an empty LibreOffice Writer document on a touch-style device. The Format > Text and File > New submenus open and close, and the document stays empty. No failure is visible, and the author's intent is unknown.

## No visible defect: menu walkthrough in empty LibreOffice Writer document

Class: **not-a-bug**

Environment: LibreOffice Writer, 'Untitled 1', Liberation Serif 12 pt, 100% zoom, English (USA), Default Page Style. Mobile-style top bar (Thu Nov 5 09:51, battery 52%, screen recorder timer). No account or organization seen.

Steps:

1. The Format menu opened with its Text submenu expanded (Bold, Italic, Underline and so on). The trigger is not visible. (00:24.1; p004)
2. The menu closed and the normal menu bar returned. The document is still empty (0 words, 0 characters). (00:25.4; p005)
3. The File menu opened with its New submenu expanded (Text Document, Spreadsheet and so on). The trigger is not visible. (00:39.0; p007)
4. The menu closed and the document is still empty and unchanged. (00:42.8; p008)

Expected (implied): Unclear. Nothing indicates what the author expected. The menus open and close normally.

Actual: Menus open and close and the document stays empty. No error, no state change and no lost content is seen. Some frames show a 'Header (Default Page Style)' marker with a dashed line, which is the normal header hint in Writer. The only anomalies are OCR artefacts: the timer read '60:0' for one frame (p001), and the title bar was garbled to 'I ntitled 1—I ibreOffice' while the menu overlapped it (frame 000130). Frame 000241 shows the title bar and the timer as normal. Most likely candidate for a real issue: none identified.

Key events: p004, p005, p007, p008

Missed by the author:

- The timer flicker '0:08' → '60:0' → '0:10' (p001, p002) is OCR noise on the recorder timer and not an app issue.
- The 'Edit View' text that appeared for 1.9 s (p003) is the menu bar partly covered by a menu opening.
