# real/nextcloud-56859

_gpt-6-sol@default, 32 s; looked at: frames/moments/p004.jpg, frames/moments/p018.jpg, frames/moments/p032.jpg, frames/moments/p034.jpg, frames/moments/p051.jpg, frames/0002.0.jpg, frames/0005.0.jpg, frames/0007.5.jpg, frames/000244.jpg, frames/000082.jpg, frames/000047.jpg, frames/000233.jpg_

In Nextcloud Files, filtering All files for “ne” shows four files, but Search everywhere opens a page that says there are no results for the same query. Changing the query to “nex” returns seven files, making the two-character no-results message misleading.

## Search everywhere reports no results for “ne” despite visible file matches

Class: **wrong-data**

Environment: Nextcloud Files on demo1.nextcloud.com in a browser with a Guest profile; Nextcloud version not visible.

Steps:

1. In All files, enter “ne” in the left search field; the filtered list shows four files. (00:01.5; p031, p023)
2. Click Search everywhere. (00:03.9; p033, p037)

Expected (implied): Show matches for “ne”, or explain why this query cannot be searched.

Actual: At /apps/files/search?query=ne, the page says “No search results for ‘ne’” [p037, p039]. After the query is changed to “nex”, it shows seven files [p047, p054].

Key events: p023, p033, p037, p039, p047, p054

Missed by the author:

- The first four matches belong to the All files filter, which also says “6 hidden”; they are not results on the Search everywhere page [p023, p032]. The watcher’s interpretation of that screen is supported by the frame.
- The brief count changes and upward list movement around 00:01.2–00:01.5 are the All files list settling into its four-file filtered state, not a separate failure [p004, p018, p023]. The moment frames settle this short-lived change.
- The search page offers a separate central “Search for files” field; changing its query to “nex” briefly replaces the no-results state with a loading indicator before seven results appear [p040, p047, p051, p054]. The moment frame resolves the brief transition.

Claims:

- "“ne” finds files in All files but Search everywhere shows no results." [ticket: Bug description, steps 1–2]: confirmed - The filtered list shows four files [p023]; the search page for the same query shows a no-results message [p037, p039].
- "Adding another character makes results appear." [ticket: Bug description, step 3]: confirmed - The query changes to “nex” [p047], and seven files appear at 00:08.1 [p054], not at 00:07.5 as the watcher notes.
- "All queries shorter than three characters fail, including direct visits to the search URL." [ticket: Bug description and Steps to reproduce]: not shown - The video shows one two-character query reached via Search everywhere, not other short queries or direct URL entry.
- "The issue affects CJK searches and reflects a three-character limit." [ticket: Additional info]: not shown - Only Latin-letter queries are tested; the video does not establish a limit or its cause.
