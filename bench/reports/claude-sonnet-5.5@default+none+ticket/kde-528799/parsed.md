# real/kde-528799

_claude-sonnet-5.5@default, 15 s; looked at: nothing_

In what appears to be Krita on Android, the reporter says the leftmost arrow-like tool (probably the Select/Transform tool) makes a vector layer snap when it is stretched, even though all snapping settings are off. They say the snap distance grows with each stretch, so precise resizing isn't possible. The ticket is thin and the video was not available.

## Vector layer snaps when stretched with the leftmost arrow tool even though all snap settings are off

Class: **wrong-data**

Environment: Android, 'latest public' Qt as of 13 Nov 2026. The app is not named in the ticket (likely Krita, from the vector layer and snap settings). App version, device, KDE Plasma and Frameworks versions are not given.

Steps:

1. Select the leftmost arrow-like tool, which the reporter thinks is freehand select. (00:00.0; )
2. Try to stretch a vector layer. (00:00.0; )
3. Repeat the stretch several times. The reporter says the snapping gets further away with each stretch. (00:00.0; )

Expected (speech): The vector layer does not snap and can be stretched precisely, since all snap settings are off.

Actual: The vector layer snaps while being stretched, and the reporter says the snap offset grows with each repeated stretch.

Key events: 

Claims:

- "All snap-to settings are off" [even if all my snap to... Settings are off]: not shown - The ticket has no video or screenshots and doesn't say which settings were checked.
- "Snapping gets worse the more times the layer is stretched" [The more times you stretch it, the further away it snaps]: not shown - Only the reporter's description is available, with no measurements.
