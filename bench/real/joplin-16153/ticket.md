# Joplin Server sharing: No longer possible to unpublish a note published by a share recipient

Source: https://github.com/laurent22/joplin/issues/16153  (reporter: personalizedrefrigerator, filed 2026-08-05)

### Operating system

Linux

### Joplin version

3.7.10

### Desktop version info

_No response_

### Current behaviour

To reproduce:
1. Share a folder with another user. Accept the share.
2. From *either* user: Publish a note in the shared folder.
3. From the other user: Attempt to unpublish the note. Observe that this isn't possible.

Screen recording:

[attachment: recording.mp4]

**Sync fuzzer**: The issue can also be reproduced using the following sync fuzzer config (see `yarn syncFuzzer start --help`):
```json
{
	"clientCount": 2,
	"actions": [
		["switchClient", { "id": 0 }],
		"sync",

		["switchClient", { "id": 1 }],
		["newToplevelFolder", { "id": "11111111111111111111111111111112" }],
		"shareFolder",
		["newNote", { "id": "11111111111111111111111111111113", "parentId": "11111111111111111111111111111112" }],
		["publishNote", { "id": "11111111111111111111111111111113" }],
		"syncAndCheckState",

		"// Unpublish from the share recipient",
		["switchClient", { "id": 0 }],
		"sync",
		["unpublishNote", { "id": "11111111111111111111111111111113" }],
		"syncAndCheckState",

		["switchClient", { "id": 1 }],
		"syncAndCheckState"
	]
}
```

### Expected behaviour

- It should be possible for the share owner to unpublish any published note within a shared folder. In particular, after a user has been removed from a share, it should be possible for the share owner to unpublish notes that were published by that user.

### Logs

_No response_

## Reporter's follow-ups

Since the sync fuzzer failure is new, this seems to be a regression. @Rygaa could this be related to https://github.com/laurent22/joplin/pull/15276?

**Update**:
- I've re-tested with a version of Joplin (and Joplin Server) just prior to #15276 and I can partially reproduce the issue. Previously, clicking "copy sharable link" on a note published by another user allowed the share owner to unpublish it. With the latest dev, clicking "copy sharable link" does not allow unpublishing the note.
- The sync fuzzer successfully runs with the above test config on fca026f0d9934629c6db02713664f4d894b85110, but fails on 2c11cbbb6bdae7ae2073b01a1ea646940c883131.
