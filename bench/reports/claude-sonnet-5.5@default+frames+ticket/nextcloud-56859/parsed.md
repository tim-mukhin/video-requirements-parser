# real/nextcloud-56859

_claude-sonnet-5.5@default, 26 s; looked at: frames, frames/0000.0.jpg, frames/0002.0.jpg, frames/0004.0.jpg, frames/0006.0.jpg, frames/0008.0.jpg, frames/0009.5.jpg, frames/0003.0.jpg, frames/0004.5.jpg, frames/0007.0.jpg_

In the Nextcloud Files app, a 2-character search ("ne") shows 4 results in the current folder. Clicking "Search everywhere" replaces them with "No search results for 'ne'". Typing a third character ("nex") then returns 7 files across the account.

## "Search everywhere" with a 2-character term shows "No search results" and discards the existing results

Class: **wrong-data**

Environment: Nextcloud demo site (demo1.nextcloud.com), Files app, in a Chromium-based browser (Edge-like UI) as a guest/demo user. Grid view is toggled off. The second tab is Settings. No server version is shown.

Steps:

1. Open Files > All files and click the "Search here..." box in the sidebar (the box is focused). (00:00.0; 0000.0)
2. Type "ne" (inferred from the box contents). The list filters to 4 files ("4 files · 6 hidden") and a "Search everywhere" button appears. The URL is still /apps/files/files. (00:02.0; 0002.0, 0003.0)
3. Click "Search everywhere" (inferred: the click itself is not visible, but the next frames show a spinner and the URL changing to /apps/files/search?query=ne). (00:04.0; 0004.0, 0004.5)
4. The result list is empty and then replaced by the empty state "No search results for 'ne'". (00:06.0; 0006.0, 0007.0)
5. Click into the "Search for files" field and add a character, making the query "nex". A spinner is shown first, then 7 files are listed across the account, including Nextcloud community.jpg, Nextcloud flyer.pdf and Welcome to Nextcloud Hub.docx. (00:08.0; 0008.0, 0009.5)

Expected (implied): "Search everywhere" with "ne" should return the same or more results than the folder-scoped search. Failing that, it should explain that the term is too short, or the button should not be offered for terms the global search rejects.

Actual: "Search everywhere" with "ne" shows "No search results for 'ne'" with no explanation, even though the folder search had just found 4 matches. A third character makes the same page return results.

Key events: 0003.0, 0004.5, 0006.0, 0009.5

Missed by the author:

- The empty state wording "No search results for 'ne'" is misleading, because the term is rejected rather than searched (0006.0).
- Selecting "Search everywhere" removes the Search everywhere button and the "People" filter chip, and the page header changes from "All files" to "Search" (0006.0).
- A blank list with only a spinner appears for about 1–2 s before the empty state (0004.5, 0005.0).

Claims:

- "Searching "ne" gives results." [User searched for "ne" => got result]: confirmed - 0003.0 shows 4 files for "ne".
- "Clicking "Search everywhere" shows a "no result" screen." [saw a "no result" screen]: confirmed - 0006.0 and 0007.0 show "No search results for 'ne'".
- "Entering more characters makes the search work normally." [User enter more chars and the result behave normally]: confirmed - 0009.5 shows 7 results for "nex".
- "The cause is a 3-character minimum on the search page." [the search everywhere page ... 3-char limit]: not shown - The video shows only that 2 characters fail and 3 work. It does not show why.
- "A URL with any 2-character query never returns a result." [observe that it will never return a result no matter what the query is]: not shown - Only the query "ne" is tried.
