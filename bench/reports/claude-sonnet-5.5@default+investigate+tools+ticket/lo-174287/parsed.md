# real/lo-174287

_claude-sonnet-5.5@default, 33 s; looked at: frames/0025.0.jpg, frames/0039.0.jpg, frames/0027.0.jpg, frames/0040.0.jpg, frames/0038.5.jpg_

In Writer, menu-bar menus (Format, Styles, Table) are seen opening and then disappearing within about 0.5–2 s. In one case the menu is already dismissed while its title is still highlighted. Dismissal is only on screen; no click or cursor is visible, so what dismisses them is unknown.

## Writer menu-bar menus close right after opening (Format, Styles, Table seen)

Class: **intermittent**

Environment: LibreOffice Writer, blank 'Untitled 1' document, dark theme, GNOME-style top bar (Thu Nov 5 09:51, screen recorder running), 1366x768. Wayland, Fedora 44 and version 26.2.6.3 are not visible in the video; they come from the ticket only.

Steps:

1. Writer is open on an empty document. A menu-bar menu is opened (the trigger is not visible). The Format popup appears with its Text submenu already expanded, tall and starting near the top of the screen over the title bar rather than under the menu bar (frame 0025.0, recorder timer 0:25). (00:25.0; p004)
2. The popup is gone and only the plain menu bar remains, with nothing chosen (frame 0027.0, timer 0:27). Visible for about 1.5–2 s. (00:27.0; p005)
3. Repeat: menus are opened in quick succession and each is replaced within about 0.5 s. Table is open at 0038.5, Styles at 0039.0 (the list shows Body Text highlighted) and Format again at 0039.5. At 0040.0 the Format title is highlighted but no popup is shown (opened, trigger not visible). (00:38.5; p007)

Expected (implied): A menu opened from the menu bar stays open, under its title, until an item is picked or it is dismissed, so the pointer can move into it.

Actual: Menus are on screen for 0.5–2 s and then vanish with nothing picked. The Format menu was placed at the top of the screen, covering the title bar. A highlighted menu title with no popup (Format at 0040.0) shows a menu already dismissed. Insert is never seen open in this video.

Key events: p004, p005, p007

Missed by the author:

- The Format popup is drawn at the top of the screen, over the title bar, with the Text submenu already open (frame 0025.0; the ticket does not mention placement).
- At 0040.0 the Format title is highlighted but no popup is open: a menu was dismissed instantly, which is a clearer failure than one that closes after about 2 s.
- The parser timeline's timestamps for later events run ahead of the direct frames and recorder timer (for example, the File menu is shown at timeline 00:39.0 / timer 0:42). Times above use the direct frames and recorder timer.

Claims:

- "Insert, Format or Styles menus appear briefly and then close." [ticket]: confirmed - Format (frames 0025.0 to 0027.0) and Styles (0039.0) are seen open and then gone. Table was also seen. Insert was not seen open.
- "Reproducible: Always." [ticket]: not shown - No menu is visible for the first 24 s. No cursor or click is shown, so it is unclear whether the menus were tried and failed, or not tried. The ticket's own 'sometimes' fits better.
- "Persists in Safe Mode, after a profile reset, with SAL_USE_VCLPLUGIN=gen, with hardware acceleration on or off, and maximized or not; GNOME on Wayland, Fedora 44, version 26.2.6.3." [ticket]: not shown - Nothing on screen shows any of these settings, the session type or the version.
- "Workaround: moving the pointer across the menu bar with another menu open." [ticket]: not shown - The rapid Table, Styles, Format sequence is consistent with this, but no pointer is visible.
