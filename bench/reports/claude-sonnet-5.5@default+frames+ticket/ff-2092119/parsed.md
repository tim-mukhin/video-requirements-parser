# real/ff-2092119

_claude-sonnet-5.5@default, 28 s; looked at: frames/0000.0.jpg, frames/0003.0.jpg, frames/0006.0.jpg, frames/0009.0.jpg, frames/0012.0.jpg, frames/0015.0.jpg, frames/0018.0.jpg, frames/0021.0.jpg, frames/0004.5.jpg, frames/0007.5.jpg, frames/0014.0.jpg_

The user picks a region of a page for a Firefox Mini Window (Beta), but the mini window shows the top of the page (the Wikipedia header and search box) instead of the selected region. The same happens on monkeytype.com, where the mini window is mostly blank. A video caption reads "doesnt show cropped selection. shows other part of webpage".

## Mini Window 'Move selection' shows the top of the page, not the cropped region

Class: **wrong-data**

Environment: Firefox (Windows, dark theme) with Mini Window (Beta). Pages: en.wikipedia.org/wiki/Quadrature_amplitude_modulation and monkeytype.com. The video was recorded at 1920x1080 and the frames show Windows 11. No account is shown.

Steps:

1. Open the Wikipedia article and start the Mini Window feature (inferred from the toolbar button at top right and the 'Choose what to move to a Mini Window' panel). 'Move selection' is highlighted. (00:03.0; 0003.0)
2. Drag a region over two paragraphs, 948x156 px (inferred), and click 'Move to Mini Window'. (00:04.5; 0004.5)
3. The original tab turns into a New Tab and a small mini window appears. It shows the Wikipedia header, search box and the start of the title, not the selected paragraphs. (00:09.0; 0006.0, 0009.0)
4. On monkeytype.com, right-click and choose 'Move Section to Mini Window (Beta)' (context menu visible). (00:12.0; 0012.0)
5. The 'Move selection' prompt shows. Drag a large region over the text area (1,280x428 px) and click 'Move to Mini Window'. (00:15.0; 0014.0, 0015.0)
6. The mini window at the bottom of the screen is almost blank and dark. It does not show the selected typing text. (00:18.0; 0018.0, 0021.0)

Expected (implied): The mini window shows only the selected region (the two paragraphs on Wikipedia, the word area on monkeytype) and nothing else.

Actual: The mini window shows another part of the page: the top of the Wikipedia article on the first attempt, and a blank dark area on monkeytype. The ticket says the whole page can be scrolled. The video does not show scrolling, but a small scrollbar mark is visible at the mini window's right edge.

Key events: 0004.5, 0009.0, 0018.0

Missed by the author:

- On monkeytype the mini window is blank and dark, not showing the page header or any text (0018.0, 0021.0). The ticket describes it as the entire page.
- On both attempts the original tab is replaced by a New Tab once the content moves to the mini window (0006.0, 0009.0, 0018.0).

Claims:

- "Selecting a region creates a mini window with the entire page, which can be scrolled." [instantiates a miniwindow containing the entire page, which can be scrolled up and down]: not shown - The mini window shows the top of the page and a scrollbar mark at its edge, but no scrolling is shown. It is not clear that it holds the whole page.
- "The steps are: right-click, select the mini window option, select a region, then click send." [select miniwindow option in right click menu... click send to miniwindow]: confirmed - The right-click menu is visible on monkeytype at 0012.0 and the 'Move to Mini Window' button at 0004.5 and 0015.0. The Wikipedia start looks like it came from the toolbar button, not a right-click.
- "The ticket's 'Expected' and 'Actual' headings are swapped." [Expected behaviour... Actual behaviour]: confirmed - The ticket's Expected text describes the correct behaviour and its Actual text describes the bug, but each sits under the opposite heading.
