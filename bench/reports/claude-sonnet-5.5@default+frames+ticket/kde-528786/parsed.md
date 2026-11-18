# real/kde-528786

_claude-sonnet-5.5@default, 47 s; looked at: frames, frames/0000.0.jpg, frames/0004.0.jpg, frames/0008.0.jpg, frames/0012.0.jpg, frames/0016.0.jpg, frames/0020.0.jpg, frames/0023.0.jpg, frames/0005.0.jpg, frames/0006.0.jpg, frames/0010.0.jpg, frames/0011.0.jpg, frames/0013.0.jpg, frames/0014.0.jpg, frames/0018.0.jpg, frames/0007.0.jpg, frames/0009.0.jpg, frames/0015.0.jpg, frames/0017.0.jpg, frames/0019.0.jpg, frames/0017.5.jpg, frames/0014.5.jpg, frames/0018.5.jpg_

In System Settings > Accessibility, the Defaults (Padrões) button was used on the 'Shake pointer' page. It also reset a setting on the 'Magnifier' page, which the user had not opened in that session. Nothing in the UI says Defaults covers the whole category, so the user can lose settings on other pages without knowing.

## Defaults button on one Accessibility page also resets the settings of other pages in the category, with no warning

Class: **not-a-bug**

Environment: KDE System Settings (Portuguese-BR UI) on Wayland, Accessibility category, Plasma 6.8.2 per the ticket. Pages seen: Magnifier (Lente de aumento) and Shake pointer (Agitar ponteiro). Dark theme (the ticket says Union). The time in the taskbar is 07:51:07.

Steps:

1. Open System Settings > Accessibility > Magnifier. 'Improve sharpness of content when zooming' is unchecked, with no pending changes (Apply is disabled). The user hovers over this checkbox around 4 s; no click is visible. (00:00.0; 0000.0, 0004.0, 0005.0)
2. Click the 'Shake pointer' page in the second column (inferred from the cursor on the item and the page change). The page shows 'Enable' already checked, and Defaults is enabled. (00:06.0; 0006.0, 0007.0)
3. Uncheck 'Enable' on the Shake pointer page (inferred). The title gets '*' and Apply and Restore become enabled. (00:09.0; 0008.0, 0009.0, 0010.0)
4. Click Apply. The '*' goes away and the buttons are disabled again, so the change is saved. 'Enable' stays unchecked. (00:11.0; 0011.0, 0012.0)
5. Click Defaults (Padrões) on the same Shake pointer page. 'Enable' goes back to checked and there is a pending change ('*', Apply enabled). No confirmation or warning appears. (00:14.5; 0014.0, 0014.5, 0015.0)
6. Click Apply. (00:17.5; 0017.0, 0017.5)
7. Go back to the Magnifier page. 'Improve sharpness...' is now checked, though it was unchecked at the start. The Defaults on the Shake pointer page also reset this other page. (00:18.0; 0018.0, 0018.5, 0019.0, 0020.0)

Expected (implied): Defaults should reset only the page the user is on, or warn that it will reset the whole Accessibility category (or let the user choose 'This page' or 'The entire category').

Actual: Defaults on the Shake pointer page also changed another page: the Magnifier checkbox went from unchecked to checked. The UI gave no warning and does not say that Defaults covers the whole category.

Key events: 0005.0, 0014.5, 0015.0, 0018.0, 0020.0

Missed by the author:

- The Magnifier checkbox was unchecked at 0000.0–0005.0, before any Defaults, and was not changed on the Shake pointer page. The video does not show whether that value was a deliberate user setting.
- After Defaults, the change still has to be applied (Apply, 0017.5) before it is saved. The Magnifier change that came with it only becomes visible on the Magnifier page at 0018.0.

Claims:

- "Defaults resets the entire category, not just the current page." [OBSERVED RESULT: The entire menu is reset to Default.]: confirmed - After Defaults on Shake pointer, the Magnifier checkbox, which was unchecked at 0005.0, is checked at 0018.0 and 0020.0.
- "No warning is shown when Defaults is clicked." [Clicking the button should give a message warning that the entire menu will be reset to Default.]: confirmed - No dialog or message appears at 0014.5–0015.0.
- "The user made and applied changes on one page, then used Defaults to undo them." [Make and apply changes to settings in one page. Use the Default button to undo those changes.]: confirmed - The Shake pointer change was applied at 0011.0 and then reverted with Defaults at 0014.5. The video does not show how the Magnifier checkbox came to be unchecked; it was already that way at 0000.0.
