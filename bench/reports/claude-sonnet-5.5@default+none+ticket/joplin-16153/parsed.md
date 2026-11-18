# real/joplin-16153

_claude-sonnet-5.5@default, 14 s; looked at: nothing_

In Joplin Server shared folders, a user cannot unpublish a note that the other user published. This looks like a regression, possibly from PR #15276. It matters because a share owner cannot unpublish notes a removed recipient published.

## Cannot unpublish a note published by the other user in a shared folder

Class: **wrong-data**

Environment: Joplin 3.7.10 on Linux, desktop version info not given. Joplin Server with two users sharing a folder. The sync fuzzer was run with 2 clients.

Steps:

1. Share a folder with another user and accept the share. (00:00.0; )
2. As either user, publish a note in the shared folder. (00:00.0; )
3. As the other user, sync and try to unpublish the note. This is not possible. (00:00.0; )

Expected (speech): The share owner can unpublish any published note in a shared folder. This includes notes published by a user who has since been removed from the share.

Actual: The other user cannot unpublish the note. Clicking 'copy sharable link' on a note published by another user no longer offers unpublishing. Before PR #15276 it did. The sync fuzzer scenario fails on 2c11cbbb but passes on fca026f0.

Key events: 

Claims:

- "This is a regression, probably from PR #15276." [Since the sync fuzzer failure is new, this seems to be a regression. Could this be related to #15276?]: not shown - The reporter's tests show the fuzzer passes on fca026f0 and fails on 2c11cbbb. The ticket does not say that 2c11cbbb is the commit that merged #15276. The reporter also says the older build only partly reproduces the issue.
- **R1** [stated] The share owner must be able to unpublish any published note in a shared folder, including notes published by a removed share member. (proposed by personalizedrefrigerator) - ticket: Expected behaviour
