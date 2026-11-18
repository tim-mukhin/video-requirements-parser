# real/bitwarden-6923

_claude-sonnet-5.5@default, 40 s; looked at: frames, frames/0000.0.jpg, frames/0002.0.jpg, frames/0004.0.jpg, frames/0006.0.jpg, frames/0008.0.jpg, frames/0010.0.jpg, frames/0012.0.jpg, frames/0014.0.jpg, frames/0016.0.jpg, frames/0017.5.jpg, frames/0001.0.jpg, frames/0003.0.jpg, frames/0005.0.jpg, frames/0007.0.jpg, frames/0009.0.jpg, frames/0011.0.jpg, frames/0013.0.jpg, frames/0015.0.jpg_

With Bitwarden running only as a menu bar icon, the icon is clicked repeatedly to show and hide the window. Some hides leave Bitwarden as the frontmost app (menu bar shows "Bitwarden") instead of returning focus to QuickTime Player. Other hides restore focus correctly, so the result is inconsistent.

## Hiding the Bitwarden window via the menu bar icon sometimes leaves focus on Bitwarden instead of the previous app

Class: **intermittent**

Environment: macOS (Mac App Store Bitwarden 2023.10.1, per the App Store page and ticket). Bitwarden desktop is signed in as <email>. QuickTime Player is the previously focused app, with the App Store Bitwarden page behind. Settings visible: Show menu bar icon, Minimise to menu bar, Close to menu bar, Start to menu bar and Start automatically on login are checked. Always show in the Dock is unchecked.

Steps:

1. Start with Bitwarden running only as a menu bar icon, with the window hidden. QuickTime Player is the frontmost app (menu bar reads "QuickTime Player"). The Settings tab already has the menu bar options enabled. (00:00.0; 0000.0, 0002.0)
2. Click the Bitwarden menu bar icon (inferred click). The window opens and Bitwarden becomes frontmost. (00:01.0; 0001.0, 0002.0)
3. Click the icon again. The window hides and focus returns to QuickTime Player, which is correct. (00:04.0; 0004.0)
4. Click the icon to open the window again, then click it again quickly to hide it. The window hides but the menu bar still shows "Bitwarden" as the frontmost app. Focus did not return to QuickTime Player. (00:08.0; 0006.0, 0008.0)
5. Repeat the open and hide cycle. Several more hides leave Bitwarden frontmost with no window visible. Only the last one (about 17.5 s) returns focus to QuickTime Player. (00:13.0; 0010.0, 0012.0, 0014.0, 0016.0, 0017.5)

Expected (implied): When the window is hidden via the menu bar icon, it disappears and focus returns to the app that was frontmost before (QuickTime Player).

Actual: After some hides, no Bitwarden window is visible but the menu bar still shows Bitwarden as the active app (for example at 8.0 s and again around 13–14 s). Focus returns to QuickTime Player only on some hides (4.0 s and 17.5 s).

Key events: 0004.0, 0008.0, 0014.0, 0017.5

Missed by the author:

- The behaviour is inconsistent: some hides restore QuickTime focus correctly (0004.0, 0017.5), so it looks like a timing or race condition rather than a deterministic fault.
- Start automatically on login is also enabled, and Always show in the Dock is off. The ticket does not mention either.

Claims:

- "The first click opens the window and focus correctly shifts to Bitwarden." [when I first click on the menu bar icon, the Bitwarden window opens and the focus correctly shifts]: confirmed - The window appears and the menu bar changes to Bitwarden (0002.0, 0006.0).
- "The window sometimes closes but focus stays on Bitwarden." [it closes but the focus is still on Bitwarden]: confirmed - The window is gone while the menu bar reads Bitwarden (0008.0, 0014.0).
- "The window does not close when the icon is clicked again." [the Bitwarden window does not close]: not shown - The sampled frames show the window hiding on each cycle. A window that stays visible cannot be distinguished from slow hiding at 0.5 s sampling.
- "This happens at about 00:09." [At about 00:09]: confirmed - The window is hidden and Bitwarden is still frontmost at about 8–9 s (0008.0).
