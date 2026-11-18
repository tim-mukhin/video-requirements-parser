# real/nextcloud-56859

_claude-sonnet-5.5@default, 19 s; looked at: frames/000139.jpg, frames/000233.jpg, frames/000047.jpg_

In Nextcloud Files, the filter "ne" matches four files in the current folder. After the author clicks "Search everywhere", the global search page says "No search results for 'ne'", even though the same query had just matched files. Retyping as "nex" eventually lists results, so the first global search is wrong or incomplete.

## "Search everywhere" returns no results for a query that matches files in the local filter

Class: **wrong-data**

Environment: Nextcloud Files at demo1.nextcloud.com in a browser with two tabs (Files and Settings), user avatar "L". The window shows "Guest" at the top right, which looks like the browser profile label.

Steps:

1. In Files > All files, type "ne" in the search box. The local filter shows 4 matching files (Nextcloud.png, Nextcloud intro.mp4, Nextcloud Manual.pdf, Reasons to use Nextcloud.pdf), "4 files · 6 hidden". A "Search everywhere" button appears. (00:01.5; p022, p030)
2. Click "Search everywhere". (00:03.9; p032)
3. The page changes to /apps/files/search?query=ne and shows "No search results for 'ne'". (00:04.6; p036, p037, p038)
4. Click the "Search for files" field and retype. The query becomes "nex", a loading spinner shows, and the results list appears. The last step (typing and the spinner) is read from frames, not from the timeline's click events. (00:06.7; p042, p045, p046, p053)

Expected (implied): Search everywhere for "ne" should return at least the files the local filter already matched.

Actual: The global search shows an empty-state "No search results for 'ne'". Retyping "nex" shows a spinner, then a file list.

Key events: p022, p032, p038, p046, p053

Missed by the author:

- The local filter showed 4 matching files for "ne" just before the click, so "no results" contradicts it (p022).
- The author said nothing useful. The only speech is "Thank you." (u001), so no claim or explanation is given.
- The first 2.7 s and 1 s around 6.7 s have no cursor tracking, so the typing and some clicks are not visible; the cursor-less parts are inferred from the screen changes.
