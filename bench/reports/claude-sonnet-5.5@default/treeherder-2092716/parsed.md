# real/treeherder-2092716

_claude-sonnet-5.5@default, 18 s; looked at: frames/000002.jpg, frames/000030.jpg, frames/000088.jpg, frames/000098.jpg_

In Treeherder's Failure Summary panel, the icon inside a button goes blank while the cursor is over it. This happened for the left button (circle icon) and the right button (bug icon). The icon returns when the cursor leaves. The video has no audio and no click is visible.

## Failure Summary icon buttons lose their icon while hovered

Class: **silent-fail**

Environment: Treeherder, job details panel, Failure Summary tab. The failure is 'AssertionError: in-tree files should pass the linter', with a line 'i2009222 Perma [tier 2] clang-tidy'. Browser and account are not visible.

Steps:

1. Open the Failure Summary tab. The left button with the circle icon and the right button with the bug icon are both drawn normally. (00:00.0; )
2. Move the cursor over the left button, the circle icon beside the AssertionError line. The icon inside disappears. (00:02.2; p001)
3. Move the cursor away. The icon is drawn again. (00:02.9; p002)
4. Move the cursor over the right button, the bug icon at the end of the line. A tooltip 'File a…' flashes and the icon disappears. (00:06.7; p004, p005)
5. Move the cursor away. The icon is drawn again. (00:07.5; p007, p006)

Expected (implied): The button icon stays visible on hover, perhaps with a highlight, and the tooltip shows.

Actual: While hovered, the icon inside each button is blank (0% of the drawing left, p001 and p005). It reappears afterwards. No error is shown.

Key events: p001, p002, p004, p005, p007

Missed by the author:

- There is no speech, so nothing is said about the problem.
- The hover at 00:05.3 over the 'AssertionError' failure line (p003) has no visible effect beyond OCR noise.
- The tooltip 'File a…' on the bug button (p004, frame 000088) is shown only briefly.
