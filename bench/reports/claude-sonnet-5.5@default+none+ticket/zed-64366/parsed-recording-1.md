# real/zed-64366

_claude-sonnet-5.5@default, 16 s; looked at: nothing_

Right-clicking a file or folder near the bottom of Zed's Project Panel opens a context menu that extends past the bottom edge of the window, so lower items are clipped or hidden. It matters because those actions can't be reached or read. The report is based on the ticket text only; the recordings were not seen.

## Project Panel context menu is clipped when opened near the bottom of the window

Class: **wrong-data**

Environment: Zed v1.20.2+stable.360 (7c451e694f3c) on Windows 10.0.26200, x86_64, Intel Iris Xe GPU, 13.7 GiB RAM. Clean configuration, no custom settings or keymap. The ticket mentions WSL/Ubuntu, but it is unclear whether WSL was used. VS Code was used for comparison.

Steps:

1. Start Zed with a clean installation/configuration. (00:00.0; )
2. Open any project. (00:00.0; )
3. Open the Project Panel. (00:00.0; )
4. Make sure a file or folder is near the bottom of the visible Project Panel. (00:00.0; )
5. Right-click that file or folder. (00:00.0; )
6. Observe that the context menu extends beyond the bottom edge of the Zed window and some items are clipped. (00:00.0; )

Expected (speech): The context menu repositions itself (for example, opening upward) so the whole menu stays visible inside the Zed window, as VS Code does.

Actual: The context menu extends below the bottom edge of the window. Lower items are partially or completely clipped and can't be viewed properly.

Key events: 

Claims:

- "The issue also occurs with a clean Zed configuration." [This also occurs with a clean Zed configuration.]: not shown - No video was available to check this; it rests on the reporter's statement.
- "VS Code repositions its context menu when there is not enough space below." [VS Code repositions the context menu when there is not enough space below the selected item, keeping the complete menu visible.]: not shown - The comparison is in recording-2, which was not available.
- "No relevant log output is produced." [No relevant log output was produced when reproducing this issue.]: not shown - No log was attached.
