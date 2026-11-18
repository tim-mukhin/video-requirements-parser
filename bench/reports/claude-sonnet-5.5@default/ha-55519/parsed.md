# real/ha-55519

_claude-sonnet-5.5@default, 30 s; looked at: frames/000382.jpg, frames/000599.jpg, frames/001297.jpg, frames/001876.jpg_

In the Home Assistant automation editor, the author opens "Add condition" and picks the "Night Lux" sensor in the By target list. The row gets a check mark, but the right pane stays on "Select a target" and never lists any conditions. Clicking other targets does not change the selection, and entity icons in the list vanish and come back. The video has no audio, so the expected behaviour is implied.

## Add condition dialog: selecting the Night Lux target shows no conditions and the pane stays on "Select a target"; list icons disappear

Class: **silent-fail**

Environment: Home Assistant web app in a macOS desktop window ("Not Secure — Automations – Home Assistant"). An automation named "Presence…" is open in the editor, with a Choose block and an Option 1 containing a time condition, a state condition and an occupancy condition. The Add condition dialog is open, using the By target / By type / Blocks tabs. The Home area lists exterior weather-station sensors (Lightning *, Night Lux, Peak Precipitation Intensity, Precipitation…). The Stats menu-bar app is also open.

Steps:

1. In the automation editor, click inside the Option 1 conditions area. The Add condition dialog (By target) opens, though the click on the add button itself is not clearly visible. (00:02.2; p003, p006)
2. Type "night" in the search box. It filters to condition types and then to the entity binary_sensor.exterior_tempest_night_lux. The cursor is not followed 00:06.4-00:12.5, so these inputs are not visible. (00:07.8; p012, p016, p017)
3. Clear the search and click the "Night Lux" target in the list. The row is highlighted with a check mark. (00:15.5; p050, p051, p052)
4. Click Night Lux again. The right pane still shows "Select a target" and no conditions for the sensor appear. (00:24.8; p054, p055)
5. Click Night Lux and the neighbouring row repeatedly. The Night Lux row stays checked and the pane stays empty. Meanwhile the Lightning rows lose their icons ("Lightning strike" ends up with no icon) and the list re-renders. (00:41.7; p147, p151, p162, p166, p186, p187, p188)
6. Click "Peak Precipitation Intensity" (535,450). The selection does not move to it. Night Lux stays checked and the pane stays on "Select a target". (01:18.0; p248, p249, p250, p251)

Expected (implied): Selecting a target in the By target list should show the conditions available for that target in the right pane. Clicking another target should move the selection to it.

Actual: Night Lux gets a check mark, but the right pane keeps saying "Select a target" and shows no conditions, with no error. The selection stays on Night Lux and does not follow later clicks. Entity icons in the list disappear and "Lightning last energy" briefly changes to "Lightning strike" after a re-render. The dialog's tab labels ("By type", "Blocks") flicker, disappear and reappear.

Key events: p050, p051, p054, p055, p145, p147, p186, p187, p188, p224, p229, p248, p251

Missed by the author:

- The tab labels "By type" and "Blocks" disappeared for 29.7 s at 00:39.9 and again at 01:09.5 (p145, p229). The cross-check flags this as error text, but it is the tab bar of the dialog flickering or disappearing.
- "Lightning last energy" changed back to "Lightning strike" after 2.5 s with no click before it (p186). The list re-rendered and the icons of the Lightning rows were lost (p187, p188).
- The Mac was under heavy load at 00:32-00:38: Home Assistant Web Content used 100-112% CPU, and searchpartyd used 86%. This may explain the sluggish and flickering UI (p060, p086, p114, p137).
