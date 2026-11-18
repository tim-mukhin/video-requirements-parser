# real/vscode-337449

_claude-sonnet-5.5@default, 28 s; looked at: frames/moments/p001.jpg, looks/0000.10-0000.50-445_848_1570_723/sheet.jpg_

The cursor over editor text switches between the I-beam and the arrow. The parser counted 60 switches over 4.3 s from 0.1 s, 10 of them with the cursor standing still. The watcher missed this because its 0.5 s frame step is too coarse. It matches the ticket's flicker report, though in this video the shapes are I-beam and arrow rather than hand and arrow.

## Mouse cursor flickers between I-beam and arrow over editor text in VS Code on macOS

Class: **intermittent**

Environment: macOS, VS Code with workspace fitcity-flutter, main.dart open (tabs client_routes.dart, index.dart), Explorer on the left, iOS Simulator window at the right edge. Version 1.139.0 is stated in the ticket only; the video shows no version and does not show whether extensions are disabled. The recording has no audio.

Steps:

1. With main.dart open, move the mouse over the editor text. The cursor alternates between I-beam and arrow: 60 switches over 4.3 s, 10 of them while it was not moving. In the 0.1–0.5 s frames I looked at, it showed as an arrow in some frames and an I-beam in most others. (00:00.1; p001)
2. Hover deep_link_resolver.dart in the Explorer. The cursor is a hand for 0.9 s and the Explorer toolbar icons appear. (00:02.6; p018)
3. Click near the right screen edge at [2261, 980]. The click was inferred from the cursor stopping and the screen reacting. Focus then moves to the iOS Simulator. (00:05.0; p034)

Expected (implied): The cursor stays an I-beam over editor text and a hand over clickable items, and changes only when it moves onto a different kind of element.

Actual: Over the editor text the cursor shape alternates between I-beam and arrow, including while the mouse is still. The ticket says hand versus arrow over clickable items; the video shows the flicker on text only.

Key events: p001, p018, p034

Missed by the author:

- The flicker is over editor text, between I-beam and arrow, not over clickable elements (p001).
- Focus leaves VS Code for the iOS Simulator at the end of the video (p049, p051). This may be related to the cursor-shape handling.

Claims:

- "Cursor keeps flickering between the hand and the arrow over clickable elements" [ticket]: confirmed - A shape flicker is confirmed (p001), but the shapes are I-beam and arrow over editor text. The hand shown over deep_link_resolver.dart (p018) was stable.
- "It flickers even when the mouse is not moving" [ticket]: confirmed - The parser counted 10 of the 60 switches while the cursor did not move (p001).
- "It happens in the Activity Bar, Explorer, tabs and buttons" [ticket]: not shown - The cursor never visits the Activity Bar, tabs or buttons. Over the Explorer item it was a hand (p018), with no flicker seen.
- "It happens constantly" [ticket]: not shown - The video is 8 s. The flicker was detected in the first 4.3 s, over the editor only.
