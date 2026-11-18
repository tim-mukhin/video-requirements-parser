# real/ff-2092119

_claude-sonnet-5.5@default, 27 s; looked at: frames/0009.0.jpg, frames/0020.0.jpg_

In Firefox's Mini Window (Beta) feature, 'Move selection' crops a region of the page. The resulting mini window does not show that region. On Wikipedia it shows the top of the page (header and search box). On monkeytype it is a dark, mostly empty window. The cropped-region feature is therefore not working as intended.

## Mini Window 'Move selection' shows the wrong part of the page (page top / blank) instead of the selected region

Class: **wrong-data**

Environment: Firefox (Windows, dark theme, 1920x1080 recording) with Mini Window (Beta). Pages: en.wikipedia.org/wiki/Quadrature_amplitude_modulation and monkeytype.com. A Zotero Connector context-menu entry is visible. No account is shown. The ticket's user agent is Firefox 160 on Windows 10, but the video shows Windows 11 window chrome. Speech: one utterance, 'Thank you.'

Steps:

1. On the Wikipedia article, right-click and choose 'Move Section to Mini Window (Beta)'. The context menu flashes at 1.6 s. The click itself is not tracked. (00:01.6; p005, p030)
2. The 'Choose what to move to a Mini Window' panel appears with 'Move selection' / 'Move full tab'. (00:02.6; p031, p032)
3. Drag a region over two paragraphs. The selection reads 948 x 156. The 'Move to Mini Window' button is shown. The drag is not tracked. (00:04.2; p046, p050)
4. Click 'Move to Mini Window' (inferred from the screen reacting). The selection and overlay disappear. (00:05.9; p055, p058, p059)
5. The original tab becomes 'New Tab'. A small mini window appears at the bottom with en.wikipedia.org in its address bar. It shows the Wikipedia logo, search box and the start of the title 'Quadrature amplitude modulation', not the selected paragraphs. A caption 'doesnt show cropped selection. shows other part of webpage' overlays the video. (00:08.5; p065, p066, p067, p074, p076)
6. Repeat on monkeytype.com: right-click, then 'Move Section to Mini Window (Beta)'. The menu is visible at 11.9 s. (00:11.9; p089, p092)
7. The 'Move selection' prompt shows. A region is selected, first 1,280 x 428, then resized to about 1,280 x 146/158. The click on 'Move to Mini Window' is not tracked. (00:14.6; p093, p102, p108, p110, p114)
8. The monkeytype tab becomes 'New Tab' and the page flickers 5 times in 0.57 s. The mini window at the bottom is dark and nearly empty, with no typing text. A later frame shows monkeytype.com in its address bar. (00:17.6; p116, p125, p127, p144)

Expected (implied): The mini window contains only the selected region of the page and nothing else.

Actual: On Wikipedia the mini window shows the page top (header and search) instead of the selected paragraphs. On monkeytype it shows a dark, blank area. The source tab is replaced by a New Tab each time.

Key events: p050, p065, p074, p076, p116, p125, p144

Missed by the author:

- On monkeytype the mini window is blank and dark rather than showing the whole page (frames 0018-0021; p127-p137). That differs from the ticket's 'entire page' description.
- The monkeytype page flickered 5 times in 0.57 s as it became a New Tab (p125).
- The selection on monkeytype was resized from 1,280 x 428 to about 1,280 x 146/158 before sending (p102, p108, p110). So the sent region was a thin strip.
- The source tab is replaced by a New Tab in both attempts (p065, p116). Whether this is intended is not stated.

Claims:

- "Selecting a region creates a mini window containing the entire page, which can be scrolled up and down." [ticket]: not shown - The video shows no scrolling. A mini window showing the page top is consistent with a whole-page view, but a small scrollbar mark at the mini window's edge in the monkeytype frame is the only hint. The monkeytype mini window shows no page content at all.
- "The mini window shows the selected region and nothing else (ticket's Expected)." [ticket]: refuted - The mini window shows the page top on Wikipedia (frame 0009.0) and a blank dark window on monkeytype (frame 0020.0).
- "Steps: right-click menu, miniwindow option, select region, send." [ticket]: confirmed - The context menu entry flashes on both pages (p005, p089) and the 'Move to Mini Window' button is shown (p046, p114). The clicks themselves are not tracked.
- "The ticket's Expected and Actual headings are swapped." [ticket]: confirmed - The text under 'Actual results' describes the intended behaviour and the text under 'Expected results' describes the bug.
