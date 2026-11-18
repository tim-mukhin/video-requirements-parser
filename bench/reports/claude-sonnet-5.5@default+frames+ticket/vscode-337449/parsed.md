# real/vscode-337449

_claude-sonnet-5.5@default, 27 s; looked at: frames, frames/0000.0.jpg, frames/0002.0.jpg, frames/0004.0.jpg, frames/0006.0.jpg, frames/0007.5.jpg, frames/0001.0.jpg, frames/0003.0.jpg, frames/0005.0.jpg_

The 7.9 s recording shows VS Code (Flutter project, main.dart) with the mouse moving across the editor, the Explorer and onto an iOS Simulator window. The reported pointer/arrow flicker cannot be confirmed: the frames, taken every 0.5 s, show the cursor with the correct shape every time. The report is likely an intermittent cursor-shape bug that this sampling cannot capture.

## Mouse cursor reportedly flickers between pointer and arrow over clickable elements (not visible in sampled frames)

Class: **intermittent**

Environment: macOS, VS Code (ticket says 1.139.0; no version is visible in the video). Workspace 'fitcity-flutter', main.dart open with client_routes.dart and index.dart tabs. Status bar shows 'iPhone 17 Pro (ios simulator)'. An iOS Simulator window sits at the right edge of the screen. Whether extensions are disabled is not shown; the ticket leaves that question unanswered.

Steps:

1. Start with the I-beam cursor over the editor text; main.dart is open and the caret is at Ln 34 (inferred click in the editor between 0.0 s and 2.0 s). (00:01.0; 0001.0, 0002.0)
2. Move the mouse into the Explorer and hover deep_link_resolver.dart. The cursor is a hand (pointer) and the Explorer toolbar icons appear, as expected for a clickable item. (00:03.0; 0003.0)
3. Move the mouse out of the VS Code window to the right, over the iOS Simulator. The cursor is an arrow. At 6.0 s VS Code's window controls are greyed out because the Simulator has focus. (00:05.0; 0005.0, 0006.0, 0007.5)

Expected (implied): The cursor stays a hand over clickable elements while the mouse is still, and changes only when it moves onto a different kind of element.

Actual: In every sampled frame the cursor matches what is under it: I-beam over text, hand over the Explorer item, arrow outside the window. No flicker shows in the 16 frames, and the mouse is never held still over a clickable element, so the 'even when the mouse is not moving' claim is not tested.

Key events: 0003.0, 0005.0

Missed by the author:

- The recording ends with the cursor over an iOS Simulator window and focus leaving VS Code (0006.0, 0007.5). A second app taking focus could be related.
- The ticket leaves the 'all extensions disabled' question as 'Yes/No', so it was never answered.

Claims:

- "Cursor flickers between hand and arrow over clickable elements anywhere in VS Code" [The mouse cursor keeps flickering between the hand (pointer) and the default arrow]: not shown - The 0.5 s sampling shows only correct cursor shapes. A flicker faster than the frame step would not be captured.
- "Flicker happens even when the mouse is not moving" [even when the mouse is not moving]: not shown - The mouse moves in nearly every frame. The only hover on a clickable item is the single frame at 3.0 s.
- "Happens in the Activity Bar, tabs and buttons" [Activity Bar, Explorer, tabs, buttons, etc.]: not shown - The cursor never visits the Activity Bar, tabs or buttons in the video.
