# real/gshell-7372

_claude-sonnet-5.5@default, 21 s; looked at: frames/000002.jpg, frames/000158.jpg, frames/000272.jpg_

A 9.8 s silent clip of a calendar popover being paged between February and January, with clicks on day cells. No error, wrong value or failed action is visible, and no audio explains what the author wanted to show. The cause cannot be determined from the evidence.

## Calendar popover month navigation: no visible fault (author's intent unknown)

Class: **not-a-bug**

Environment: A small (286×308) calendar popover with a month header and arrows, over a form with 'month' and 'late' fields and a text area. It is a GNOME-style desktop widget. No account or organization is visible.

Steps:

1. The calendar shows February. The cursor hovers over a day cell near '31'. (00:00.8; p001, p002)
2. The view changes to January. The trigger is not visible, most likely a click on the previous-month arrow. (00:03.0; p003)
3. The view returns to February. Clicks are not seen here because the cursor is lost from 4.0 s to 5.2 s. (00:05.2; p009)
4. Day cells are clicked in February (16, 10, 02, 23). The highlight moves and the view returns to January. (00:05.6; p010, p012, p016, p017, p022)

Expected (implied): Unknown. No speech or on-screen text states what the author expected. The implied expectation is that month navigation and day selection behave consistently.

Actual: The popover switches between January and February while the cursor moves over day cells. The frames show a correct layout: weeks start on Monday, the 03 cell stays highlighted in both months, and event dots appear on some days. I found no error, missing control or wrong value. The OCR digit differences (e.g. '60' for 09, '28' without 27) are misreads of the frames.

Key events: p003, p009, p022

Missed by the author:

- Between 00:03.8 and 00:04.6 the OCR shows cells flashing in and out ('27', '11') and changing colour while the view is January [p004, p005, p006, p007, p008]. This is probably hover highlighting and not an error.
- The view flips back to January at the end [p022] after the clicks on 02 and 23 in the February view [p016, p017]. It is unclear whether these clicks caused the jump. A click on an out-of-month day (such as 01 or 02 of March, or 31 of January) may switch the displayed month, which could be the behaviour the author meant to show.
