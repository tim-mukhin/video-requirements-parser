# real/zed-62058

_claude-sonnet-5.5@default, 32 s; looked at: frames/0000.0.jpg, frames/0006.0.jpg, frames/0012.0.jpg, frames/0018.0.jpg, frames/0024.0.jpg, frames/0030.0.jpg, frames/0036.0.jpg, frames/0042.0.jpg, frames/0003.0.jpg, frames/0009.0.jpg, frames/0021.0.jpg, frames/0027.0.jpg, frames/0033.0.jpg, frames/0041.5.jpg, frames/0041.0.jpg_

In Zed, typing a backtick and then clicking elsewhere and typing another backtick puts the new backtick next to the first one, not at the clicked cursor. The video repeats this in a Go file (env.go) and in docker-compose.yml. Typed text ends up in the wrong place, which can corrupt code.

## Backtick typed after clicking elsewhere is inserted at the previous backtick's position, not at the cursor

Class: **wrong-data**

Environment: Zed editor (version 1.13.1 and macOS Tahoe 26.6 per ticket only, not visible in the video). One-Dark-style dark theme. Files pkg/env/env.go (Go) and docker-compose.yml (YAML). Git blame annotation 'Mustapha Boudouch' is visible in the YAML file.

Steps:

1. Open env.go and place the cursor at the end of line 25, after `key)`. This is inferred from the cursor position and the mouse pointer. (00:03.0; 0003.0)
2. Type a backtick. It appears at the end of line 25. This is inferred from the later frame. (00:06.0; 0006.0)
3. Click elsewhere, for example inside `fmt` on line 25 (shown selected/highlighted), then on line 17 and line 30. Type backtick again. The extra backticks pile up after `key)` on line 25, not at the clicked cursor positions (line 17 cursor is at `int8`). The count grows from 1 to 6 to about 10 to 14. (00:09.0; 0006.0, 0009.0, 0012.0, 0018.0)
4. Click at the end of line 33 (`return v, nil`) and type a backtick. This works the first time, because it is the first backtick after the click. (00:24.0; 0024.0)
5. Repeat the typing: the backticks accumulate at the line-33 position. Then switch to the docker-compose.yml tab. (00:27.0; 0027.0, 0030.0)
6. In docker-compose.yml, backticks accumulate after `environment:` on line 6 (2, then 3, then 5). They appear there while the cursor and clicks are elsewhere (line 15 at 0036.0, the mouse pointer elsewhere at 0041.0). (00:41.0; 0033.0, 0036.0, 0041.0)

Expected (implied): Each backtick is inserted at the current cursor position, wherever the user last clicked.

Actual: Later backticks are inserted at the position of the earlier backtick, not at the new cursor position. In docker-compose.yml they land on line 6 while the cursor is on line 15.

Key events: 0009.0, 0012.0, 0036.0, 0041.0

Missed by the author:

- The bug repeats in the YAML file, not only in the Go file (0033.0, 0036.0, 0041.0).
- After the first backtick there is a red squiggle at the end of line 25 (0006.0), which suggests an autoclose or pair behaviour. The backtick does not auto-pair in a visible way.
- In the video many backticks are typed in a row, up to about 14 on line 25 (0018.0), not just two.

Claims:

- "The second backtick is inserted next to the first one, not at the new cursor position." [Instead, it gets written next to the first backtick that was typed earlier.]: confirmed - Frames 0009.0 and 0012.0 show backticks piling up after `key)` on line 25 while the cursor is elsewhere. Frame 0036.0 shows them on line 6 of the YAML file while the cursor is on line 15.
- "The cursor was moved by clicking, not with the arrow keys." [click elsewhere - do not use arrow keys]: not shown - The mouse pointer moves between frames, so clicks are likely, but no click is visible and there is no sound. Clicks are inferred.
- "Default settings, with no custom settings." [Using default settings (no custom settings.json overrides)]: not shown - No settings are visible. The ticket's own settings.json shows custom theme, icon theme and font sizes, which contradicts 'default settings'.
