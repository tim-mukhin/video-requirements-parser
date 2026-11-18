# real/ff-2092119

_claude-sonnet-5.5@default, 23 s; looked at: frames/000198.jpg, frames/000129.jpg_

In Firefox, the author uses the beta "Move Section to Mini Window" feature on a Wikipedia page and selects a 948×156 area. The Mini Window that opens shows the top of the page (Wikipedia header and search box), not the selected paragraph. The same happens on monkeytype.com, so the feature does not honour the selected region.

## Firefox "Move Section to Mini Window" shows the top of the page instead of the selected area

Class: **wrong-data**

Environment: Firefox (new UI) on a 1920×1080 screen. Pages: en.wikipedia.org/wiki/Quadrature_amplitude_modulation and monkeytype.com. Context menu entry "Move Section to Mini Window Beta". The video shows no accounts or organizations.

Steps:

1. Open the page context menu; it lists "Move Section to Mini Window Beta" (the trigger is not visible). (00:01.6; p005)
2. The "Choose what to move to a Mini Window" chooser opens (the choice is not visible). It offers "Move selection" and "Move full tab", and the selection mode follows. (00:02.6; p031, p032)
3. Drag out a selection of the paragraph "The two carrier waves…" (948 × 156). The frame shows the Move to Mini Window button. (00:04.2; p043, p045, p046, p050)
4. Confirm with "Move to Mini Window" (the click is not visible). The original tab turns into a New Tab and a Mini Window appears at the bottom right. (00:05.9; p056, p065, p066)
5. The Mini Window shows the Wikipedia header, search box and the title "Quadrature amplitude modulation", not the selected paragraph. The author overlays the note "doesnt show cropped selection. shows other part of webpage". (00:06.5; p067, p068, p072, p073)
6. Repeat on monkeytype.com with a 1,280 × 428 selection (later 1,280 × 146, then 1,280 × 158). It ends again with a New Tab and the same note. (00:12.7; p092, p101, p107, p109, p124, p127, p128)

Expected (speech): The Mini Window shows exactly the area that was selected.

Actual: The Mini Window shows another part of the page, the top (header and search), instead of the cropped selection. This repeats on a second site.

Key events: p043, p045, p050, p065, p067, p068, p073, p092, p101, p127, p128

Missed by the author:

- The Wikipedia page flickers when the menu opens: text blocks flash and are replaced by menu items, and "View Page Source" briefly becomes "View Page Scarce" (p005, p013, p015).
- In the selection overlay the page text is garbled by OCR with fragments like "move to a Mini Window. It'll stay on top while you browse" mixed into the page text (p039, p040). This is a rendering artifact.

Claims:

- "The Mini Window does not show the cropped selection; it shows another part of the webpage." [on-screen note (p067/p068)]: confirmed - Frame 000198 shows the Wikipedia header and search box in the Mini Window, while the selection was the 'two carrier waves' paragraph in frame 000129.
