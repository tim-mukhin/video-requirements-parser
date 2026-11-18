# real/zed-64366

_claude-sonnet-5.5@default, 16 s; looked at: nothing_

Right-clicking a file or folder near the bottom of Zed's Project Panel opens a context menu that extends past the bottom of the window, so lower items are clipped or hidden. This blocks use of those actions. VS Code repositions its menu to stay fully visible. The report comes from the ticket text alone, with no video.

## Project Panel context menu is clipped when opened near the bottom of the window

Class: **wrong-data**

Environment: Zed v1.20.2+stable.360.7c451e694f3c52ee0aeb01d7e28b5fa18cd0ad2f on Windows 10.0.26200 (x86_64, 13.7 GiB RAM, Intel Iris Xe Graphics). Clean configuration. The ticket mentions WSL/Ubuntu in a template question, but it is not stated that WSL was used. VS Code was used for comparison. Window size and the number of menu items are not given.

Steps:

1. Start Zed with a clean installation/configuration. (00:00.0; )
2. Open any project. (00:00.0; )
3. Open the Project Panel. (00:00.0; )
4. Make sure a file or folder is near the bottom of the visible Project Panel. (00:00.0; )
5. Right-click that file or folder. (00:00.0; )
6. Observe that the context menu extends past the bottom edge of the Zed window and the lower items are clipped. (00:00.0; )

Expected (speech): The context menu repositions itself, for example opening upward or shifting up, so the whole menu stays visible inside the Zed window, as VS Code does.

Actual: The context menu extends beyond the bottom edge of the window. Lower items are partially or completely clipped and cannot be viewed. No log output is produced.

Key events: 

Claims:

- "The issue also occurs with a clean Zed configuration." [This also occurs with a clean Zed configuration.]: not shown - No video was available. Only the ticket text supports this.
- "VS Code repositions its context menu when there is not enough space below." [VS Code repositions the context menu when there is not enough space below the selected item.]: not shown - The comparison recordings were not available.
