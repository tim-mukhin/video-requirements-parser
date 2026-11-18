# real/bitwarden-6923

_claude-sonnet-5.5@default, 14 s; looked at: nothing_

On macOS, with Bitwarden running only as a menu bar icon, clicking the icon to open the window and then clicking it again right away doesn't close the window reliably. Either the window stays open, or it closes but focus stays on Bitwarden instead of returning to the previous app. This disrupts the workflow of users who rely on the menu bar icon.

## Fast double-clicking the menu bar icon doesn't close Bitwarden window correctly or restore focus (macOS)

Class: **intermittent**

Environment: Bitwarden desktop 2023.10.1 (13648), Mac App Store build, macOS 14.2 Beta (23C5047e). Previously focused app in the recording was QuickTime Player. No account or organization is mentioned.

Steps:

1. In Bitwarden settings, enable Show menu bar icon, Minimize to menu bar, Close to menu bar and Start to menu bar. (00:00.0; )
2. Close the main window so Bitwarden runs in the background with no dock icon and only the menu bar icon. (00:00.0; )
3. Click the menu bar icon to open the main window. (00:00.0; )
4. Click the menu bar icon again immediately to close the window. (00:00.0; )

Expected (speech): The Bitwarden window closes and focus returns to the app or window that was focused before.

Actual: The window doesn't close. In a variant, it closes after a delay (about 00:09 in the video) but focus stays on Bitwarden and doesn't return to the previous app (QuickTime Player). The first click opens the window and shifts focus correctly.

Key events: 

Claims:

- "The first click opens the window and focus shifts correctly." [when I first click on the menu bar icon, the Bitwarden window opens and the focus correctly shifts]: not shown
- "The issue was already present in multiple client and macOS versions." [The issue was already present in multiple client versions and multiple macOS versions before.]: not shown - No video, and no version details are given.
