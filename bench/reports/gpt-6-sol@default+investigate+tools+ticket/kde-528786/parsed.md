# real/kde-528786

_gpt-6-sol@default, 35 s; looked at: frames/0002.0.jpg, frames/0008.5.jpg, frames/0015.0.jpg, frames/0019.5.jpg, frames/moments/p042.jpg, frames/0016.5.jpg, frames/0017.5.jpg, frames/moments/p035.jpg, frames/moments/p033.jpg, frames/0014.0.jpg, frames/0017.0.jpg, frames/0018.0.jpg, frames/moments/p049.jpg, frames/moments/p001.jpg_

In KDE System Settings, using Defaults on Accessibility > Shake Cursor and applying the change also changes an option on the separate Magnifier page, without warning that other pages are affected. A user trying to reset one page can therefore overwrite an existing setting elsewhere.

## Accessibility Defaults changes settings on other pages without warning

Class: **wrong-data**

Environment: KDE System Settings, Portuguese-language Accessibility category. The ticket reports CachyOS, Plasma 6.8.2 and Union; the recording does not show those details.

Steps:

1. Start with Magnifier's 'Improve the sharpness of screen contents when zooming' option unchecked. (00:01.7; p004)
2. Open Shake Cursor, turn off Enable, and click Apply. (00:06.7; p007, p034, p039)
3. While still on Shake Cursor, click Defaults and apply the pending change. (00:14.6; p044, p046, p048)

Expected (implied): Reset only the current page, or warn that the Accessibility category will be reset and let the user choose the scope.

Actual: After the reset is applied, Magnifier's sharpness option is checked, although it was unchecked at the start. No scope choice or warning appears.

Key events: p004, p007, p034, p039, p044, p046, p048, p050, p055

Missed by the author:

- The concrete cross-page change is Magnifier's sharpness checkbox: unchecked initially, checked after Defaults is used on Shake Cursor [p004, p044, p050, p055].
- The recording shows Shake Cursor being disabled and applied before Defaults; it does not show the checkbox being turned back on and applied beforehand, as the frame-only notes inferred [p034, p039, p044].

Claims:

- "The entire menu is reset to Default." [ticket.md: OBSERVED RESULT]: not shown - The recording demonstrates a change on one other Accessibility page, not the state of every setting in the category.
- "Defaults gives no warning that it affects the entire category." [ticket.md: EXPECTED RESULT]: confirmed - No warning or scope selection appears during the recorded reset.
- "The recording shows the reported software versions and Union theme." [ticket.md: SOFTWARE/OS VERSIONS; ADDITIONAL INFORMATION]: not shown
