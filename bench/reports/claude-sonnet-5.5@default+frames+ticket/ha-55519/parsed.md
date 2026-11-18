# real/ha-55519

_claude-sonnet-5.5@default, 33 s; looked at: frames/0000.0.jpg, frames/0005.0.jpg, frames/0010.0.jpg, frames/0020.0.jpg, frames/0030.0.jpg, frames/0045.0.jpg, frames/0060.0.jpg, frames/0084.0.jpg, frames/0002.0.jpg, frames/0013.0.jpg, frames/0016.0.jpg, frames/0025.0.jpg, frames/0070.0.jpg, frames/0078.0.jpg_

In the Safari PWA, the Add condition dialog on an automation page barely responds. Searching, expanding the target tree and picking a target all lag, and the right-hand panel never fills in. The reporter's Safari-only slowness claim is plausible, but the video cannot prove it.

## Add condition dialog (By target) freezes or is extremely slow in Safari PWA with many entities

Class: **stuck**

Environment: Home Assistant frontend 2026.11.0b2 (version from ticket) in a Safari 27 PWA window on macOS 15.8.1, 'Not Secure' http URL. Automation 'Presence' open in the editor. Home 'Lake Estates' has many areas and entities. The Add condition dialog is open.

Steps:

1. Open the automation 'Presence' and expand 'Option 1' in the Then do block (inferred click on the chevron). (00:02.0; 0002.0)
2. Click 'Add condition' (inferred). The dialog opens on the 'By target' tab, with the area tree on the left and 'Select a target' on the right. (00:05.0; 0005.0)
3. Type 'night' in the search box. Results appear, so search works. (00:10.0; 0010.0)
4. Refine the search to 'night lux'. One entity is shown, binary_sensor.exterior_tempest_night_lux. (00:13.0; 0013.0)
5. Clear the search to return to the By target tree. The tree is scrolled to the Tempest entities and Night Lux is highlighted. (00:16.0; 0016.0)
6. Click Night Lux in the list (inferred). The row is highlighted, but the right panel still says 'Select a target'. The state is the same 20 s and about 35 s later. (00:37.0; 0025.0, 0030.0, 0037.0, 0046.0, 0051.0)
7. Click the row again. The panel is still empty and the list has only moved slightly. (01:06.0; 0045.0, 0060.0)
8. Switch to the 'By type' tab. The tab changes, but the 'Select a condition' panel is empty. (01:11.0; 0070.0)
9. Return to 'By target'. The list is still stuck, with missing icons on some rows (for example Lightning strike). (01:18.0; 0078.0, 0084.0)

Expected (implied): The dialog stays responsive. Selecting a target immediately shows its available conditions in the right panel.

Actual: After a target is clicked, the right-hand panel stays on 'Select a target' for tens of seconds. The UI responds very late, and icons on list rows flicker in and out. The first search results in this video appear promptly.

Key events: 0016.0, 0025.0, 0046.0, 0051.0, 0060.0, 0078.0

Missed by the author:

- The search box was responsive at 0010.0 and 0013.0. The slowness appears when the By target tree is rendered or an entity is selected (0016.0 onward).
- Row icons for the Lightning entities appear and disappear between 0016.0 and 0084.0, which suggests rendering is lagging.
- The macOS menu bar shows CPU at about 15–19% and RAM at 75–78% throughout. There is no obvious CPU spike, so the cause is unclear.
- The automation has a Choose block with five options, which makes the page heavy as well. The Add condition button used is inside Option 1.

Claims:

- "The frontend becomes unusably slow when adding a condition" [the frontend becomes unusably slow]: confirmed - Over about 80 s the target selection never produces a result and the UI updates sluggishly.
- "Some mouse clicks were not registered" [some of the mouse clicks are not even registered]: confirmed - The click on Night Lux has no visible effect for a long time. The same selection state persists through 0025.0–0060.0.
- "The problem is specific to WebKit and does not occur in Opera" [Does not appear to reproduce inside Opera]: not shown - Only the Safari PWA is recorded.
- "The reporter has many entities" [Have a lot of entities]: confirmed - The target tree is long, with many areas and entities.
- "The browser console shows no errors" [No errors]: not shown - The console is not visible.
