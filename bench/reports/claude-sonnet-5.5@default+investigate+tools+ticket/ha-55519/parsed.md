# real/ha-55519

_claude-sonnet-5.5@default, 25 s; looked at: nothing_

In a Safari PWA on macOS, the Home Assistant Add condition dialog on a large installation becomes very slow once the By target tree is shown and a target is picked. The right panel stays on 'Select a target' for tens of seconds, and Activity Monitor shows the 'Home Assistant Web Content' process at over 100% CPU. Search itself responded quickly.

## Add condition dialog (By target) nearly freezes in Safari PWA with many entities; Web Content process above 100% CPU

Class: **stuck**

Environment: Home Assistant frontend (ticket says 2026.11.0b2) in a Safari PWA window on macOS ('Not Secure' http URL, automation 'Presence', home 'Lake Estates'). Activity Monitor CPU window opened over it. Version and browser come from the ticket; the video does not show them.

Steps:

1. Open the automation and expand Option 1 (click at [280,388]); the Conditions list with '+ Add condition' is shown. (00:02.2; p003, p004)
2. Add condition dialog opens on 'By target' with the area tree and an empty 'Select a target' panel (the click on '+ Add condition' is not seen). (00:04.3; p006)
3. Type 'night' and then 'night lux' in the search box. Results appear promptly (entity binary_sensor.exterior_tempest_night_lux). (00:07.8; p012, p013, p016, p017)
4. Clear the search and click an entry in the tree at [421,247]. The entity list for Exterior Tempest renders, with icons flickering. (00:15.5; p050, p051, p053)
5. Click Night Lux at [400,422]. The row only highlights briefly and the right panel stays on 'Select a target'. Repeat: clicks at 41.7 s and 43.3 s have the same result. (00:24.8; p055, p056, p148, p152, p153)
6. While the dialog is stuck, Activity Monitor shows Home Assistant Web Content at 110.7% CPU (112.0% later), the top process. (00:32.1; p061, p115)
7. The list scrolls and jumps late (about 51 to 54 s) with icons vanishing. After switching tabs (click at [550,172]) the By type panel opens only after about 3 s. Back on By target, Night Lux again shows no result. (00:51.4; p155, p193, p201, p204, p249, p250)

Expected (speech): The dialog stays responsive. Clicking a target immediately lists its conditions in the right panel.

Actual: After a target is clicked, the right panel does not fill in for tens of seconds, and clicks appear not to register. Rendering lags (icons disappear, the list jumps). The Safari 'Home Assistant Web Content' process runs above 100% CPU at the same time.

Key events: p051, p055, p061, p115, p148, p155, p204, p249

Missed by the author:

- Search is fast (p012 to p017). The slowness starts when the By target tree or an entity list renders (p051 onward).
- The Activity Monitor window shows the HA Web Content process at about 110% CPU (p061), which points to the frontend rendering as the cause. It also shows screencapture and other processes active.
- Row icons vanish and reappear, and lists jump 219 px and 259 px (p155, p192, p193), which indicates lagging rendering.
- 'Lightning last energy' reverted to 'Lightning strike' about 2.5 s later with no click (p191). This is probably lagging virtual-list rendering, not a real state change.

Claims:

- "The frontend becomes unusably slow when adding a condition." [ticket]: confirmed - Target selection never shows a result in about 80 s of video (p055, p148, p249). Rendering is delayed (p155, p204).
- "Some mouse clicks are not even registered." [ticket]: confirmed - Repeated clicks on Night Lux (p055, p148, p152) have no lasting effect. Cause cannot be told apart from slow rendering.
- "The machine is bogged down." [ticket]: confirmed - Activity Monitor shows Home Assistant Web Content at 110.7% to 112% CPU (p061, p115).
- "It does not reproduce in Opera." [ticket]: not shown - Only Safari is recorded.
- "Has a lot of entities." [ticket]: confirmed - The area and entity tree is long (p006, p051). The video does not show the actual entity count.
- "No JavaScript errors." [ticket]: not shown - The console is not visible. The timeline's 'error text' cross-checks (p146, p234) only matched the tab labels 'By type Blocks'.
