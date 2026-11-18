# real/vscode-337449

_claude-sonnet-5.5@default, 21 s; looked at: frames/000200.jpg, frames/000146.jpg_

A silent, wordless 8-second recording of VS Code with a Flutter project (fitcity-flutter, main.dart) and an iOS simulator beside it. No action fails and no error appears. The only visible changes are the Explorer toolbar icons appearing on hover and disappearing again, which is normal VS Code behaviour. The video does not show what the author wanted to demonstrate.

## No defect visible; Explorer toolbar icons only appear on hover

Class: **not-a-bug**

Environment: VS Code with project fitcity-flutter, main.dart open (tabs: main.dart, client_routes.dart, index.dart). Status bar shows the debug target 'iPhone 17 Pro (ios simulator)', 0 errors, 66 warnings, 43 infos. An iOS simulator window is partly visible on the right. No audio.

Steps:

1. main.dart is open with the cursor at Ln 34, Col 8. The status bar target changes to 'iPhone 17 Pro (ios simulator)'. (00:00.3; p002, p005)
2. Hover the mouse over deep_link_resolver.dart in the Explorer. The Explorer header toolbar icons (new file, new folder, refresh, collapse) appear (lighter). They disappear again at 00:03.5 when the cursor leaves the sidebar (frame 000146 compared with 000200). (00:02.6; p016, p017, p018, p019, p020, p023, p024, p025, p026)
3. Click at [2261, 980] on the right edge of the editor (the scrollbar/minimap area). A later change in the same area is not tied to a visible click. (00:05.0; p032, p041, p043)

Expected (implied): Unknown. The author said nothing and showed no failing action.

Actual: No error, hang or wrong value is visible. The icon changes are VS Code's normal hover-only toolbar. The editor and Explorer stay stable, and the file list and open tabs do not change. The only anomaly is that the code comments are in Uzbek. They are not a defect.

Key events: p016, p023, p032, p043

Missed by the author:

- The video has no audio, so nothing the author noticed is known.
- Possible candidates: the status bar shows 66 warnings and 43 infos [p005], and the simulator is selected as the target [p002]. Neither looks wrong on screen.
- A very short flash of '2' at 00:03.4 [p022] is most likely a transient line-number or counter change in the editor.
