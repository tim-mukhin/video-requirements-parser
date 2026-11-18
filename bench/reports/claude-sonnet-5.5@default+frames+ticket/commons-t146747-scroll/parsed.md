# real/commons-t146747-scroll

_claude-sonnet-5.5@default, 66 s; looked at: frames/0000.0.jpg, frames/0004.0.jpg, frames/0008.0.jpg, frames/0012.0.jpg, frames/0016.0.jpg, frames/0020.0.jpg, frames/0024.0.jpg, frames/0028.0.jpg, frames/0032.0.jpg, frames/0035.5.jpg, frames/0017.0.jpg, frames/0018.0.jpg, frames/0019.0.jpg, frames/0026.0.jpg, frames/0027.0.jpg, frames/0013.0.jpg, frames/0022.0.jpg, frames/0025.0.jpg, frames/0030.0.jpg, frames/0031.0.jpg, frames/0021.0.jpg, frames/0016.5.jpg, frames/0026.5.jpg, frames/0017.5.jpg, frames/0020.5.jpg_

In the Wikipedia Android app, each article opened from a link first renders at the top, then jumps to a mid-page or near-bottom scroll position that looks inherited from the previous article. This happened for Veterinärmedizin, Hochschule and ETH Zürich. The video matches the ticket. Technische Universität opened at the top, so the effect is not seen on every page.

## New article opened via link/preview jumps to the previous page's scroll position instead of the top

Class: **state-revert**

Environment: Wikipedia Android app, German-language articles (de), in a dark-toolbar article view with a link-preview bottom sheet ("ARTIKEL LESEN"). Phone screen recording at 20:49–20:50. Version, device and OS are only in the ticket (2.3.152, LG G4, Android 6.0). The video does not show them.

Steps:

1. Open an article (Pentobarbital) and scroll down through the sections. The first frame is blank. (00:04.0; 0004.0, 0008.0, 0012.0)
2. Tap a wikilink; a preview sheet for Veterinärmedizin appears (inferred tap), then tap ARTIKEL LESEN (inferred). (00:16.0; 0016.0)
3. The new article starts at the top (header image, title, empty body, loading bar), which is the expected position. (00:16.5; 0016.5)
4. Within about 0.5 s the same article jumps to mid-page (Berufsorganisationen section) with no scroll gesture visible. This is the bug. (00:17.0; 0017.0, 0017.5)
5. Open the Hochschule link from this page, which shows a preview and then the article. It starts at the top, then jumps to the list near the bottom of the article. (00:20.0; 0019.0, 0020.0, 0020.5)
6. Scroll further, tap Technische Universität (preview shown), then go back or scroll to the Schweiz > ETH Zürich link and open it (inferred). (00:25.0; 0022.0, 0024.0, 0025.0)
7. ETH Zürich loads at the top, then jumps to the Departemente section near the bottom, with the scrollbar at the bottom of the track. (00:26.5; 0026.0, 0026.5, 0027.0)
8. Technische Universität later opens correctly at the top. At 31.0 the ETH page is at the top again. (00:32.0; 0031.0, 0032.0, 0035.5)

Expected (implied): A newly opened linked article is shown from the top, with no scroll offset carried over from the previous article.

Actual: The new article renders at the top and then jumps to a mid-page or near-bottom position that appears to depend on the scroll position of the previous article. This is seen in 3 of 4 transitions.

Key events: 0016.5, 0017.0, 0020.0, 0020.5, 0026.0, 0026.5

Missed by the author:

- The page first renders correctly at the top and then jumps while still loading, so the scroll is restored late (0016.5→0017.0, 0020.0→0020.5, 0026.0→0026.5).
- Links were opened from the preview bottom sheet, not directly (0016.0, 0019.0, 0022.0, 0025.0).
- Technische Universität opened at the top at 32.0, so the bug depends on prior scroll state.

Claims:

- "The new page opens somewhere in the page, related to the previous page's scroll position" [New page opens somewhere in the page, somehow related to scroll status on the former page]: confirmed - Veterinärmedizin, Hochschule and ETH Zürich all jump away from the top soon after loading. The new article sits at a position similar in proportion to where the previous article was scrolled. The video cannot prove the cause.
- "Steps: open a page, scroll down, open a wikilink" [1. Open a page 2. Scroll down 3. Open a wikilink]: confirmed - The video shows scrolling and then opening links through preview sheets. The ticket does not mention the preview sheet or ARTIKEL LESEN step.
- "The bug happens every time" [(implied by the ticket)]: refuted - Technische Universität (32.0–35.5) opened at the top and stayed there. In that case the previous page was already at the top.
