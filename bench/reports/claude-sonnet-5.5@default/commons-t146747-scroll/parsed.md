# real/commons-t146747-scroll

_claude-sonnet-5.5@default, 21 s; looked at: frames/000311.jpg, frames/000621.jpg_

A silent, no-audio phone recording shows a German Wikipedia-style reader on Android. The viewer follows links from OROS to Hydromorphon, Pentobarbital, Veterinärmedizin, Hochschule, Technische Universität and ETH Zürich, then goes back. No error, failure or wrong data is visible, so the reason the video was recorded is unclear.

## No defect visible: article-to-article navigation with link preview cards

Class: **not-a-bug**

Environment: Android phone in portrait (a guess), a Wikipedia-style German reader in an in-app browser. A bottom preview card with 'ARTIKEL LESEN' shows for each tapped link. Status bar clock 20:49-20:50. Wi-Fi is on and the network-speed indicator changes. No account or organisation is shown.

Steps:

1. A preview card for 'Orales osmotisches System' is shown, then the full article opens (trigger not visible). (00:00.9; p001, p002)
2. Further preview cards and articles open in turn: Hydromorphon, Pentobarbital, Veterinärmedizin, Hochschule, Technische Universität, ETH Zürich. Each is opened by an input the video does not show. (00:03.6; p004, p008, p012, p015, p020, p026, p030)
3. The list of universities is shown with a dimmed background and the ETH Zürich link underlined, with the preview card at the bottom. This is the standard link-preview state. (00:18.9; p028, p029, p030, p031)
4. The view goes back through ETH Zürich, the university list and Technische Universität (back navigation or tab switch, trigger not visible). (00:24.1; p036, p037, p038)

Expected (implied): Links open previews and articles, and going back returns to the previous page. This is the observed behaviour.

Actual: Every transition completes within about a second. No error, blank page, wrong content or stuck state is visible. The text of the Technische Universität and ETH Zürich cards is consistent between the preview and the full article. I cannot tell what the author wanted to show. The most likely candidates are the scroll or page-transition smoothness, or the preview-card behaviour, but neither visibly misbehaves. Only the OCR text was checked on most transitions. The frames at p012 and p031 were viewed directly.

Key events: p012, p030, p031, p036, p038

Missed by the author:

- The network speed readout in the status bar changes (for example 0, 12, 56, 98 and 175 KB/s). This is ordinary traffic and not a defect (p005, p007, p011, p025).
