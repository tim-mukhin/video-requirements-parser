# real/gshell-7372

_gpt-6-sol@default, 43 s; looked at: frames/0004.0.jpg, frames/0004.5.jpg, frames/0005.0.jpg, frames/0008.5.jpg, frames/0009.0.jpg, frames/moments/p002.jpg, frames/moments/p015.jpg, frames/0005.5.jpg, frames/0006.0.jpg, frames/0002.5.jpg, frames/0003.0.jpg, frames/0009.5.jpg, frames/000125.jpg, frames/000136.jpg, frames/0007.5.jpg, frames/0008.0.jpg, looks/0004.80-0005.60-0_0_286_308/sheet.jpg, looks/0008.50-0009.30-0_0_286_308/sheet.jpg_

Selecting a dimmed day in another month changes the displayed month, but the focus outline on that day disappears shortly afterward. The same visible loss occurs when navigation moves from February 1 to January 31, leaving the keyboard focus unclear.

## Calendar day loses visible focus after switching months

Class: **state-revert**

Environment: GNOME Shell calendar popover. The ticket reports GNOME 45.3 on Fedora 39 with Wayland; the video does not verify those details.

Steps:

1. Open the calendar popover to February (the trigger is not visible). (00:00.8; p001)
2. Select the dimmed February 1 in January's calendar (the trigger is not visible). The calendar switches to February. (00:04.6; p008, p009)

Expected (implied): Focus remains on the selected day after the month changes.

Actual: February 1 briefly has a blue focus outline after the switch, then loses it as event dots appear. Later, the outline moves onto the dimmed January 31 in February, but disappears after January opens. The frame-by-frame view settles the timing more precisely than the watcher's half-second frames: the first outline is visible around 5.0 s and gone by about 5.2 s.

Key events: p008, p009, p016, p018, p019, p021, p022

Missed by the author:

- The blue-filled February 3 remains visible even while January is displayed; it is distinct from the selected day's transient focus outline [p003, p009].

Claims:

- "Selecting a dimmed day can switch months and lose the day's visible focus." [ticket: Bug summary; What happened]: confirmed - The video shows the outline briefly on February 1 after the month switch, then shows it disappear.
- "Keyboard navigation into another month has the same result." [ticket: Steps to reproduce]: confirmed - With the pointer elsewhere, the outline moves from February 1 to dimmed January 31; it disappears after January opens. The keys themselves are not visible.
- "Focus moves to the panel widget, so left/right selects Activities or quick menu." [ticket: What happened]: not shown - The recording shows the calendar losing its outline, not subsequent panel selection.
- "The outline disappears when event dots load." [ticket: Relevant logs, screenshots, screencasts etc.]: confirmed - The frame-by-frame view shows the outline vanish as dots appear; it does not establish that loading the dots causes the focus loss.
- "It works properly when there are no events to load." [ticket: Relevant logs, screenshots, screencasts etc.]: not shown - The video contains no event-free comparison.
