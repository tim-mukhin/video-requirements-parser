# Some Writer menus (Insert, Format, and Styles) close immediately when selected by mouse (Fedora 44 GNOME Wayland)

Source: https://bugs.documentfoundation.org/show_bug.cgi?id=174287  (reporter: <email>, filed 2026-11-01)

Description:
I’m experiencing an issue with the Insert, Format, and Styles menus in LibreOffice Writer. When I try to open one of these menus from the top menu bar, it sometimes does not open or appears briefly and then disappears.

A workaround is to open a menu farther to the right or left, and move the pointer across the menu bar with a different menu open, but this is unreliable and awkward.

The issue persists:
- In LibreOffice Safe Mode
- After resetting my user profile
- When launching with SAL_USE_VCLPLUGIN=gen
- With hardware acceleration enabled or disabled
- Whether the Writer window is maximized or not

Environment:
- Fedora 44
- GNOME on Wayland (XDG_SESSION_TYPE=wayland)
- LibreOffice 26.2.6.3 620(Build:3)

Expected behavior:
The selected menu should remain open so I can move the pointer into it and choose an item.

Actual behavior:
The Insert, Format, or Styles menu may fail to open or disappear shortly after opening.

I have not yet tested whether the issue also occurs in an Xorg session.

With appreciation,
        Jonathan Lusk

Steps to Reproduce:
1. Open LibreOffice Writer.
2. Click Insert on the menu bar.
3. Repeat with Format and Styles.

2.
3.

Actual Results:
The Insert, Format, or Styles menu sometimes fails to open or appears briefly and then closes.

Expected Results:
The selected menu stays open so I can move the pointer into it and choose a menu item.

Reproducible: Always

User Profile Reset: Yes

Additional Info:
LibreOffice version from the terminal: 26.2.6.3 620(Build:3)
Operating system: Fedora 44
Desktop/session: GNOME on Wayland (XDG_SESSION_TYPE=wayland)

The issue persists in Safe Mode and when launching with SAL_USE_VCLPLUGIN=gen. Toggling hardware acceleration and changing whether the Writer window is maximized did not resolve it.

I tested Safe Mode and resetting my user profile completely. I have not yet tested an Xorg session.
