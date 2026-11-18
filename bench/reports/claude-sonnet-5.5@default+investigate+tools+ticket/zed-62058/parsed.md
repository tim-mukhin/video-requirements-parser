# real/zed-62058

_claude-sonnet-5.5@default, 23 s; looked at: frames/0012.0.jpg, frames/0036.0.jpg_

Backticks typed after clicking elsewhere in Zed are inserted after the first backtick, not at the clicked cursor. In env.go they pile up after `key)` on line 25 while the cursor is on line 30. In docker-compose.yml they pile up after `environment:` on line 6 while the cursor is on line 15. Text lands in the wrong place and can corrupt code, for example the syntax error flagged at 00:19.9.

## Backtick is inserted at the previous backtick's position instead of the current cursor after clicking elsewhere

Class: **wrong-data**

Environment: Zed editor, dark theme. Files pkg/env/env.go (Go) and docker-compose.yml (YAML, git blame 'Mustapha Boudouch' visible). Zed 1.13.1 and macOS 26.6 are from the ticket only and are not visible in the video. Video is 42.5 s, no speech. Keystrokes are not seen, so the typing of backticks is inferred from the screen.

Steps:

1. In env.go, click in the editor near line 25 (the cursor and click are on `return zero, fmt.Errorf(...key)`); type a backtick (inferred from a backtick appearing at the end of line 25). (00:03.0; p005)
2. Click elsewhere (the line 17 type list at 5.3 s and 6.1 s, line 25 at 7.0 s, line 30 at 8.8 s) and type backtick again. The new backticks appear after `key)` on line 25, not at the clicked line. By 12.0 s about 10 are on line 25 while the cursor is on line 30. The first typed backtick (step 1) does land at the click. (00:08.8; p029, p033, p040)
3. Repeat the click-and-type in env.go. A syntax error 'expected ';'' flashes at 19.9 s after a click, and the click at 22.2 s lands at line 32 (the Go file also shows this at the end of line 33). (00:19.8; p052, p053, p059, p064)
4. Switch to the docker-compose.yml tab, click on line 6 `environment:` at 31.1 s, then click on line 15 `condition: service_healthy` at 34.4 s and 35.3 s, and line 17 at 38.0 s, typing backticks (inferred). The backticks accumulate after `environment:` on line 6 (2, 3, then 5 over the clip). At 36.0 s the cursor is on line 15 and the backticks (3) are still on line 6. (00:34.4; p086, p110, p115, p121)

Expected (implied): Each backtick is inserted at the current cursor position, wherever it was last clicked.

Actual: After a click moves the cursor, later backticks are written next to the earlier backtick (line 25 of env.go, line 6 of docker-compose.yml). The cursor shown is on a different line. The repeated backticks also produce syntax errors and red squiggles over the YAML.

Key events: p029, p040, p045, p053, p107, p110, p115, p121

Missed by the author:

- The bug is not limited to a pair of backticks: about 10 pile up in env.go, shown at 0012.0 (p040).
- Red error squiggles and a flashed 'expected ';', found' syntax error appear in env.go at 19.9 s (p053), and red squiggles over the whole environment block in the YAML (0036.0).
- The bug also appears in docker-compose.yml (p086, p110, p115).

Claims:

- "The second backtick is written next to the first backtick typed earlier, not at the new cursor position." [ticket]: confirmed - Frame 0012.0: about 10 backticks after `key)` on line 25 while the cursor is on line 30. Frame 0036.0: backticks after `environment:` on line 6 while the cursor is on line 15.
- "Reproduces with any file." [ticket]: confirmed - Seen in both a Go file and a YAML file; only those two were checked.
- "The cursor is moved by clicking, not with the arrow keys." [ticket]: confirmed - CLICK events are logged before the changes (p029, p033, p110, p115, p121). Keys are not visible in the video.
- "Default settings, no overrides." [ticket]: refuted - The ticket's own settings.json sets a theme, an icon theme and font sizes. No settings are visible on screen.
