# real/vscode-337449

_gpt-6-sol@default, 52 s; looked at: frames/moments/p001.jpg, frames/moments/p024.jpg, frames/moments/p025.jpg, frames/0003.0.jpg, frames/0005.0.jpg, frames/moments/p032.jpg, frames/moments/p051.jpg, looks/0002.70-0003.20-415_885_170_100/sheet.jpg, frames/0000.5.jpg, frames/0001.5.jpg, frames/0004.0.jpg, looks/0003.80-0004.10-1570_1050_250_180/sheet.jpg_

The timeline detects rapid arrow/I-beam cursor changes in the VS Code editor, including changes while the cursor was tracked as stationary. This supports a cursor-flicker issue that the watcher's half-second frames missed, but the video does not establish the ticket's more specific claim of hand-to-arrow flicker while stationary over clickable controls.

## Cursor rapidly changes shape in the VS Code editor

Class: **intermittent**

Environment: VS Code on macOS, with the fitcity-flutter workspace and main.dart open; an iPhone 17 Pro simulator is beside it. The ticket states VS Code 1.139.0, but the version is not shown.

Steps:

1. Click in main.dart, then move the cursor across the editor and pause; the timeline detects repeated arrow/I-beam changes, including while tracked as stationary. (00:00.4; p005, p001)

Expected (implied): The cursor should retain the shape appropriate to the area beneath it while stationary.

Actual: The timeline records 60 arrow/I-beam changes over 4.3 seconds, 10 while it tracked no movement [p001]. Enlarged consecutive frames show arrow and I-beam states in the editor; they do not establish stationary hand-to-arrow flicker over a clickable control. A hand remains visible during the checked Explorer-file hover [p018].

Key events: p001, p005, p018

Missed by the author:

- The timeline detects arrow/I-beam changes rather than the reported hand/arrow changes [p001]; its short-event evidence settles what the watcher's half-second samples could not.
- During the checked hover over deep_link_resolver.dart, the cursor appears as a hand [p018]. The brief Explorer toolbar-icon changes coincide with hover changes, not a demonstrated control failure [p019, p025].
- The ticket's extension-disabled question is unanswered, and no such test is shown.

Claims:

- "The cursor flickers between a hand and an arrow while stationary over clickable elements." [ticket.md]: not shown - The detected rapid changes are arrow/I-beam changes. The checked Explorer hover shows a hand, not a stationary hand-to-arrow alternation.
- "Flickering occurs throughout the Activity Bar, Explorer, tabs and buttons." [ticket.md]: not shown - The rapid changes are detected in the editor; the video does not establish flicker in every named area.
- "This happens constantly." [ticket.md]: not shown - The recording is eight seconds long and cannot establish how often it happens outside it.
