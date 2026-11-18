# real/bitwarden-6923

_claude-sonnet-5.5@default, 26 s; looked at: nothing_

With Bitwarden running only as a menu bar icon, clicking the icon to show and then hide the window works when the window stays open about 2 s or more. The hide then returns focus to QuickTime Player. When the window is hidden within about 0.5–1 s of opening, the window disappears but the menu bar still shows Bitwarden as the active app. This is an intermittent focus-restore failure that looks timing-dependent.

## Hiding the window via the menu bar icon soon after showing it leaves Bitwarden as the frontmost app instead of restoring the previous app

Class: **intermittent**

Environment: macOS, Mac App Store Bitwarden 2023.10.1 (per the App Store page on screen and the ticket). Bitwarden desktop is signed in as <email>. Settings page shows menu bar icon options enabled. QuickTime Player is the previously focused app, with the App Store Bitwarden page behind it.

Steps:

1. Start with Bitwarden running only as a menu bar icon and QuickTime Player frontmost. Click the Bitwarden menu bar icon at (996, 5). The window opens and Bitwarden becomes frontmost. (00:00.2; p001, p003, p004)
2. Control case: click the icon again after the window has been open about 3.4 s. The window hides and QuickTime Player is frontmost again. The same happens for the 4.4 s to 6.3 s cycle, which was open about 1.9 s. (00:03.8; p005, p006, p008)
3. Open the window (CLICK at the O3 menu bar item) and hide it again about 0.9 s later. The window is gone but the menu bar still reads Bitwarden, so focus did not return to QuickTime Player. (00:07.0; p010, p011, p013)
4. Repeat quick open and hide cycles (the window is shown at 8.5 s, hidden at 9.0 s, shown at 9.8 s, hidden at 10.8 s, shown at 11.6 s, hidden at 12.3 s). Each hide leaves Bitwarden frontmost with no window visible, in the 4 quick cycles checked. (00:08.5; p014, p016, p017, p019, p020, p022)
5. Control case: open the window at 14.5 s and leave it about 2 s. The hide at 16.5 s correctly returns focus to QuickTime Player. (00:14.5; p023, p025)

Expected (implied): Hiding the window through the menu bar icon makes it disappear and returns focus to the app that was frontmost before (QuickTime Player), however quickly it follows the open.

Actual: After a quick show and hide the window disappears but Bitwarden stays the active app (menu bar shows Bitwarden), so focus is not restored. When the window stays open for about 2 s or more, focus is restored correctly.

Key events: p005, p008, p013, p016, p019, p022, p025

Missed by the author:

- The slow open and hide cycles at 0.4–3.8 s and 4.4–6.3 s restore focus to QuickTime Player correctly (p005, p008), as does the last one at 16.5 s (p025). This contrast suggests a timing dependence on how long the window has been open.
- The cursor is followed through 99% of the video, but only two clicks are inferred (p001, p010). The other icon clicks are not visible as separate events, so the later open and hide triggers are inferred from the screen changes.
- The Settings page shows 'Start automatically on login' checked and 'Always show in Dock' unchecked, which the ticket does not mention.

Claims:

- "The Bitwarden window does not close when the icon is clicked again quickly." [ticket]: refuted - In the cycles checked, the window disappeared every time (p013, p016, p019, p022). At 0.5 s frame sampling a slow hide cannot be ruled out, but the video does not show a window that stays open.
- "The window closes but focus is still on Bitwarden (at about 00:09)." [ticket]: confirmed - At 7.9 s and 9.0 s the window is gone and the menu bar reads Bitwarden (p013, p016).
- "The first click opens the window and focus shifts correctly." [ticket]: confirmed - p003 and p004 show Bitwarden frontmost with the window shown after the click at 0.2 s.
- "The issue was already present in multiple client versions and macOS versions before." [ticket]: not shown - The video shows one machine and one build.
- "Bitwarden was reinstalled a few minutes before recording." [ticket]: not shown - Nothing in the video shows this.
