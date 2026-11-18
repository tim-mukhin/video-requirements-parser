# real/commons-wikidata-coord-zoom

_gpt-6-sol@default, 32 s; looked at: frames/moments/p001.jpg, frames/moments/p023.jpg, frames/moments/p027.jpg, frames/0004.0.jpg, frames/0004.5.jpg, frames/0010.0.jpg, frames/0010.5.jpg, frames/0011.0.jpg, frames/0001.5.jpg, frames/0002.0.jpg, frames/000064.jpg, frames/000132.jpg, frames/000308.jpg, frames/0008.5.jpg_

Clicking a zoom control in Wikidata's coordinate-location map preview can close the preview while the statement remains in edit mode. The video shows this after a + click and after a second − click, interrupting further map adjustment.

## Coordinate map preview closes after zoom-control clicks

Class: **intermittent**

Environment: Wikidata coordinate-location statement editor; Wikimedia maps preview; an OpenStreetMap reference is visible.

Steps:

1. Open the existing coordinate-location statement for editing (the trigger is not visible). (00:01.5; p003)
2. Open the map preview (the trigger is not visible). (00:02.1; p005)
3. Click the preview's + zoom control. (00:04.3; p010, p013, p014, p015, p016)

Expected (implied): The map zooms while its preview remains open for further adjustment.

Actual: The preview disappears by 4.7 s, without an error; the coordinate field still reads 46°4′0.91″N, 11°7′20.78″E. On the later attempt, a first − click leaves the preview open, but a second − click at 10.7 s is followed by its disappearance. The timeline establishes the click times; the frames show the controls and the closing preview.

Key events: p005, p010, p013, p014, p015, p016, p031, p033, p036

Missed by the author:

- The screen shows an existing coordinate value, precision ±0.00001°, and an unchecked “set manually” option before the + click [p005].
- The timeline records two − clicks on the later attempt, not one; frames show the preview still open after the first [p031, p032, p033, p036].
- The brief OpenStreetMap text and click-label flashes correspond to the visible reference and interaction, not a separate error [p023, p027, p034].

Claims:

- "There is a user-interaction bug with the Wikidata coordinate picker zoom button." [ticket.md]: confirmed - The frames show clicks on the map's zoom controls, and the timeline records the preview closing afterward. The first − click does not immediately close it.
