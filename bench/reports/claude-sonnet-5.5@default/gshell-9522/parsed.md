# real/gshell-9522

_claude-sonnet-5.5@default, 22 s; looked at: frames/000123.jpg, frames/000445.jpg, frames/000323.jpg_

In GNOME Settings > Power, the Power Mode radio flips between Performance, Balanced and Power Saver without a visible click. A notice says Performance is disabled because of high temperature, yet the video ends with Performance selected. The estimated battery time also dropped from 2 h 12 min to 1 h 58 min.

## Power Mode changes to Performance by itself, although the UI says Performance is disabled due to high temperature

Class: **state-revert**

Environment: GNOME desktop (Nov 6, 10:24 PM). Settings > Power (General / Power Saving tab) next to a system monitor window for an Intel Core i5-10210U (Processor page). Battery at 70%. No audio and no user account is shown.

Steps:

1. Click in the system monitor's Processor view. It shows temperature, with 'Highest: 82°' at first and later 93 °C. (00:00.4; p003, p007)
2. The Settings window with the Power Mode list (Performance / Balanced / Power Saver) comes to the front. The trigger is not visible: the only click is p006, and it is in the monitor window. (00:04.0; p006, p008)
3. Power Saver is selected and the notice 'Performance mode temporarily disabled due to high operating temperature' appears. (00:05.8; p009)
4. The radio selection flickers between Performance, Balanced and Power Saver. The cursor stays over the list and no click is detected. The notice disappears and reappears. (00:13.3; p015, p016, p018, p019, p021, p022, p023, p024, p025, p027, p028)
5. The estimate changes to '1 hour 58 minutes remaining' and Performance ends up selected. The video ends in the Activities overview. (00:21.1; p026, p031)

Expected (implied): While the notice says Performance is disabled, Performance should not be selectable or become active. The chosen mode (Power Saver) should stay unchanged.

Actual: Power Saver is shown as selected while the notice is visible. The selection then flickers between modes with no detected click, and the end state has Performance selected (frame 000445). The notice had already disappeared at 16.6 s. The battery estimate dropped from 2 h 12 min to 1 h 58 min. Temperature in the monitor was 57 °C at 5.8 s, 67 °C at 15.3 s and 72 °C in the overview at 21.1 s.

Key events: p009, p018, p019, p021, p023, p024, p026, p028, p031

Missed by the author:

- The warning notice appears, disappears and reappears (p009, p018, p024, p028), so it is not a stable state.
- Power Saver flashed for 0.1 s (p022) and Performance for 0.5 s (p025) in the middle of the flicker.
- The end state has Performance selected (p031) although the notice had said it was disabled. Nothing shows a click selecting it.
