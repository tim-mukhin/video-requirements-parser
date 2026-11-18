# real/commons-t146747-scroll

_claude-sonnet-5.5@default, 14 s; looked at: nothing_

In the Wikipedia Android app, opening a wikilink after scrolling down a page loads the new page at a scroll position tied to the previous page, not at the top. This disorients readers, who must scroll back up to read the new article from the start. The report comes from the ticket text alone, with no video.

## New page opened via wikilink keeps scroll position from previous page

Class: **wrong-data**

Environment: Wikipedia Android app 2.3.152-r-2016-08-18, Android 6.0 (Marshmallow), LG G4 H815, device language German. The ticket does not name the article or wiki, and gives no account or organization.

Steps:

1. Open a page in the app. (00:00.0; )
2. Scroll down the page. (00:00.0; )
3. Tap a wikilink to open another page. (00:00.0; )

Expected (speech): The new page opens at the top.

Actual: The new page opens partway down, at a position that seems related to the scroll position on the previous page.

Key events: 

Claims:

- "The new page opens at a position related to the previous page's scroll status." [New page opens somewhere in the page, somehow related to scroll status on the former page]: not shown - There is no video or log to check this. The reporter's own wording is vague: 'somewhere' and 'somehow related'.
