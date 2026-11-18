# real/nextcloud-56859

_claude-sonnet-5.5@default, 18 s; looked at: nothing_

In Nextcloud Files, clicking "Search everywhere" after a short search (under 3 characters, e.g. "ne") opens /apps/files/search?query=ne and shows a "no result" screen. The in-folder search had returned results, so the user is confused and expects more results, not fewer. The result list is replaced with nothing and no error or hint appears.

## "Search everywhere" shows no results instead of feedback when the search term is shorter than 3 characters

Class: **silent-fail**

Environment: Nextcloud demo site (exact version, browser and account not stated). Files app, route /apps/files/search. Reporter says the issue was found while working with CJK characters.

Steps:

1. In the Nextcloud Files app, search for a short term such as "ne" (2 characters). Results appear. (00:00.0; )
2. Click "Search everywhere". (00:00.0; )
3. Observe the page /apps/files/search?query=ne. It shows a "no result" screen, and the earlier results are gone. (00:00.0; )
4. Alternatively, open /apps/files/search?query=xx directly. It never returns a result, whatever the query. (00:00.0; )
5. Enter more characters (3 or more). Results display normally. (00:00.0; )

Expected (implied): Unclear; the reporter is unsure. Options: search anyway for 2 characters, show a clear message about the minimum length, or hide the "Search everywhere" button when the term is too short. At minimum, the user should not see a misleading empty "no result" state.

Actual: With a term under 3 characters, the search-everywhere page shows an empty "no result" state with no error or explanation, and the previous results are erased.

Key events: 

Claims:

- "Search everywhere returns nothing for terms shorter than 3 characters, whatever the query." [it will never return a result no matter what the query is]: not shown - No video or event data; the claim comes from the ticket text only.
- "The in-folder search for "ne" returned results before "Search everywhere" was clicked." [User searched for "ne" => got result => good]: not shown - The recording is not available.
- "Terms of 3 or more characters work normally." [User enter more chars and the result behave normally]: not shown - The recording is not available.
- **R1** [proposed] Show helpful feedback instead of a misleading "no result" screen when the search term is too short. (proposed by Summon528) - ticket: Expected behavior
- **R2** [proposed] Allow 2-character searches on the "Search everywhere" page, consistent with the earlier reduction of the search limit to 2 characters (PR #21777). (proposed by Summon528) - ticket: Reporter's follow-ups
- **R3** [proposed] Hide the "Search everywhere" button when the search term is 1 character. (proposed by Summon528) - ticket: Reporter's follow-ups
- **R4** [open_question] Why does the search-everywhere page enforce a 3-character minimum when other search allows 2? This matters for CJK languages. (proposed by Summon528) - ticket: Additional info
