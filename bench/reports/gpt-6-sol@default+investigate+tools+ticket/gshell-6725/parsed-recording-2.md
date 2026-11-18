# real/gshell-6725

_gpt-6-sol@default, 51 s; looked at: frames/0002.0.jpg, frames/0002.5.jpg, frames/0003.0.jpg, frames/000077.jpg, frames/0001.5.jpg, frames/0001.0.jpg, looks/0001.85-0002.45-860_70_2120_460/sheet.jpg, looks/0001.85-0002.45-860_70_2120_460/002.413.jpg, looks/0001.85-0002.45-860_70_2120_460/002.312.jpg, looks/0002.42-0002.54-860_70_2120_460/sheet.jpg_

GNOME search visibly updates from Celluloid to Calculator as the selected result, but launching the search opens Celluloid. This can start a different application from the one shown as selected.

## Search opens Celluloid after Calculator becomes the selected result

Class: **wrong-data**

Environment: GNOME Shell Activities search; Celluloid and Calculator are visible. The ticket reports GNOME Shell 44.1 on Fedora Silverblue 38.20230509.0 with Wayland, but the recording does not verify those details.

Steps:

1. Open the Activities overview (the trigger is not visible). (00:00.9; p001)
2. Enter “c”; Celluloid becomes the selected search result. The keystroke is not visible. (00:01.4; p002, p003)
3. Extend the query to “cal” and submit it quickly. Calculator is selected by 2.413 s; the submission key is not visible. (00:02.4; p003, p004)

Expected (implied): Submitting the search should open the visibly selected result, Calculator.

Actual: Calculator is highlighted immediately before the overview closes, but Celluloid opens at about 2.5–2.8 s. The last visible query is “cal”, not “calc”.

Key events: p003, p004, p005

Missed by the author:

- The last visible query is “cal”, not the reported “calc” [p003, p004].

Claims:

- "Calculator is selected before Celluloid opens." [ticket: The search results correctly show Calculator as the selected search result]: confirmed - The intervening video frames show Calculator highlighted at 2.346–2.413 s; the half-second sample and parser timeline miss this update.
- "The search bar shows “calc” before submission." [ticket: The search bar correctly shows "calc" as my search term]: refuted - The last visible search frame, at 2.413 s, shows “cal”.
- "Pressing Enter opens Celluloid." [ticket: when I press the Enter key, Celluloid still opens]: confirmed - Celluloid opens, although the recording does not show which key or other input submitted the search.
- "The issue happens often and was absent on Fedora Silverblue 36." [ticket: This is very easily reproducible for me; I did not experience this bug when using Fedora Silverblue 36]: not shown - This recording shows one attempt and no earlier system.
