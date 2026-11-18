# real/commons-wikidata-coord-zoom

_claude-sonnet-5.5@default, 30 s; looked at: frames, frames/0000.0.jpg, frames/0002.0.jpg, frames/0004.0.jpg, frames/0006.0.jpg, frames/0008.0.jpg, frames/0010.0.jpg, frames/0012.0.jpg, frames/0014.0.jpg, frames/0001.0.jpg, frames/0004.5.jpg, frames/0005.0.jpg, frames/0009.0.jpg, frames/0010.5.jpg, frames/0011.0.jpg_

In the Wikidata statement editor for 'coordinate location', clicking the map's zoom buttons does not zoom the map. The coordinate popup fades out and closes instead. This blocks use of the zoom controls in the coordinate picker.

## Coordinate picker popup closes and the map does not zoom when a zoom (+/−) button is clicked

Class: **silent-fail**

Environment: Wikidata item page in a browser. Statement 'coordinate location' (46°4'0.91"N, 11°7'20.78"E, Trento) with reference 'stated in: OpenStreetMap'. Palazzo Calepini (Trento) is the item. Not logged in or otherwise identified in the frames.

Steps:

1. On the item page, the pointer is on 'edit' beside the coordinate location statement, which is in read-only mode (inferred click on edit). (00:01.0; 0001.0)
2. The statement is in edit mode. The coordinate input is focused and the 'will be displayed as' map popup is open. (00:02.0; 0002.0)
3. Move the pointer to the map's '+' zoom button and click it (click inferred). The button shows a pressed/focused state with a tooltip. (00:04.5; 0004.0, 0004.5)
4. The popup is gone. The map did not zoom and the pointer now rests over '1 reference'. (00:05.0; 0005.0, 0006.0)
5. Repeat: the input is focused again and the popup reopens (inferred re-click in the field). The pointer then moves to the '−' button and the popup is open. (00:08.0; 0008.0, 0009.5, 0010.0)
6. Click '−' (inferred). The popup fades out with a 'Left' tooltip and the map behind it changes to a different, zoomed-out view. The popup is closed by the next frame. (00:10.5; 0010.5, 0011.0)

Expected (implied): Clicking '+' or '−' zooms the map in or out and keeps the popup open, so the coordinate can be adjusted.

Actual: The click closes the coordinate popup. The '+' click shows no zoom at all, and the scale stays at 1 km. During the '−' click's fade-out (0010.5), the map shows a different zoomed-out view with the scale bar still at '1 km'. The popup is closed in the next frame.

Key events: 0004.5, 0005.0, 0010.5, 0011.0

Missed by the author:

- The map appears to start zooming out when '−' is clicked (0010.5), but the popup closes immediately after.
- The ticket gives no steps, browser, or exact expected behaviour.

Claims:

- "The zoom button interaction on the coordinate picker is broken." [Video of a bug with the user interaction on the Wikidata coordinate picker zoom button.]: confirmed - Clicking '+' and '−' closes the popup instead of zooming the map (0004.5 to 0006.0, 0010.5 to 0011.0).
