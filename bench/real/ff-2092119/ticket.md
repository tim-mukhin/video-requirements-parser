# mini-window crop function does not focus correctly

Source: https://bugzilla.mozilla.org/show_bug.cgi?id=2092119  (reporter: <email>, filed 2026-11-12)

[attachment: recording.mp4]
Firefox bug.mp4

User Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:160.0) Gecko/20100101 Firefox/160.0

### Steps to reproduce

Open a webpage e.g en.wikipedia.org, monkeytype.com  (shown in example, but could be any)
-select miniwindow option in right click menu
-in crop mode, select a region of the webpage to send to a miniwindow
-click send to miniwindow

### Actual results

Expected behaviour: In the cropping mode, selecting a region of the webpage will instantiate a miniwindow which contains that region of the page, nothing else

### Expected results

Actual behaviour: In the cropping mode, selection a region of the webpage instantiates a miniwindow containing the entire page, which can be scrolled up and down.
