# real/excalidraw-11376

_claude-sonnet-5.5@default, 15 s; looked at: nothing_

In the Excalidraw macOS desktop app, the New Folder dialog keeps the name of the last created folder instead of resetting. Each new folder requires the user to delete the old text first. This is minor, but it adds repeated friction when organizing many folders. The report comes from the ticket text only; the recording was not available.

## New Folder input is prefilled with the previously created folder name

Class: **state-revert**

Environment: Excalidraw desktop app for macOS, version 1.7.3 (59), installed from the desktop download (not the web version). The macOS version and the account or workspace used are not given.

Steps:

1. Open the Excalidraw desktop application. (00:00.0; )
2. Click the New Folder button. (00:00.0; )
3. Type a name (e.g. Try1) and confirm to create the folder. (00:00.0; )
4. Click the New Folder button again. (00:00.0; )

Expected (speech): The input field is empty, or shows a placeholder such as 'Untitled Folder', ready for a fresh name.

Actual: The input field is prefilled with the last created folder's name (e.g. Try1). The user has to backspace or select all and delete it before typing a new name.

Key events: 

Claims:

- "The New Folder dialog does not reset its state after a folder is created." [the "New Folder" dialog does not clear its state after a folder is created]: not shown - Ticket text only, no video. It is a plausible reading of the described behavior but was not observed.
- "The prefill appears on the second opening of the dialog and repeats for every later folder." [The input field is prefilled with the string from the last created folder]: not shown - No recording was available to check this.
- **R1** [stated] The New Folder dialog input must be empty, or show a default placeholder such as 'Untitled Folder', each time it opens after a folder was created. - ticket.md: Expected Behavior
- **R2** [open_question] Unclear: should the field be empty or show a default name? Should a default name be pre-selected so typing replaces it? The reporter offers both options. - ticket.md: Expected Behavior
