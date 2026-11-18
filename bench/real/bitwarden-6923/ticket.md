# Fast clicking the menu bar icon doesn't close Bitwarden correctly

Source: https://github.com/bitwarden/clients/issues/6923  (reporter: D3m3rion, filed 2023-11-20)

### Steps To Reproduce

1. Go to settings, enable show, minimize to, close to and start to menu bar
2. Close the main window and Have Bitwarden run in the background (no dock icon, only the menu bar icon)
3. Click on the menu bar icon to open the main window and directly click it again to close it.

### Expected Result

The Bitwarden window closes and the focus is shifted to the the window/app that was previously in focus.

### Actual Result

The Bitwarden window does not disappear/close, or it closes but the focus is still on Bitwarden.

### Screenshots or Videos

[attachment: recording.mp4]

As you can see, when I first click on the menu bar icon, the Bitwarden window opens and the focus correctly shifts. If I then click it again directly, the Bitwarden window does not close. At about 00:09, you can see how the window closes, but the focus does not shift back to QuickTime Player.

### Additional Context

Reinstalled Bitwarden a few minutes before recording the video.
The issue was already present in multiple client versions and multiple macOS versions before.

### Operating System

macOS

### Operating System Version

14.2 Beta (23C5047e)

### Installation method

Mac App Store

### Build Version

2023.10.1 (13648)

### Issue Tracking Info

- [X] I understand that work is tracked outside of Github. A PR will be linked to this issue should one be opened to address it, but Bitwarden doesn't use fields like "assigned", "milestone", or "project" to track progress.
