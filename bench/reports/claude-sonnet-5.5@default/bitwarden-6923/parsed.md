# real/bitwarden-6923

_claude-sonnet-5.5@default, 18 s; looked at: frames/000514.jpg, frames/000545.jpg_

Bitwarden desktop (macOS) is set to show in the menu bar. Clicking its menu bar icon opens the Bitwarden window, which flips between the settings view and the App Store Bitwarden page (181.7 MB, version 2023.10.1). The vault window flickers on and off by itself, apparently without further user input. The recording is short and has no narration, so the cause is not stated.

## Bitwarden desktop window repeatedly appears and disappears after clicking the menu bar icon

Class: **intermittent**

Environment: macOS, Bitwarden desktop app (settings view, 'App Settings (All Accounts)', account <email>) with the Mac App Store page for Bitwarden (version 2023.10.1) behind it. QuickTime Player is the recording app. The menu bar icon is enabled, along with Minimise/Close/Start to menu bar and Start automatically on login.

Steps:

1. Click in the menu bar area near the Bitwarden menu bar icon at the start. The Bitwarden window comes to the front showing settings over the App Store page. (00:00.2; p001, p003, p004)
2. Click the menu bar icon again (OCR reads 'O3'). The Bitwarden window appears in front once more. (00:07.0; p010, p011, p012)
3. The cursor stays on the icon. The window alternates repeatedly between Bitwarden settings in front and only the App Store page (Bitwarden window hidden), about every 0.5–2 s, until the end of the video. (00:07.9; p013, p014, p016, p017, p019, p020, p022, p023, p025)

Expected (implied): Clicking the menu bar icon should show or hide the Bitwarden window once and it should stay in that state.

Actual: The Bitwarden window repeatedly shows and hides. The foreground alternates between Bitwarden and the App Store page or QuickTime. The screen shows no further clicks to explain this, and only the click at 00:07.0 is visible. The video ends with the window hidden.

Key events: p010, p013, p014, p016, p017, p019, p020, p022, p023, p025

Missed by the author:

- The only utterance is the single word 'you' (u002), probably a misheard word. The author says nothing about the flicker.
- A 0.1 s flash at the start shows the QuickTime menu bar, then Bitwarden comes to the front (p002).
