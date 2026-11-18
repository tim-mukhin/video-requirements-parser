# Calendar widget: day loses focus when changing month

Source: https://gitlab.gnome.org/GNOME/gnome-shell/-/issues/7372  (reporter: Lorenzo Ubaldi (@nokse22), filed 2024-02-03)

### Affected version

Gnome 45.3 on Fedora 39 with Wayland

### Bug summary

When navigating the days in the calendar with the keyboard I can press enter to select a day, but if I select a day that is not in the currently viewed month it has to switch month, but the focus is lost (it should be on the just selected day) and it is given to the panel widget.

### Steps to reproduce

1. open calendar/notifications widget
2. click on a day
3. using keyboard select a day of the next/previous month (the dimmed ones) and press enter

### What happened

The focus will be on the panel widget and if you try to move left or right you will select the activities or the quick menu.

Same thing happens if you click on one of the dimmed days with the cursor.

### What did you expect to happen

The focus should be on the selected day.

### Relevant logs, screenshots, screencasts etc.

Looks like it has focus for a brief time, then loses it when the events dots are loaded.

If there are no events to load it works properly.

[attachment: recording.webm]
