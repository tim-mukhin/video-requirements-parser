# real/lo-174287

_gpt-6-sol@default, 59 s; looked at: frames/0024.5.jpg, frames/0025.0.jpg, frames/0026.5.jpg, frames/0027.0.jpg, frames/0039.5.jpg, frames/0040.0.jpg, frames/0040.5.jpg, frames/0028.0.jpg, frames/0030.0.jpg, frames/0032.0.jpg, frames/0034.0.jpg, frames/0036.0.jpg, frames/0038.5.jpg, frames/0041.0.jpg, frames/0042.0.jpg, frames/0023.0.jpg, frames/0024.0.jpg, frames/0037.5.jpg, frames/0040.0.jpg, frames/0041.5.jpg, frames/000130.jpg, frames/000137.jpg, frames/000209.jpg, frames/000120.jpg, frames/000049.jpg, frames/0009.0.jpg, frames/0039.0.jpg_

In a blank LibreOffice Writer document, the Format menu opens above the menu bar, covering its own label and part of the window title, then disappears. A later pass shows Format highlighted without a dropdown, while nearby menus open; the recording does not show the pointer or clicks, so it cannot establish why either menu closed.

## Writer Format menu is misplaced and sometimes disappears

Class: **intermittent**

Environment: A maximized, untitled LibreOffice Writer window on a GNOME desktop. The ticket names Fedora 44, Wayland and LibreOffice 26.2.6.3; those details are not visible in the recording.

Steps:

1. Open Format, then its Text submenu (the triggers are not visible). (00:24.1; p004)

Expected (implied): The selected menu stays open and accessible so an item can be chosen.

Actual: The Format dropdown and Text submenu appear above and across the menu bar [p004], then are gone at 25.4 s [p005]. Later frames show Format highlighted without a dropdown, although adjacent menus open. Unseen input could account for the closure; a failed mouse click is not established.

Key events: p004, p005, p007

Missed by the author:

- The Format dropdown begins above the menu bar and covers its label and part of the title [p004]; the later Table dropdown opens below the bar (direct/frames/0038.5.jpg). The frames settle this placement issue, which the ticket does not mention.
- The timeline reports “60:0” at 8.9 s [p001], but its frame shows an ordinary recording timer reading 0:09; this is OCR noise, not another screen problem.

Claims:

- "Insert, Format and Styles sometimes fail to open or close shortly after opening." [ticket.md: Description]: confirmed - Format is shown open and then closed [p004, p005], and later highlighted without a dropdown in direct/frames/0040.0.jpg. The recording does not establish a failed click or the same failure for Insert or Styles.
- "Moving across the menu bar from another open menu is a workaround." [ticket.md: Description]: not shown - Frames show different menus open in succession, but no pointer or clicks are visible, and the proposed technique is not demonstrably successful.
- "The problem persists in Safe Mode, after profile reset, with the gen plugin, at either acceleration setting and at either window size." [ticket.md: Description]: not shown - Only one maximized Writer window is visible; those configurations are not shown.
- "The issue is reproducible always." [ticket.md: Reproducible]: not shown - The recording does not expose clicks or enough identifiable attempts to establish a rate.
