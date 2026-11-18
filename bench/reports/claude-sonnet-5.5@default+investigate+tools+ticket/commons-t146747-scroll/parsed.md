# real/commons-t146747-scroll

_claude-sonnet-5.5@default, 58 s; looked at: frames/0011.0.jpg, frames/0010.0.jpg, frames/0012.0.jpg, frames/000311.jpg, frames/000356.jpg, frames/000417.jpg, frames/0016.5.jpg, frames/000873.jpg, frames/000833.jpg_

In the Wikipedia Android app (German), articles opened from a link preview first render at the top and then end up mid-page or near the bottom, as if the previous article's scroll position had been applied. The video shows no touch input, so a user scroll cannot be excluded for every transition. The clearest case is Veterinärmedizin.

## Article opened via link preview does not stay at the top; it lands mid-page after loading

Class: **state-revert**

Environment: Wikipedia Android app, German articles (Pentobarbital, Veterinärmedizin, Hochschule, Technische Universität, ETH Zürich), phone portrait 1080x1920, status bar 20:49-20:50, link-preview bottom sheet with ARTIKEL LESEN. App version, device and OS (2.3.152, LG G4, Android 6.0) come from the ticket only; the video does not show them. Note: the direct frames run about 4 s later than the timeline clock.

Steps:

1. Open the Pentobarbital article and scroll down through its sections (touch input is not visible). (00:00.9; p005, p012, p014)
2. A link preview sheet for Veterinärmedizin with ARTIKEL LESEN appears over the scrolled article (the trigger is not visible). (00:10.9; p025)
3. The full article is opened via ARTIKEL LESEN (the trigger is not visible). It is shown scrolled to the Berufsorganisationen section, not at the top. In the direct frames it had first rendered at the top with the loading bar. (00:12.8; p029)
4. Repeat from the next links. Hochschule opens at the top (14.2 s) and then shows mid-page and the list near the bottom (15.1 s, 15.5 s). ETH Zürich opens at the top (18.9 s) and by 20.5 s shows the Hönggerberg section far down. User scrolling in between is not excluded. (00:14.2; p032, p037, p038, p048, p055)

Expected (implied): A newly opened linked article is shown from the top, with no scroll offset carried over from the previous article.

Actual: Veterinärmedizin is shown at Berufsorganisationen right after opening. Hochschule and ETH Zürich also leave the top within about 1-2 s. Technische Universität opened at the top both times it was opened (16.8 s and 26.9 s), so it does not happen on every open.

Key events: p025, p029, p032, p038, p048, p055, p040, p072

Missed by the author:

- The articles are opened through the preview sheet (ARTIKEL LESEN), not directly (p025, p061).
- The page first shows the top with a loading bar, and the position changes only afterwards, so the scroll is applied late (direct frame 0016.5 versus p029).

Claims:

- "New page opens somewhere in the page, related to the scroll status of the former page" [ticket]: confirmed - Veterinärmedizin appears mid-page after Pentobarbital was scrolled down (p029). The video cannot prove the cause.
- "Steps: open a page, scroll down, open a wikilink" [ticket]: confirmed - The video shows scrolling, then a link preview sheet and ARTIKEL LESEN. The ticket does not mention that preview step.
- "Implied: it happens every time" [ticket]: refuted - Technische Universität opened at the top at 16.8 s and 26.9 s (p040, p072).
