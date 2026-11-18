# real/nautilus-4374

_claude-sonnet-5.5@default, 15 s; looked at: nothing_

In Nautilus 51.1, typing a `/` in the rename popover shows the warning "File / Folder names cannot contain `/`". If the popover is closed with Escape or a click outside, the warning is still shown the next time rename is opened, on any file or folder, even when the name has no `/`. This misleads users into thinking the new name is invalid. It happens only in the same window or tab.

## Rename warning about `/` persists after rename popover is closed and reopened

Class: **state-revert**

Environment: Nautilus 51.1 on Bazzite 51. The ticket does not say whether the development version is also affected (the field was left as "Yes / No"). No account or organization applies.

Steps:

1. Open the rename popover on a file or folder. (00:00.0; )
2. Type a `/` character in the name. The warning "File / Folder names cannot contain `/`" appears. (00:00.0; )
3. Close the rename popover by pressing Escape or clicking outside it. (00:00.0; )
4. Open the rename popover again on any file or folder, in the same window or tab. (00:00.0; )

Expected (speech): The warning does not carry over into a new rename session. It appears only while the name contains `/`.

Actual: The warning is already visible when rename is reopened, even though the name has no `/`. It happens only in the same window or tab.

Key events: 

Claims:

- "The warning persists into a new rename session in the same window or tab." [the warning persists into a new rename operation (in the same window / tab only)]: not shown - No video was available. The claim comes from the ticket text only.
