# real/gshell-9532

_gpt-6-sol@default, 48 s; looked at: frames/0010.0.jpg, frames/0011.0.jpg, frames/0018.5.jpg, frames/0000.0.jpg, frames/moments/p030.jpg, frames/moments/p041.jpg, frames/moments/p005.jpg, frames/moments/p011.jpg, frames/moments/p019.jpg, frames/moments/p022.jpg, frames/moments/p027.jpg, frames/moments/p029.jpg, frames/0008.5.jpg, frames/0012.5.jpg, frames/0003.5.jpg, frames/0006.0.jpg, frames/0015.5.jpg, frames/0017.5.jpg, frames/0019.5.jpg, frames/0021.5.jpg, frames/0020.0.jpg, frames/0020.5.jpg, frames/0021.0.jpg, frames/0013.5.jpg, frames/0014.5.jpg, frames/0016.5.jpg_

GNOME's workspace overview can linger between two workspaces: two large previews sit side by side while the purple selection outline straddles their thumbnails. The recording also shows abrupt transitions, but the switcher later moves and returns to the desktop; it is not shown permanently stuck.

## Workspace overview lingers between workspaces with misaligned selection

Class: **intermittent**

Environment: GNOME Shell overview with four workspace thumbnails. The ticket reports GNOME 51.1 on CachyOS; neither is visible in the recording.

Steps:

1. Move between workspaces in the overview; the input is not visible. The preview settles on one workspace by 00:03.5. (00:02.9; p016)
2. Continue changing the overview state while moving between workspaces (the trigger is not visible). After the app grid appears at 00:09.2, the overview returns to a split position at 00:10.0. (00:09.2; p027, p028, p029)

Expected (implied): The overview finishes on one workspace, with its preview and selection outline aligned.

Actual: At 00:10.0–00:11.0, two previews remain side by side and the selection outline crosses two thumbnails. A similar split is visible at 00:18.5. The view subsequently moves; around 00:19.5–00:20.5 the previews also expand abruptly toward the desktop before settling.

Key events: p016, p027, p028, p029, p039, p043, p044, p045

Missed by the author:

- The frames show the outline already crossing thumbnails at the start of the recording; the triggering input is not captured [p001].
- The timeline records transitions into the app grid and later back to the desktop, and the frames show the switcher continues responding [p028, p038, p045].

Claims:

- "The switcher can get stuck between two states." [ticket: Bug summary]: confirmed - The frames show a split position persisting through 00:10.0–00:11.0, though later movement rules out a permanent freeze.
- "Pressing Super during a gesture animation causes it." [ticket: Steps to reproduce]: not shown - Neither the keypress nor the gesture input is visible. The recording already starts in a split position.
- "There are weird animations throughout." [ticket: title]: confirmed - The frames show abrupt preview expansion around 00:19.5–00:20.5; the timeline's local flicker detections alone do not establish separate failures.
- "The affected version is GNOME 51.1 on CachyOS." [ticket: Affected version]: not shown - No version or distribution information appears on screen.
