# real/gshell-9532

_claude-sonnet-5.5@default, 13 s; looked at: nothing_

In GNOME Shell 51.1 on CachyOS, pressing Super while a workspace-switcher gesture animation is still running can leave the switcher stuck between two states. The reporter also sees odd animations elsewhere. The ticket is thin and the recording isn't available, so the exact states and timing are unknown.

## Workspace switcher can get stuck between two states when Super is pressed mid-gesture animation

Class: **stuck**

Environment: GNOME Shell 51.1 on CachyOS (latest). Hardware, input device, session type (Wayland or X11), extensions and workspace count are not stated.

Steps:

1. Open the workspace switcher view (overview) using a touchpad or touch gesture. (00:00.0; )
2. While the gesture's transition animation is still running, press the Super key. (00:00.0; )
3. Observe that the switcher ends up stuck between two states. (00:00.0; )

Expected (implied): The switcher finishes or reverses the transition cleanly and ends in a consistent state, either the overview or the normal desktop.

Actual: The workspace switcher is left stuck between two states, a half-transitioned view. The reporter also says there are 'weird animations throughout', without details.

Key events: 

Claims:

- "The switcher can be left stuck between 2 states." [it is possible to get the switcher stuck between 2 states]: not shown - No video is available, and the ticket doesn't describe which two states.
