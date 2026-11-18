# real/lo-174287

_claude-sonnet-5.5@default, 44 s; looked at: frames/0000.0.jpg, frames/0003.0.jpg, frames/0006.0.jpg, frames/0010.0.jpg, frames/0015.0.jpg, frames/0020.0.jpg, frames/0025.0.jpg, frames/0030.0.jpg, frames/0035.0.jpg, frames/0040.0.jpg, frames/0045.0.jpg, frames/0021.0.jpg, frames/0022.0.jpg, frames/0023.0.jpg, frames/0024.0.jpg, frames/0026.0.jpg, frames/0027.0.jpg, frames/0037.0.jpg, frames/0039.0.jpg, frames/0041.0.jpg, frames/0038.0.jpg, frames/0038.5.jpg, frames/0039.5.jpg, frames/0025.5.jpg, frames/0026.5.jpg, frames/0013.0.jpg_

In Writer, a menu-bar menu stays open only about 1–2 s. Format shows at 0:25–0:26.5, then it is gone at 0:27. A burst of menus, including Styles, Table and Format, flashes by at 0:38–0:40. The video has no pointer and no sound, so clicks are inferred.

## Writer menu-bar menus (Format, Styles) close by themselves after about 1–2 s

Class: **intermittent**

Environment: LibreOffice Writer, blank 'Untitled 1' document, dark theme, GNOME-style top bar (Thu Nov 5 09:51, screen recorder running). The Wayland session, Fedora 44 and version 26.2.6.3 from the ticket are not visible in the video. The window looks close to full-screen.

Steps:

1. Writer is open on an empty document with the cursor in the header area and the menu bar idle. No menu opens in the first 24 s, and no pointer is visible, so any clicks in this stretch are not shown. (00:00.0; 0000.0, 0010.0, 0020.0)
2. A menu-bar menu is opened, inferred to be Format by click (the pointer is not visible). It appears as a tall popup with Text, Spacing and so on, and its Text submenu is already expanded. The popup starts at the top of the screen over the title bar, not under the menu bar. (00:25.0; 0025.0, 0025.5)
3. The popup is still visible, then it has closed by 0:27 with no item chosen. Total visible time is about 1.5–2 s. (00:26.0; 0026.0, 0026.5, 0027.0)
4. Several menu-bar entries are tried quickly. Form is highlighted at 0:38, Table is open at 0:38.5, Styles is open at 0:39, and the Format popup is open again at 0:39.5. All of them are gone or replaced within about 0.5 s. Edit is highlighted at 0:41 with no popup. (00:38.0; 0038.0, 0038.5, 0039.0, 0039.5, 0041.0)

Expected (implied): A clicked menu stays open until the user picks an item or dismisses it, so the pointer can move into the menu. It also opens under its menu-bar title.

Actual: Menus appear for 1–2 s or less and disappear without any item being chosen. The Format popup is drawn at the top of the screen, overlapping the title bar. A highlighted but empty menu title (Format at 0:40, Edit at 0:41) shows a menu that was dismissed immediately.

Key events: 0025.0, 0026.5, 0027.0, 0038.5, 0039.0, 0039.5, 0040.0

Missed by the author:

- The Format popup is drawn at the top of the screen with its Text submenu already open, not below the menu bar (0025.0).
- Menus that fail show only a highlighted title, with no popup (Format at 0040.0, Edit at 0041.0).
- Between 0:38 and 0:40 several different menus flash in turn (0038.5 Table, 0039.0 Styles, 0039.5 Format), which fits the workaround of moving across the menu bar.

Claims:

- "Insert, Format and Styles menus close right after opening." [Insert, Format, or Styles menu may fail to open or disappear shortly after opening]: confirmed - Format at 0:25–0:26.5 and Styles at 0:39 are visible only briefly. Insert is never seen open.
- "The problem happens always." [Reproducible: Always]: not shown - Nothing is visible for the first 24 s. The video cannot tell us whether the menus were not clicked or failed to open. The 'sometimes' wording in the description is closer to what is shown.
- "Safe Mode, profile reset, SAL_USE_VCLPLUGIN=gen, the hardware acceleration setting, window maximization and the Wayland session." [persists in Safe Mode and with gen plugin]: not shown - No title bar, terminal or settings in the frames show any of this.
