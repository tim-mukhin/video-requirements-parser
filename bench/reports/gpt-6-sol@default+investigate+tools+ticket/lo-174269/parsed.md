# real/lo-174269

_gpt-6-sol@default, 100 s; looked at: frames/0005.0.jpg, frames/0006.0.jpg, frames/0014.0.jpg, frames/0020.0.jpg, frames/0030.5.jpg, frames/0045.0.jpg, frames/0011.0.jpg, frames/0013.0.jpg, frames/0017.0.jpg, frames/0021.0.jpg, frames/0025.0.jpg, frames/0028.0.jpg, frames/0029.5.jpg, frames/0031.0.jpg, looks/0012.50-0015.00-520_244_235_65/sheet.jpg, looks/0027.50-0031.40-520_245_236_63/sheet.jpg, looks/0005.30-0006.20-525_247_225_62/sheet.jpg, looks/0012.50-0014.50-790_363_345_90/sheet.jpg, looks/0027.80-0031.30-790_363_345_90/sheet.jpg, looks/0005.40-0006.10-790_360_345_100/sheet.jpg, frames/0027.0.jpg, frames/0032.0.jpg, frames/0044.5.jpg, looks/0027.80-0031.30-790_363_345_90/030.900.jpg, looks/0012.50-0014.50-790_363_345_90/014.100.jpg, looks/0005.40-0006.10-790_360_345_100/005.567.jpg, looks/0012.50-0014.50-790_363_345_90/014.233.jpg, looks/0027.80-0031.30-790_363_345_90/031.000.jpg, looks/0027.80-0031.30-790_363_345_90/028.000.jpg, looks/0015.00-0016.00-836_376_73_42/sheet.jpg, looks/0020.40-0021.30-836_376_80_42/sheet.jpg_

In LibreOffice Writer, a semicolon-only bookmark name leaves Insert disabled without a validation warning. By contrast, entering a backslash shows a warning whose forbidden-character list omits the semicolon, leaving the reason for the disabled button unexplained.

## Semicolon-only bookmark name is blocked without a validation warning

Class: **silent-fail**

Environment: LibreOffice Writer editing bug174271.odt, with the Navigator open. The version is not shown.

Steps:

1. Open Insert > Bookmark; the default name Bookmark 1 is selected. (00:03.1; p023, p024, p032, p033)
2. Replace the selected name with a semicolon. (00:14.0; p061, p064, p066)

Expected (implied): If a semicolon is forbidden, show the forbidden-character warning and include the semicolon in its list.

Actual: The semicolon-only name has no warning, but Insert remains disabled. A backslash entered earlier produced a red validation indicator and a warning that did not list semicolon.

Key events: p057, p061, p064, p066, p086, p089, p113

Missed by the author:

- The later successful bookmark is named :ss, not a semicolon-containing name: the enlarged frames and the resulting Navigator entry resolve the watcher's contrary interpretation [p086, p089, p113].
- The document displays a list of claimed forbidden characters behind the dialog; that document text is not the dialog's validation message [p035, p057].

Claims:

- "A semicolon-only name gets no warning and cannot be inserted." [ticket.md: Description]: confirmed - The field shows the character without the warning, while Insert is disabled.
- "The dialog warning omits semicolon." [ticket.md: Reporter's follow-ups]: confirmed - The warning displayed for a backslash lists other characters but not semicolon.
- "Every other listed forbidden character generates a warning." [ticket.md: Reporter's follow-ups]: not shown - The video does not visibly test every listed character.
- "Dots and colons can be used in bookmark names." [ticket.md: Reporter's follow-ups]: not shown - The video inserts a name beginning with a colon, but does not test a dot as a bookmark name.
