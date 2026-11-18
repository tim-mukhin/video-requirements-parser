# real/gshell-7372

_claude-sonnet-5.5@default, 16 s; looked at: nothing_

In GNOME Shell's calendar widget, selecting a dimmed day from an adjacent month, by keyboard Enter or by mouse click, switches the month. Keyboard focus then moves to the top panel instead of staying on the selected day. Keyboard users lose their place, and Left/Right arrows then move through the Activities button and quick menu.

## Calendar widget: selected day loses keyboard focus to panel after month change

Class: **state-revert**

Environment: GNOME Shell 45.3, Fedora 39, Wayland. Calendar/notifications widget in the top panel. No accounts or organizations mentioned.

Steps:

1. Open the calendar/notifications widget from the panel. (00:00.0; )
2. Click on a day. (00:00.0; )
3. Using the keyboard, move to a dimmed day belonging to the next or previous month and press Enter. Clicking a dimmed day with the mouse also reproduces it. (00:00.0; )

Expected (speech): The calendar switches month and keyboard focus stays on the selected day.

Actual: The month changes, but focus ends up on the panel widget. Pressing Left or Right then moves to Activities or the quick menu. The reporter says focus is briefly on the day and is lost when the event dots load. With no events to load, focus is kept.

Key events: 

Claims:

- "Focus is lost after switching month and goes to the panel widget." [the focus is lost (it should be on the just selected day) and it is given to the panel widget]: not shown - Ticket text only; the recording was not available.
- "Focus is lost when the event dots are loaded, and the bug does not occur when there are no events." [Looks like it has focus for a brief time, then loses it when the events dots are loaded. If there are no events to load it works properly.]: not shown - This is the reporter's hypothesis and could not be checked without the recording.
- "The same thing happens when clicking a dimmed day with the mouse." [Same thing happens if you click on one of the dimmed days with the cursor.]: not shown - No video; reported only in the ticket text.
