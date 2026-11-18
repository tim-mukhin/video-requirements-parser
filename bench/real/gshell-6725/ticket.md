# Search opens incorrect result when typing quickly

Source: https://gitlab.gnome.org/GNOME/gnome-shell/-/issues/6725  (reporter: Chris Tucker (@christucker), filed 2023-05-27)

### Affected version

* GNOME Shell: 44.1
* Fedora Silverblue: 38.20230509.0
* Wayland

**I did not experience this bug when using Fedora Silverblue 36, which I believe was running GNOME 42.**

### Bug summary

When performing a search by typing on the keyboard quickly, GNOME very often opens the incorrect search result.

For example, if I type "c", I get Celluloid appearing as the first/selcted search result. When I add "alc" to search for "calc", the search bar correctly shows "calc" as my search term, and the search results correctly show Calculator as the selected search result — but when I press the Enter key, Celluloid still opens!

Visually everything is shown correctly, but when actually pressing the Enter key opens the previously-shown result. It's like GNOME is delayed and acting on the older search results, which are not in sync with what is shown visually.

This is very easily reproducible for me, and happens often enough to be frustrating. I have to intentionally slow down when doing a search to make sure GNOME opens the right thing.

### Steps to reproduce

Either:

1. Open the Overview screen.
2. Type one letter of the search term and view the search results.
3. Quickly type the rest of the search term (to change the results) and press Enter.

Or:

1. Open the Overview screen.
2. Quickly type a search term and press Enter.

### What happened

GNOME opens the wrong program. The selected search result shown on-screen does not match the application that is opened.

### What did you expect to happen

I expected GNOME to open the result that was shown on-screen as selected. With Calculator shown as the selected search result, I expected Calculator to be opened, not Celluloid.

### Relevant logs, screenshots, screencasts etc.

[attachment: recording-1.webm]

[attachment: recording-2.webm]

Recordings: in the opening post: recording-1.webm, recording-2.webm.
