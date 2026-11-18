# real/commons-wikidata-coord-zoom

_claude-sonnet-5.5@default, 27 s; looked at: frames/0007.5.jpg, frames/0004.0.jpg_

In the Wikidata coordinate editor, clicking the map's +/− zoom buttons in the 'will be displayed as' popup closes the popup instead of zooming the map. It happened on '+' at about 4.3 s and again on '−' at about 10.7 s, so the zoom controls cannot be used while editing a coordinate.

## Coordinate picker popup closes and the map does not zoom when a zoom button is clicked

Class: **silent-fail**

Environment: Browser on a Wikidata item page for Palazzo Calepini (Trento). The 'coordinate location' statement (46°4'0.91"N, 11°7'20.78"E, reference 'stated in: OpenStreetMap') is in edit mode with the 'will be displayed as' map popup (Wikimedia maps, scale 1 km). No account, browser or version is visible. The video has no audio beyond 'Thank you.'.

Steps:

1. The statement is in edit mode. Click into the coordinate input, which opens the 'will be displayed as' popup with the map and the +/− buttons. The click on the input is inferred from the popup appearing. (00:02.0; p004, p005)
2. Hover the '+' zoom button (0.5 s), then click it. (00:04.3; p009, p010)
3. About 0.4 s after the click the popup and its map are gone. The scale stays at 1 km, and the statement is shown in edit mode without the popup. (00:04.7; p011, p012, p013, p014, p015, p016, p017)
4. Repeat: click into the input again to reopen the popup, move to the zoom buttons and click ('−' area). The first click (291,220) only changes an icon or colour and the popup stays open. The second click (288,210) closes the popup again. The map is not zoomed. The second click lands on a different spot, so it is unclear which button it hit. (00:10.2; p028, p029, p030, p031, p032, p033, p034, p035, p036)

Expected (implied): Clicking + or − zooms the map one level and the popup stays open, so the coordinate can be adjusted.

Actual: Clicking the zoom buttons closes the popup and no zoom is visible. In frame 0004.0 the cursor is on '+' with the popup open at 1 km. After the click the popup disappears, and frame 0005.0 shows it gone with the scale still 1 km. The second attempt ends the same way.

Key events: p010, p012, p013, p016, p031, p033, p036

Missed by the author:

- Between the two attempts the statement was left and re-entered, probably by cancel and edit: at 7.3–7.5 s it shows read-only with the cursor on the cancel position, and at 7.7 s it is back in edit mode (p021, p022, p024, p025). The video shows the author did this; it does not show why.
- A 'Left' tooltip flashed at 4.7 s and 7.5 s (p017, p023). It comes from the 'Left' tooltip on the cursor position and is not an error message.
- The second attempt has two clicks (p031, p033). The first changed an icon or colour with the popup still open. The popup closed only on the second click.

Claims:

- "The zoom button interaction on the coordinate picker is broken (ticket)." [ticket]: confirmed - Both clicks on the zoom controls (p010, p033) are followed within about 0.4 s by the popup disappearing (p012–p016, p034–p036), and no zoom is seen.
