# Custom shape range slider with tooltip causes range-thumb to flicker

Source: https://bugzilla.mozilla.org/show_bug.cgi?id=2092950  (reporter: <email>, filed 2026-11-14)

[attachment: recording.mp4]
Recording of the flicker

### Steps to reproduce

Here is the full demo: https://codepen.io/editor/t_afif/pen/01a150b9-e78d-71ee-9dea-3adfe3e18538

And a more simplified demo with only the needed CSS to reproduce the issue (the CSS related to Chromium is removed as well): https://codepen.io/t_afif/pen/YPZMPre/e69d82ea69d78d1c100535d34f625128

### Actual results

When you drag the thumb, you will notice some flickering. Attached is a recording showing the flicker that happens mostly on the right side (high values)

### Expected results

When trying to reduce the code, I noticed that the issue is not only related to the input. The output (the tooltip) needs to be present with the counter value to activate the flicker. It looks like a complex combination of different things that creates the bug.

PS: in case the attachment is not working, I shared it here: https://bsky.app/profile/css-only.dev/post/3n2bhf5pp7c2x
