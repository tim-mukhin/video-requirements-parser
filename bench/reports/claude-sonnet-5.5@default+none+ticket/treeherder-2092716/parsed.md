# real/treeherder-2092716

_claude-sonnet-5.5@default, 14 s; looked at: nothing_

On TreeHerder, icons on gray buttons in the Failure Summary panel (file-bug, pin/thumbtack) disappear while the pointer hovers over the button. This makes the buttons hard to identify and use. It was reported in both Chrome and Firefox, in light and dark mode.

## TreeHerder Failure Summary button icons disappear on hover

Class: **wrong-data**

Environment: treeherder.mozilla.org, Firefox and Chrome, light and dark color-scheme, no sign-in needed. OS and browser versions are not given.

Steps:

1. Visit https://treeherder.mozilla.org/ (00:00.0; )
2. Click a red or orange task. (00:00.0; )
3. In the 'Failure Summary' area at the bottom, hover a gray button such as 'file-bug' or 'pin/thumbtack'. (00:00.0; )

Expected (speech): The icon stays visible while the button is hovered.

Actual: The icon disappears while hovering. The reporter's screenshot shows an 'alert' icon turning white and nearly invisible on the hovered button, which suggests the icon color matches the hover background.

Key events: 

Claims:

- "Happens in both Chrome and Firefox" [This happens in Chrome as well as Firefox.]: not shown - Only the reporter's statement; no evidence is available without the video.
- "Independent of color-scheme" [This happens regardless of your preferred color-scheme]: not shown - Only the reporter's statement; no evidence is available without the video.
- "Sign-in is not required" [You don't need to be signed in to TreeHerder to test this.]: not shown - Only the reporter's statement; no evidence is available without the video.
