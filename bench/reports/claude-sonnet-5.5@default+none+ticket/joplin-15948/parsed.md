# real/joplin-15948

_claude-sonnet-5.5@default, 14 s; looked at: nothing_

In Joplin desktop 3.7.9 on Linux, selecting several read-only notes (for example from a Joplin Cloud share) and clicking Delete removes them locally. After a sync they come back. Deleting read-only notes should not be possible at all, even temporarily, so the user sees a misleading deletion that later reverts.

## Multiple selected read-only notes can be deleted locally, then reappear after sync

Class: **state-revert**

Environment: Joplin desktop 3.7.9 (dev build, revision fd76c4052a, branch pr/desktop/ai-cancel-chat) on Linux; Markdown editor; sync target Joplin Cloud; notes from a Joplin Cloud share (read-only). Plugins: Backup 1.5.1, Freehand Drawing 4.3.0.

Steps:

1. Select multiple read-only notes (e.g. from a Joplin Cloud share). (00:00.0; )
2. Click "Delete". (00:00.0; )
3. Observe that the notes have been deleted. (00:00.0; )
4. Run a sync. (00:00.0; )
5. Observe that the notes have been recreated. (00:00.0; )

Expected (speech): Read-only notes cannot be deleted, even temporarily.

Actual: The read-only notes are deleted from the list after clicking Delete. After sync they are restored.

Key events: 

Claims:

- "Read-only notes disappear after Delete with multiple notes selected." [Observe that the notes have been deleted.]: not shown - No video; ticket text only.
- "Notes are recreated after sync." [Observe that the notes have been recreated.]: not shown - No video; ticket text only.
