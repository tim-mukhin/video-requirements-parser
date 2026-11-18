# real/gshell-7372

_claude-sonnet-5.5@default, 23 s; looked at: frames, frames/0000.0.jpg, frames/0002.0.jpg, frames/0003.0.jpg, frames/0004.0.jpg, frames/0005.0.jpg, frames/0006.0.jpg, frames/0007.0.jpg, frames/0009.0.jpg_

In the GNOME calendar widget, clicking a dimmed day from an adjacent month switches the month. The selected day briefly shows a focus ring, which disappears once the event dots load. The keyboard focus is lost, as the ticket describes.

## Calendar: focus ring on the selected day is lost after switching month via a dimmed day

Class: **state-revert**

Environment: GNOME Shell calendar/notification popup (month view, Feb/Jan 2024, today = 3). Frame 0000.0 shows a different window with the issue text. Version and Wayland are not visible, only given in the ticket.

Steps:

1. Open the calendar popup showing February. The dimmed 31 (January) is under the pointer. (00:02.0; 0002.0)
2. Click the dimmed 31 (inferred click). The view switches to January with the dots loaded. 31 is highlighted at the bottom, with no focus ring. (00:03.0; 0003.0)
3. Click the dimmed 01 (February) in the last row (inferred click). (00:04.0; 0004.0)
4. The view switches to February. 01 has a blue focus ring and no event dots have loaded yet. (00:05.0; 0005.0)
5. Event dots appear on 7, 14 and Mar 2. The focus ring on 01 is gone. 01 stays grey-highlighted, apparently only because it is selected. (00:06.0; 0006.0)

Expected (implied): The selected day (Feb 1) keeps keyboard focus after the month change.

Actual: The focus ring on the selected day appears briefly and disappears once the event dots load. The ticket says focus moves to the panel widget; the video cannot show that.

Key events: 0005.0, 0006.0

Missed by the author:

- The first switch to January (0003.0) shows no focus ring at all, so the loss may already have happened there.

Claims:

- "Focus is shown briefly, then lost when the event dots load" [Looks like it has focus for a brief time, then loses it when the events dots are loaded.]: confirmed - The ring is visible at 0005.0 with no dots. It is gone at 0006.0 once the dots are shown.
- "Same happens when clicking a dimmed day with the cursor" [Same thing happens if you click on one of the dimmed days with the cursor.]: confirmed - The video uses only mouse clicks, and the ring is lost after the click at 0004.0.
- "Focus goes to the panel widget" [it is given to the panel widget]: not shown - No panel is visible in the frames, only the calendar.
- "With no events to load it works properly" [If there are no events to load it works properly.]: not shown - Both month switches shown have events.
- "Keyboard navigation and Enter trigger the problem" [using keyboard select a day ... and press enter]: not shown - The video shows only pointer clicks; no key presses are visible.
