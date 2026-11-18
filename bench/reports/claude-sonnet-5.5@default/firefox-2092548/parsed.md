# real/firefox-2092548

_claude-sonnet-5.5@default, 19 s; looked at: frames/000040.jpg, frames/000097.jpg_

A 5-second, silent Firefox recording with no speech. The vertical tab sidebar expands and collapses twice, and each time the Google page content reflows (page links move, the footer links change and the page width changes). The author's intent is not stated, so the exact defect is a best guess.

## Vertical tab sidebar expand/collapse makes the page layout jump and flicker on google.com

Class: **intermittent**

Environment: Firefox with the vertical tabs sidebar, www.google.com (signed out), zoom 90%, 1280x720. One tab, 'Google'.

Steps:

1. Move the cursor to the left window edge (x=0, y≈437) with the sidebar collapsed. The sidebar expands to show 'Google ×' and '+ New Tab'. The page shifts right and the page's 'Advertising', 'Business' and 'India' links disappear. The trigger is inferred, not seen. (00:01.2; p003, p004, p005, p006)
2. Click in the page area at (210, 376). The sidebar collapses to an icon strip and the page content reflows back, with the footer links reappearing. The icon at (249, 367) then loses its drawing. (00:01.8; p010, p011, p017, p020)
3. Repeat: go to the left edge (0, 412). The sidebar expands again and the footer links vanish. (00:02.6; p021, p022, p024)
4. Click at (243, 368). The sidebar collapses and the page reflows, with a darker icon at (345, 340) that then goes blank. (00:03.1; p028, p029, p034, p036, p037)

Expected (implied): Opening or closing the tab sidebar should change the layout once and cleanly. It should not leave flickering or vanishing page elements, and page icons should not disappear.

Actual: Every sidebar toggle makes the page content jump. Footer and header links ('Advertising', 'Business', 'India', 'About', 'Store') flash or disappear for 0.4–0.8 s. The screen states alternate between sidebar-open and sidebar-collapsed layouts. Icon regions lose their drawing after the toggles (p020, p037).

Key events: p004, p006, p011, p017, p020, p022, p029, p037

Missed by the author:

- The page links reflow and flash with each sidebar toggle (p006–p015, p024–p033).
- Icons go blank after the toggles (p020, p037).
