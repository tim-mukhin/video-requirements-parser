# real/gshell-9532

_claude-sonnet-5.5@default, 35 s; looked at: frames, frames/0000.0.jpg, frames/0003.0.jpg, frames/0006.0.jpg, frames/0009.0.jpg, frames/0012.0.jpg, frames/0015.0.jpg, frames/0018.0.jpg, frames/0021.5.jpg, frames/0004.5.jpg, frames/0007.5.jpg, frames/0010.5.jpg, frames/0013.5.jpg, frames/0016.5.jpg, frames/0020.5.jpg_

The recording shows the GNOME Shell overview and workspace switching, with a screen recorder timer running in the top bar. The overview repeatedly opens and closes while the workspace strip moves between workspaces. During the transitions the workspace thumbnails, search bar and dock are clipped, drawn half-faded, or the thumbnail strip is cut off. This matches the ticket's 'weird animations'. The video does not show the 'stuck between two states' result clearly.

## Workspace switcher/overview shows broken, half-finished animation states when toggled during a workspace gesture

Class: **intermittent**

Environment: GNOME Shell (ticket: GNOME 51.1 on CachyOS), Wayland-style desktop, 1920x1200. Overview with 4 workspaces, the dock showing 4 apps plus the app grid button, and a screen recorder timer in the top bar. Clock reads 13 Nov 11:46. No accounts or orgs are visible.

Steps:

1. Start in the overview with the workspace strip on the second workspace. Workspace 2 is between two windows. This is the initial state. (00:00.0; 0000.0)
2. Swipe or scroll to the first workspace (inferred gesture, not directly visible). The strip switches to workspace 1 and the overview starts to close, at the same time as the transition. (00:05.5; 0004.5, 0006.0)
3. The overview fully closes to the desktop. Search bar, dock and thumbnails are gone. (00:09.0; 0009.0)
4. Overview is re-opened (Super key, inferred) while the workspace animation is still running. The result is a mixed state: the thumbnail strip is half-hidden and the dock is half-visible while the windows are still large. (00:12.0; 0012.0)
5. Overview closes again, then the workspace slides sideways (a dark bar appears on the right edge). (00:15.0; 0015.0, 0017.0)
6. Overview opens again, with the strip moving to the second workspace. The thumbnail strip is clipped by the left window at 20.5 s. The dock is clipped and its app-grid icon is partly faded at 20.5 s, so it shows as three dots. (00:20.5; 0019.0, 0020.5)
7. The final state is the desktop with the workspace indicator on workspace 2. (00:21.5; 0021.5)

Expected (implied): Toggling the overview during a workspace-switch gesture should end in a consistent state (either fully open or fully closed). The animation should be smooth, and the thumbnail strip, search bar and dock should not be clipped or half-drawn.

Actual: Toggling the overview during a workspace-switch animation produces inconsistent intermediate visuals: a clipped thumbnail strip, a half-faded dock and search bar, and overview elements out of sync with the window layout (0012.0, 0020.5). The ticket says the switcher can stay stuck between two states. The sampled frames only show the transitions and a clean final desktop at 21.5 s, so a persistent stuck state is not confirmed.

Key events: 0012.0, 0015.0, 0020.5, 0021.5

Missed by the author:

- The ticket gives no precise steps, such as which gesture or how many workspaces. The video suggests a 4-workspace strip, repeated overview toggling and swipes about every 3 s.
- Mid-transition frames show the dock's app-grid icon partly drawn as three dots (0020.5).
- A dark vertical bar appears at the left (0009.0) and right (0017.0) screen edges during workspace slides.

Claims:

- "The workspace switcher can be left stuck between two states." [it is possible to get the switcher stuck between 2 states]: not shown - The frames show mixed, half-animated states during transitions (0012.0, 0020.5). The last frame (0021.5) shows a normal desktop, so no state that persists is visible.
- "There are weird animations throughout." [also weird animations throughout (ticket title)]: confirmed - The clipped strip and dock, the half-faded search bar (0004.5, 0015.0) and the sideways slide with a dark edge bar (0017.0) are all visible.
- "Pressing Super in the middle of the gesture animation triggers the problem." [Try to press the super key in between the animation of the gesture.]: not shown - There is no sound or key overlay. The overview toggling mid-transition is consistent with a key press, but it is only inferred.
