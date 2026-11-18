# Text context menu appears behind rename popover when right-clicking filename

Source: https://gitlab.gnome.org/GNOME/nautilus/-/issues/4356  (reporter: envious8016 (@envious8016), filed 2026-10-23)

### Title

**Text context menu appears behind rename popover when right-clicking filename**

### Description

When renaming a file or folder in Nautilus, right-clicking inside the editable filename field opens the text context menu (Cut / Copy / Paste, etc.) behind the rename popover.

As a result, the context menu is obscured and cannot be accessed normally.

### Steps to reproduce

1. Open Nautilus.
2. Select any file or folder.
3. Press `F2` or choose **Rename** from the context menu.
4. While the filename is editable, right-click inside the filename text field.
5. Observe the position of the text context menu.

### Actual result

The Cut / Copy / Paste context menu is displayed behind the rename popover.

Its options are therefore hidden or inaccessible.

### Expected result

The text context menu should be displayed above the rename popover and should remain fully visible and interactive.

### Environment

* Fedora Linux 44 (Forty Four)
* GNOME Shell 50.6
* Nautilus 50.4
* Display server: Wayland

### Additional information

The issue specifically affects the mouse context menu while editing a filename during a rename operation.

Keyboard shortcuts such as `Ctrl+C`, `Ctrl+X`, and `Ctrl+V` are not the issue; the problem concerns the visual stacking and accessibility of the right-click text context menu.

Here's a small screen cast video showing the issue.

[attachment: recording.mp4]
