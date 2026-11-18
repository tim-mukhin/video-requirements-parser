# real/ha-55519

_claude-sonnet-5.5@default, 15 s; looked at: nothing_

In Home Assistant 2026.11.0b2, adding a condition to an automation in Safari 27.0 (WebKit, PWA) on macOS 15.8.1 makes the frontend extremely slow. The reporter says it bogged down the whole MacBook and some clicks were not registered. It reportedly does not reproduce in Opera (Chromium). The report is based on the ticket text only; the recording failed to upload.

## Automation condition editor unusably slow in Safari/WebKit with many entities

Class: **stuck**

Environment: Home Assistant Core 2026.11.0b2 frontend; Safari 27.0 (20625.1.29.18.28), used as a PWA; macOS Sequoia 15.8.1; MacBook Pro. Not reproduced in Opera. Account and organization not given.

Steps:

1. Use a Home Assistant instance with a large number of entities (exact count not given). (00:00.0; )
2. Open the automation editor in Safari (PWA) on macOS. (00:00.0; )
3. Start adding a condition to an automation. (00:00.0; )
4. Observe that the UI becomes extremely slow and drops some clicks. (00:00.0; )

Expected (speech): The UI stays responsive when adding a condition.

Actual: The frontend becomes unusably slow in WebKit when adding a condition. The system is heavily loaded and some mouse clicks are not registered. No console errors are reported.

Key events: 

Claims:

- "Does not reproduce in Opera (Chromium)." [Does not appear to reproduce inside Opera.]: not shown - No video or evidence is available. The wording is hedged ('does not appear').
- "The slowdown is caused by having many entities." [Have a lot of entities]: not shown - Listed as a reproduction step, but the entity count is not given and no comparison was made.
- "The browser console shows no errors." [No errors]: not shown - Not verifiable from the ticket alone.
