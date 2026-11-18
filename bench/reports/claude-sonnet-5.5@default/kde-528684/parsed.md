# real/kde-528684

_claude-sonnet-5.5@default, 41 s; looked at: frames/000164.jpg, frames/000636.jpg, frames/000578.jpg, frames/000317.jpg, frames/000942.jpg_

A silent, captioned screen recording of a KDE Plasma desktop. The caption says a pinned app disappears from the Task Manager after its window is moved with a keyboard shortcut, and that it sometimes happens with apps minimized to tray. The pinned Konsole launcher is missing right after its window goes, and the pinned Serein launcher is absent in the 12:50 frame and shown twice in the final frame. The keystrokes are not visible, so the exact trigger is not confirmed.

## Pinned app launcher vanishes from Task Manager after its window is moved/closed (Konsole, Serein)

Class: **silent-fail**

Environment: KDE Plasma (kde-linux), vertical Icons-Only Task Manager panel on the left, user 'matthew'. Konsole (zsh) and Serein (a chat app, Settings > Keybinds) windows. Serein is also in the system tray. Recording is 1920x1080, no audio, no cursor or keys visible.

Steps:

1. Caption states the scenario: an app is pinned in the Task Manager and its window is moved with a keyboard shortcut. The caption text is the author's claim, not an action. (00:00.1; p002)
2. A Konsole window opens (the trigger is not visible). It is briefly resized, flashing 'Size: 90 x 28', and disappears. Right after, the Task Manager has no Konsole pinned icon: the chevron icon below the pinned launchers is gone. (00:04.4; p044, p046, p068)
3. Konsole is open again, and the Task Manager shows the pinned/running Konsole icon (chevron) highlighted. (00:10.5; p071)
4. The Konsole window closes again and the application launcher menu opens (the trigger is not visible). (00:11.4; p072, p075)
5. Caption: it sometimes happens with other apps minimized to tray. The Serein context menu from the Task Manager is shown (Open New Window, Unpin from Task Manager, More...). Serein's Keybinds settings window is open. (00:19.2; p149, p150)
6. Serein is shown running from the tray. In the 12:50 frame, the Task Manager has no pinned Serein icon. It holds asterisk, Telegram, a purple app and a chevron only. (00:21.1; p246)
7. Serein is shown a second time, and now the Task Manager lists two Serein icons: one highlighted, one plain. (00:31.3; p266)

Expected (implied): A pinned app's launcher stays in the Task Manager whether its window is moved, closed or minimized to tray, and a running app maps to a single entry.

Actual: Pinned launcher icons disappear from the Task Manager (Konsole after its window goes away, Serein while it is in the tray). When Serein is running, it appears twice. This is inferred from frames only, since no key presses are visible.

Key events: p002, p068, p071, p149, p246, p266

Missed by the author:

- Konsole's pinned chevron icon is absent in the 00:05 frame, then back at 00:10 and in the 00:21 frame, so it flickers in and out [p068, p071].
- Serein is shown twice in the Task Manager in the last frames, one pinned-style and one extra, which the author does not mention [p266].
- Serein's tray icon appears at about 00:21 while no pinned Serein launcher is visible [p246].

Claims:

- "If an app is pinned and moved with a keyboard shortcut, the app disappears." [p002]: not shown - No keystroke is visible. The Konsole pinned icon is missing in frame 000164 at 00:05, but it is also missing while the window is absent, so the link to the shortcut is not confirmed.
- "It sometimes happens with other apps minimized to tray." [p149]: not shown - Only Serein is shown, and the tray state is seen in only two frames. The missing pinned Serein icon at 00:21 is consistent with the claim, but is not proof.
