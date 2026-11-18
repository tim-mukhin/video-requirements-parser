# Project Panel context menu is clipped when opened near the bottom of the window

Source: https://github.com/zed-industries/zed/issues/64366  (reporter: Valley-15, filed 2026-09-17)

### Reproduction steps

1. Start Zed with a clean installation/configuration.
2. Open any project.
3. Open the Project Panel.
4. Make sure there is a file or folder near the bottom of the visible Project Panel.
5. Right-click the file or folder.
6. Observe the context menu.
7. The context menu extends beyond the bottom edge of the Zed window, causing some menu items to be clipped and not fully visible.

### Current vs. Expected behavior

**Current behavior:**

When right-clicking a file or folder near the bottom of the Project Panel, the context menu can extend beyond the bottom edge of the Zed window. As a result, the lower menu items are partially or completely clipped and cannot be properly viewed.

This also occurs with a clean Zed configuration.

**Expected behavior:**

The context menu should automatically reposition itself so that the entire menu remains visible within the Zed window, even when the selected file or folder is near the bottom of the Project Panel.

For comparison, VS Code repositions the context menu when there is not enough space below the selected item, keeping the complete menu visible.

**Screenshots / screen recordings:**

A screen recording comparing the behavior in Zed and VS Code is attached.

[attachment: recording-1.mp4]
[attachment: recording-2.mp4]

### Zed version and system specs

Zed: v1.20.2+stable.360.7c451e694f3c52ee0aeb01d7e28b5fa18cd0ad2f (Zed)
OS: Windows 10.0.26200
Memory: 13.7 GiB
Architecture: x86_64
GPU: Intel(R) Iris(R) Xe Graphics || Intel Corporation || 31.0.101.5522

### Attach Zed log file

<details><summary>Zed.log</summary>

No relevant log output was produced when reproducing this issue.

</details>

### Relevant Zed settings

<details><summary>settings.json</summary>

No relevant settings. The issue was also reproduced with a clean Zed configuration.

</details>

### Relevant Keymap

<details><summary>keymap.json</summary>

No relevant keymap changes. The issue was also reproduced with a clean Zed configuration.

</details>

### (for AI issues) Model provider details

_No response_

### If you are using WSL on Windows, what flavor of Linux are you using?

Ubuntu

Recordings: in the opening post: recording-1.mp4, recording-2.mp4.
