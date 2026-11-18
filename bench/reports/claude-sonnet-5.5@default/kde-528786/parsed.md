# real/kde-528786

_claude-sonnet-5.5@default, 40 s; looked at: frames/000043.jpg, frames/000167.jpg, frames/000254.jpg, frames/000462.jpg, frames/000202.jpg, frames/000244.jpg, frames/000358.jpg, frames/000340.jpg, frames/000412.jpg, frames/000424.jpg, frames/000451.jpg_

In KDE System Settings > Accessibility, the author turns off 'Shake pointer', applies, then clicks 'Padrões' (Defaults) and applies again, all on the 'Agitar ponteiro' sub-page. When they open 'Lente de aumento' (Magnifier) afterwards, the 'Melhorar a nitidez do conteúdo da tela ao aplicar zoom' checkbox is checked. It was unchecked at the start, and the author never touched it. Defaults and Apply on one sub-page appear to change settings on another sub-page. There is no speech, so the intent is not stated.

## Defaults + Apply on 'Shake pointer' page silently enables an unrelated Magnifier option

Class: **wrong-data**

Environment: KDE Plasma System Settings (Portuguese-Brazil UI), 'Acessibilidade' module, sub-pages 'Lente de aumento' and 'Agitar ponteiro'. Recording at 3840×2160. No accounts or organizations seen.

Steps:

1. Open Accessibility > Magnifier. 'Melhorar a nitidez do conteúdo da tela ao aplicar zoom' is unchecked, 'Habilitar rastreio de cursor de texto' is unchecked, and Zoom is 'Tela cheia'. The cursor only hovers here. (00:01.7; p003)
2. Click the 'Agitar ponteiro' sub-page. 'Habilitar' is checked. (00:06.7; p005, p006, p008)
3. Click the 'Habilitar' checkbox to uncheck it. The title gets '*', and Apply and Restore become enabled. (00:08.2; p032, p033, p035)
4. Click 'Aplicar'. The '*' disappears and Apply and Restore are disabled again. (00:10.3; p036, p037, p038)
5. Click 'Padrões'. 'Habilitar' becomes checked again, the title shows '*', and Apply and Restore are enabled. (00:14.6; p042, p044, p046)
6. Click 'Aplicar' (the click is not in the timeline, but the cursor is on the button and the '*' is gone). The state is applied. (00:17.4; )
7. Click back to 'Lente de aumento'. 'Melhorar a nitidez…' is now checked. The other options are unchanged. (00:18.8; p047, p048, p052, p049)

Expected (implied): Settings on the Magnifier page stay as they were, because the author only changed 'Shake pointer'. If 'Padrões' is meant to reset the whole module, the page should say so or ask for confirmation.

Actual: After 'Padrões' and 'Aplicar' on the 'Agitar ponteiro' page, the Magnifier checkbox 'Melhorar a nitidez do conteúdo da tela ao aplicar zoom' is checked. It was unchecked before and the author never touched it (hover only at p003). The author gave no sign of noticing.

Key events: p003, p042, p046, p047, p052, p037

Missed by the author:

- The Magnifier checkbox 'Melhorar a nitidez…' changed from unchecked to checked (p003 vs p052) without being touched. The most likely cause is that 'Padrões' resets the whole Accessibility module, not just the visible sub-page. This is not proven, because the Magnifier page is not shown between the two actions.
- The 'Aplicar' click at about 17.3 s is not in the click list. Frames 000412 and 000424 show it was applied.
