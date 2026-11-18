# real/commons-wikidata-coord-zoom

_claude-sonnet-5.5@default, 18 s; looked at: frames/000132.jpg, frames/000221.jpg_

On a Wikidata coordinate-location statement in edit mode, clicking the map's zoom-in "+" button closes the preview popup instead of zooming the map. The same thing happens on a second attempt. The author's speech is only "Thank you.", so there is no narration of the problem.

## Clicking zoom "+" on the coordinate preview map closes the popup instead of zooming

Class: **silent-fail**

Environment: Wikidata item page in a browser (Palazzo Calepini (Trento)), 'coordinate location' statement in edit mode with the 'will be displayed as' Wikimedia maps preview (46°4'0.91"N, 11°7'20.78"E). Account not visible.

Steps:

1. Open the 'coordinate location' statement for editing (the trigger is not visible; the edit form appears with the map preview). (00:01.5; p003, p005)
2. Hover the map's zoom-in '+' button (a 'Left↓' tooltip shows), then click it. (00:04.3; p009, p010, p011)
3. The preview popup (map and coordinates) disappears at once and the map is not zoomed. The edit form stays open. (00:04.7; p012, p013, p014, p015, p016, p017)
4. Repeat: click the 'edit' link, then click '+' again. The popup closes again with no zoom. (00:10.2; p028, p031, p032, p033, p034, p036)

Expected (implied): Clicking '+' zooms the preview map in and keeps the popup open.

Actual: Each click on '+' closes the 'will be displayed as' popup. No zoom is visible and no error appears. The edit form stays open, with the unchanged coordinates.

Key events: p010, p011, p012, p013, p031, p033, p034, p036

Missed by the author:

- Between the two attempts the author clicked publish/cancel (p019, p021, p024). The statement shows as saved with a reference 'stated in OpenStreetMap' (p022, p026, p027), and a 'Left t' tooltip flashed (p023). The video does not show whether the statement changed.
- The cursor is not followed after 00:12.3, so the final state is not confirmed (s025).

Claims:

- "Thank you." [u001]: not shown - The utterance says nothing about the problem.
