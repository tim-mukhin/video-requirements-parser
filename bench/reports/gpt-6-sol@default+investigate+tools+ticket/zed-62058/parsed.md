# real/zed-62058

_gpt-6-sol@default, 65 s; looked at: frames/0007.0.jpg, frames/0011.0.jpg, frames/0013.0.jpg, frames/0032.0.jpg, frames/0036.5.jpg, frames/moments/p053.jpg, frames/0008.5.jpg, frames/0009.0.jpg, frames/0010.5.jpg, frames/moments/p114.jpg, frames/moments/p120.jpg, frames/moments/p104.jpg, frames/0035.5.jpg, frames/0003.0.jpg, frames/0004.0.jpg, frames/0005.0.jpg, frames/0006.5.jpg, frames/0030.0.jpg, frames/0031.0.jpg, frames/0034.0.jpg, frames/0037.5.jpg, frames/0011.5.jpg, frames/0015.5.jpg, frames/0031.5.jpg, frames/0039.5.jpg, frames/moments/p041.jpg_

After a backtick is typed in Zed, a later backtick can appear beside it even after a click places the caret elsewhere. The recording shows this in a Go file and a Docker Compose file; the extra characters corrupt the text, and the YAML displays diagnostics.

## Backticks appear at an earlier insertion point after clicking elsewhere

Class: **wrong-data**

Environment: Zed editing pkg/env/env.go and docker-compose.yml. The ticket reports Zed 1.13.1 on macOS Tahoe 26.6, but the video does not show the version, OS, or settings.

Steps:

1. In pkg/env/env.go, click at the end of the line 25 fmt.Errorf call and type backticks (typing inferred from the text change). (00:03.0; p005, p011, p012)
2. Click in the line 30 fmt.Errorf call, then type more backticks (typing inferred from the text change). (00:08.8; p029, p040, p042)

Expected (implied): A backtick typed after the click appears at the newly selected position.

Actual: The caret is shown on line 30, but the backticks accumulate after the line 25 call instead. In docker-compose.yml, they likewise accumulate after line 6's environment: despite clicks on later lines.

Key events: p005, p029, p040, p042, p086, p095, p115, p120

Missed by the author:

- The YAML example shows red diagnostics under environment: and its entries after the misplaced backticks [p095, p104, p120].
- A Go syntax diagnostic flashes briefly while the misplaced text is present [p053]; its moment frames show the flash.

Claims:

- "A later backtick is written beside the earlier one rather than at the newly clicked position." [ticket]: confirmed - The Go and YAML demonstrations show the caret moved to another line while backticks accumulate at the earlier location.
- "The behavior occurs in any file." [ticket]: not shown - The video shows a Go file and a Docker Compose YAML file only.
- "The recording establishes Zed 1.13.1, macOS Tahoe 26.6, and the reported settings." [ticket]: not shown - No version, OS information, or settings screen appears.
