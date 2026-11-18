# real/ff-2092119

_claude-sonnet-5.5@default, 15 s; looked at: nothing_

In Firefox 160 on Windows, the right-click "miniwindow" option lets the user crop a region of a page. Sending the crop opens a miniwindow with the entire page, scrollable, instead of only the selected region. The crop feature doesn't do what it promises. The ticket has no video, so only the written text was used.

## Mini-window crop sends the entire page instead of the selected region

Class: **wrong-data**

Environment: Firefox 160.0 on Windows 10/11 (Win64). Pages named: en.wikipedia.org, monkeytype.com, though the reporter says any page. No accounts or organizations are mentioned.

Steps:

1. Open a webpage, e.g. en.wikipedia.org or monkeytype.com. (00:00.0; )
2. Right-click and select the miniwindow option in the context menu. (00:00.0; )
3. In crop mode, select a region of the webpage. (00:00.0; )
4. Click "send to miniwindow". (00:00.0; )

Expected (speech): A miniwindow opens containing only the selected region of the page and nothing else.

Actual: The miniwindow contains the entire page, which can be scrolled up and down, instead of only the cropped region.

Key events: 

Claims:

- "The miniwindow contains the whole scrollable page rather than the cropped region." [selection a region of the webpage instantiates a miniwindow containing the entire page, which can be scrolled up and down]: not shown - No video is available. The claim comes from the ticket text only and could not be checked.
