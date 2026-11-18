# real/zed-62058

_claude-sonnet-5.5@default, 27 s; looked at: frames/000405.jpg, frames/000544.jpg, frames/000701.jpg, frames/000057.jpg_

In a Go file in Zed, a run of backtick characters builds up at the end of line 25 after `fmt.Errorf(...)`. The text is real: a syntax diagnostic 'expected ';', found `' flashes over it. The recording has no speech and the keystrokes are not visible, so the trigger is unknown. The run is not removed by the end of the Go-file part of the recording.

## Zed: stray backtick characters accumulate at end of line 25 in env.go and cause a syntax error

Class: **silent-fail**

Environment: Zed editor, pkg/env/env.go (Go, func Get), then docker-compose.yml (ms-users service). No accounts or organizations visible. The recording has no speech. Keys are not seen; the cursor is followed for 90% of the video.

Steps:

1. Open pkg/env/env.go in Zed and click in the editor at line 25, `return zero, fmt.Errorf("%w: %q", ErrNotExist, key)` in func Get. The breadcrumb changes to func Get. (00:01.1; p001, p002)
2. Click at the end of line 25. A single backtick appears after `key)` and a red squiggle shows under it (keys not visible, so how the backtick was entered is unknown). Later frames show a row of about 14 backticks there. (00:03.0; p005, p003, p012)
3. Line 25 still ends in the backtick run (frame at 00:11.4). Lines 29-31 briefly get a yellow wavy underline on `if err != nil { ... }`, which is gone again by 00:15.4. (00:11.4; p036, p038, p042)
4. Click and select the backticks on line 25. The diagnostic tooltip 'expected ';', found ` (syntax)' flashes for 0.6 s. (00:19.8; p048, p049)

Expected (implied): Line 25 should end at `key)` with no extra characters, and the editor should show no syntax error.

Actual: Line 25 gets a long run of backtick characters after `key)`. Zed's Go diagnostics treat them as real code ('expected ';', found `'). The author says nothing about it and the video has no speech.

Key events: p003, p012, p036, p048, p049

Missed by the author:

- The parser's cross-checks flag 'error text on screen' at p038 and p042. These are OCR misreads of the valid format string `"%w: %q cannot be parsed as %T: %w"` on line 30 (frame 000544 shows it intact). They are not real errors.
- The real error is the syntax tooltip 'expected ';', found `' that flashes for 0.6 s (p049, frame 000701). The tooltip is easy to miss.
- A yellow wavy underline briefly covers lines 29-31 (frame 000405, p036). It is gone at 00:15.4, so it is probably a transient diagnostic.
- The recording ends in docker-compose.yml (p067 onward) with no visible problem. This part looks unrelated.
