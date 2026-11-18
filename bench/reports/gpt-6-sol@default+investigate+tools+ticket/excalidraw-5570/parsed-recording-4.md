# real/excalidraw-5570

_gpt-6-sol@default, 46 s; looked at: frames/moments/p004.jpg, frames/moments/p006.jpg, frames/0002.5.jpg, frames/0003.0.jpg, frames/0004.0.jpg, frames/0005.0.jpg, frames/000055.jpg, frames/000108.jpg, frames/000372.jpg, frames/moments/p009.jpg, frames/moments/p048.jpg, frames/0010.0.jpg, frames/000067.jpg, frames/000320.jpg, frames/0003.5.jpg, frames/0004.5.jpg_

In the recorded mobile browser session, a selected rectangle's context menu repeatedly closes and reopens, with a slight change in position between openings. This makes the menu appear unstable, but the recording shows no touch gestures, so it cannot establish whether scrolling failed or what caused each closure.

## Rectangle context menu repeatedly closes and reopens on mobile

Class: **intermittent**

Environment: excalidraw.com in a portrait mobile browser. This clip does not identify the device or browser version; the ticket identifies a different recording as Pixel 4A with Chrome 104.0.5112.69.

Steps:

1. Select the rectangle near the bottom of the canvas (the trigger is not visible). (00:01.7; p001)
2. Open its context menu (the trigger is not visible). (00:02.2; p003)
3. Observe the menu close and then reopen; this pattern repeats during the recording, though the intervening gestures are not visible. (00:03.2; p005, p008, p010, p013)

Expected (implied): The context menu remains usable without unexpectedly closing or changing position during interaction.

Actual: The menu is visible at 2.2 s, absent at 3.2 s, and visible again at 4.4 s; similar cycles follow. Its horizontal position differs slightly between some openings. No attempted scroll or menu selection is visible.

Key events: p003, p004, p005, p008, p010, p013, p031, p037, p047, p049

Missed by the author:

- The menu disappears altogether between openings, rather than only shifting position [p003, p005, p008]. The timeline and sampled frames agree.
- Selection handles also disappear on some closures and return before the next menu opening [p005, p008]. The frames settle this; the timeline's changing menu text alone does not.
- The brief 'Press Enter to add text' message is a tooltip change, not evidence that text was entered [p004]. Its moment frames settle the short event.

Claims:

- "The context menu is displayed, then repositioned." [ticket]: confirmed - Frames show slightly different positions across openings, but do not establish repositioning while one opening remains visible.
- "Context-menu scrolling does not work consistently." [ticket]: not shown - No touch path is visible, so an attempted scroll cannot be identified.
- "The issue occurs on Pixel 4A with Chrome 104.0.5112.69 but not on the other named devices." [ticket]: not shown - This clip shows one browser session without a verifiable device, version, or comparison; the ticket associates the Pixel 4A claim with another recording.
