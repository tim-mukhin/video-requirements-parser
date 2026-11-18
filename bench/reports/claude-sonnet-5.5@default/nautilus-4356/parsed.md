# real/nautilus-4356

_claude-sonnet-5.5@default, 19 s; looked at: frames/000013.jpg, frames/000018.jpg, frames/000036.jpg_

In Nautilus, a Rename File dialog is open for file.txt. A text-field context menu then opens, and its upper part (Paste and probably Cut/Copy) is hidden behind the dialog. The menu also drifts a few pixels and an item highlight appears without any visible cursor. The recording is silent and shows no cursor.

## Context menu of the Rename File entry is drawn partly behind the rename popover, hiding its top items

Class: **wrong-data**

Environment: Nautilus (GNOME Files), folder Home / Downloads / temp, file.txt selected, Rename File popover open. Single window; no accounts or organizations seen.

Steps:

1. In Home/Downloads/temp, start renaming file.txt. The Rename File popover opens with 'file' selected. The trigger is not visible. (00:00.9; p001, p002, p003)
2. A context menu (Delete, Select All, Change direction, Insert Emoji) opens below the entry. Its top is covered by the popover. The trigger is not visible, most likely a right-click in the text field. (00:02.0; p004)
3. The menu shifts about 2 px and re-renders. Only a fragment of 'Paste' shows above 'Delete', and the rest of the top is clipped by the popover. (00:02.8; p005, p006, p007, p009, p012)
4. The 'Delete' row is highlighted and the menu shifts again, still clipped at the top. (00:06.0; p014, p016, p017)

Expected (implied): The context menu is fully visible above the dialog, with all its entries (Cut/Copy/Paste, etc.) readable and stable.

Actual: The menu's top entries are cut off by the Rename File popover (only a sliver of 'Paste' is visible). The menu changes position and size between frames, and the screen shows no explanation for it.

Key events: p004, p005, p014, p016

Missed by the author:

- No narration exists. The menu is visibly clipped by the popover in frames/000013.jpg, frames/000018.jpg and frames/000036.jpg.
- The 'Delete' item is highlighted at 00:06 (p016) although no cursor is visible in the video.
