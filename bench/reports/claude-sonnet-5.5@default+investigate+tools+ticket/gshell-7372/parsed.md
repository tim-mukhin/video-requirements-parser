# real/gshell-7372

_claude-sonnet-5.5@default, 22 s; looked at: frames/0005.0.jpg, frames/0006.0.jpg, frames/0008.0.jpg_

In the GNOME Shell calendar popup, clicking a dimmed day from an adjacent month switches the month. The selected day shows a focus ring for about a second, and the ring disappears when the event dots load. This matches the ticket's 'focus lost when dots load' for mouse clicks. The video shows no keyboard use and no panel, so it cannot confirm that focus moves to the panel.

## Calendar: selected day loses focus ring after month switch via a dimmed day, once event dots load

Class: **state-revert**

Environment: GNOME Shell calendar popup, month view (Feb/Jan 2024, today = 3 Feb), 286x308 recording with no audio. The ticket gives GNOME 45.3, Fedora 39 and Wayland; the video does not show these.

Steps:

1. With the calendar showing February, hover the dimmed '31' (January) and click it. The view switches to January with dots. The click is inferred (the cursor stopped, then the screen reacted). (00:03.0; p002, p003)
2. Click the dimmed '01' (February) in the last row of January. The click is inferred and the cursor is not tracked 4.0-5.2 s. The view switches to February, and 01 has a blue focus ring and no event dots yet (frame 0005.0). (00:05.2; p008, p009)
3. Wait about 0.4 s. Event dots appear under 07, 14 and 02 Mar, and the focus ring on 01 is gone (frame 0006.0). 01 stays grey only as the selected day. (00:05.6; p011)

Expected (implied): The newly selected day (1 Feb) keeps keyboard focus and its focus ring after the month switch and the dots loading.

Actual: The ring appears right after the switch and is gone once the dots load. No ring is visible on the selected day afterwards. The ticket says focus ends up on the panel; that is not visible.

Key events: p009, p011, p003

Missed by the author:

- After the first switch to January (3.0 s) no focus ring is visible on the clicked day in the frames checked. Dots and day states change at 3.8-4.6 s (p004-p008).
- Later clicks at 5.6-7.9 s (16, 10, 02, 23) move the grey highlight, and the ring appears on 01 again around 8.0 s (frame 0008.0), then the view returns to January at 9.0 s (p022). This was not examined in detail.

Claims:

- "Focus is held briefly, then lost when the event dots load" [ticket]: confirmed - Ring on 01 at 5.0 s with no dots; at 6.0 s the dots are present and the ring is gone.
- "The same happens when clicking a dimmed day with the mouse" [ticket]: confirmed - Both month switches in the video are done by mouse click on a dimmed day.
- "Focus goes to the panel widget / left-right arrows move to Activities or the quick menu" [ticket]: not shown - Only the popup is in view and no keys are seen.
- "It works when there are no events to load" [ticket]: not shown - Both months switched to in the video have events.
- "Keyboard navigation plus Enter triggers it" [ticket]: not shown - No key presses are visible (keys are not seen in this video).
