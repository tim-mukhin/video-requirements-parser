# real/kde-528786

_claude-sonnet-5.5@default, 29 s; looked at: frames/0005.0.jpg, frames/0020.0.jpg_

In System Settings > Accessibility, pressing Defaults (Padrões) on the 'Agitar ponteiro' (Shake pointer) page also reset the 'Lente de aumento' (Magnifier) page. The Magnifier checkbox 'Melhorar a nitidez…' went from unchecked to checked. No warning appeared, so settings on pages the user never opened can be lost silently.

## Defaults button on one Accessibility page resets other pages in the category with no warning

Class: **silent-fail**

Environment: KDE System Settings (pt-BR UI), Accessibility category, dark theme, Wayland and Plasma 6.8.2 per the ticket (not visible in the video). Pages: Lente de aumento (Magnifier) and Agitar ponteiro (Shake pointer). The video does not show the Union style mentioned in the ticket.

Steps:

1. Open Accessibility > Lente de aumento. 'Melhorar a nitidez do conteúdo…' is unchecked, Padrões is enabled, and Aplicar/Restaurar are disabled. The cursor only hovers over the checkbox (no click). (00:01.7; p004)
2. Click the 'Agitar ponteiro' page. (00:06.7; p007, p008)
3. Change the 'Habilitar' checkbox on that page. The title gets '*' and Aplicar becomes enabled. The click is only inferred from the screen change; the timeline labels the click at 8.2 s 'Zoom'. (00:08.2; p034, p035, p036, p037)
4. Click Aplicar. The '*' disappears and the change is saved. (00:10.3; p039, p040)
5. Click Padrões on the same Shake pointer page. The change is reverted and Aplicar is enabled again. No confirmation or warning appears. (00:14.6; p044, p046, p047, p048)
6. Apply again. The '*' clears at about 17.4 s; the timeline shows no click event for this step. (00:17.4; s021)
7. Click back to 'Lente de aumento'. 'Melhorar a nitidez…' is now checked and Padrões is greyed out, meaning the page is at its defaults. It was unchecked at the start. (00:18.8; p050, p055, p075)

Expected (implied): Defaults resets only the current page, or first warns that the whole Accessibility category will be reset (the ticket also suggests a 'This page' / 'Entire category' choice).

Actual: Defaults on the Shake pointer page reset the whole category. The Magnifier checkbox went from unchecked to checked, and the UI gave no warning or indication of the wider scope.

Key events: p004, p044, p047, p050, p055, p075

Missed by the author:

- The Magnifier checkbox was unchecked before any Defaults press (5.0 s) and checked afterwards (20.0 s). The video does not show whether the unchecked value was a deliberate user setting or just differed from the default, but Padrões was enabled on that page at the start.
- Defaults only stages the change; the other page's reset becomes visible only when switching back to it (p055).

Claims:

- "The entire menu is reset to Default." [ticket]: confirmed - The Magnifier checkbox is unchecked at 5.0 s (Padrões enabled) and checked at 20.0 s (Padrões greyed out), after Defaults was pressed on another page.
- "Clicking Default gives no warning about the scope." [ticket]: confirmed - No dialog or message appears around the Defaults click at 14.6 s.
- "The user made and applied changes on one page, then used Defaults to undo them." [ticket]: confirmed - The Shake pointer change was applied at 10.3 s and reverted with Defaults at 14.6 s.
- "Environment: Plasma 6.8.2, Wayland, Union style." [ticket]: not shown - No version or style information is visible in the video.
