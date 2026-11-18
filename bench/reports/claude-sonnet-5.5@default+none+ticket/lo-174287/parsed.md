# real/lo-174287

_claude-sonnet-5.5@default, 15 s; looked at: nothing_

In LibreOffice Writer on Fedora 44 (GNOME, Wayland), the Insert, Format and Styles menus sometimes fail to open from the menu bar, or open and close again straight away. This makes those menus hard to use. The reporter says it persists in Safe Mode, with a reset profile, with the gen VCL plugin, and regardless of hardware acceleration or window maximization.

## Writer Insert, Format and Styles menus close immediately when clicked with the mouse (Fedora 44, GNOME Wayland)

Class: **intermittent**

Environment: LibreOffice 26.2.6.3 620 (Build:3), Writer; Fedora 44, GNOME on Wayland (XDG_SESSION_TYPE=wayland). Not tested on Xorg. Other menus (e.g. File, Edit) are not mentioned.

Steps:

1. Open LibreOffice Writer. (00:00.0; )
2. Click Insert on the menu bar. (00:00.0; )
3. Repeat with Format and Styles. (00:00.0; )

Expected (speech): The selected menu stays open so the pointer can be moved into it and an item chosen.

Actual: The Insert, Format or Styles menu sometimes does not open, or appears briefly and then closes. Workaround: open a menu farther left or right, then move the pointer across the menu bar with that menu open. The reporter calls this unreliable.

Key events: 

Claims:

- "Issue persists in Safe Mode" [The issue persists in LibreOffice Safe Mode]: not shown - Ticket only; no video or logs to check.
- "Issue persists after a profile reset" [After resetting my user profile]: not shown - Ticket only.
- "Issue persists with SAL_USE_VCLPLUGIN=gen" [When launching with SAL_USE_VCLPLUGIN=gen]: not shown - Ticket only.
- "Reproducible: Always" [Reproducible: Always]: not shown - Contradicts the description's 'sometimes' and 'may fail', so reproducibility is unclear.
