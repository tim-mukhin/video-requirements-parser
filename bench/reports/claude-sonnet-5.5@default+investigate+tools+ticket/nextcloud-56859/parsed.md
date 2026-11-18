# real/nextcloud-56859

_claude-sonnet-5.5@default, 17 s; looked at: nothing_

In Nextcloud Files on demo1.nextcloud.com, searching 'ne' in the folder returns 4 files. Clicking 'Search everywhere' navigates to /apps/files/search?query=ne and shows 'No search results for "ne"'. Adding a third character ('nex') returns 7 files, so a 2-character term gives a misleading empty page with no explanation.

## 'Search everywhere' with a 2-character term shows 'No search results' instead of results or an explanation

Class: **wrong-data**

Environment: Nextcloud demo site (demo1.nextcloud.com), Files app, guest user, Chromium-style browser with a Settings tab open. No server version visible.

Steps:

1. In Files > All files, type 'ne' in the 'Search here...' box. The list filters to '4 files · 6 hidden' and a 'Search everywhere' button appears. The URL is still /apps/files/files. The typing itself is not seen, since the cursor is not followed before 2.7 s. (00:01.5; p003, p023, p024)
2. Click 'Search everywhere'. The URL becomes /apps/files/search?query=ne. (00:03.9; p033, p037)
3. The page shows 'No search results for "ne"' with the query 'ne' in the field. There is no hint that the term is too short. (00:04.6; p038, p039, p040)
4. Click the search field and add a character, making the query 'nex'. The page now lists 7 files (Nextcloud.png, community.jpg, flyer.pdf, intro.mp4, Manual.pdf, and others). (00:06.7; p043, p046, p047, p054)

Expected (implied): 'Search everywhere' for 'ne' should return the same or more results than the folder search, or explain that the term is too short, or not be offered for such a term.

Actual: The folder search found 4 files for 'ne'. 'Search everywhere' with the same term shows an empty 'No search results' state with no explanation. 'nex' works.

Key events: p023, p033, p037, p039, p054

Missed by the author:

- The empty page says 'No search results', which is misleading because the term is probably rejected rather than searched (p039).
- A blank spinner state lasts about 1.5 s before the empty state (p034, p037).

Claims:

- "Searching 'ne' gives results" [ticket]: confirmed - p023 shows '4 files · 6 hidden'.
- "'Search everywhere' then shows a 'no result' screen" [ticket]: confirmed - p039 shows 'No search results for "ne"'.
- "More characters make the result behave normally" [ticket]: confirmed - p054 lists 7 files for 'nex'.
- "The search page has a 3-character minimum" [ticket]: not shown - The video shows that 2 characters fail and 3 work. It does not show the reason.
- "Any 2-character query never returns a result" [ticket]: not shown - Only 'ne' is tried.
