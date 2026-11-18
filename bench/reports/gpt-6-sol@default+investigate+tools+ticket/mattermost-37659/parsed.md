# real/mattermost-37659

_gpt-6-sol@default, 51 s; looked at: frames/0007.5.jpg, frames/0011.5.jpg, frames/0012.0.jpg, frames/0015.5.jpg, frames/moments/p137.jpg, frames/moments/p161.jpg, frames/moments/p193.jpg, frames/moments/p383.jpg, frames/moments/p231.jpg, frames/moments/p094.jpg, frames/0000.0.jpg, frames/0022.0.jpg, frames/0028.0.jpg, frames/0030.0.jpg, frames/0017.5.jpg, frames/0018.0.jpg, frames/moments/p016.jpg, frames/moments/p040.jpg, frames/moments/p050.jpg, frames/moments/p065.jpg, frames/moments/p105.jpg, frames/moments/p248.jpg, frames/0008.5.jpg, frames/0010.5.jpg_

The recording shows Mattermost channel history changing direction and revisiting image posts, but it does not establish the reported skipped messages. The scroll input is not visible, and the blurred message text prevents checking for gaps; an unintended position jump remains a possible issue rather than a confirmed one.

## Possible intermittent jump while scrolling channel history

Class: **intermittent**

Environment: A Mattermost channel in a desktop window with a Windows taskbar visible. The ticket reports Desktop 6.2.2, server 11.7.2, and a Chrome 144 reproduction; the recording does not verify those versions or show Chrome.

Steps:

1. Start in the already-open channel and scroll through its history; the input itself is not visible. (00:01.9; p022)
2. Continue through the image posts and table, then scroll back through that portion of the history. (00:09.8; p094, p105, p137, p161)

Expected (implied): Older messages remain in continuous chronological order without skipped posts or unexpected changes in scroll position.

Actual: A white image with a blue card is visible around 7.5 seconds and again around 12 seconds. The timeline records content moving up at 9.8–11.9 seconds and down at 13.5 seconds, so the revisited image alone does not prove an unintended jump. Short-frame strips show additional position shifts at 17.5 and 28.4 seconds, but do not distinguish them from scrolling. No specific missing message can be identified.

Key events: p094, p105, p137, p161, p231, p383

Missed by the author:

- The frames show the blue-card image twice, while the timeline records scroll movement reversing direction around those appearances [p094, p137, p161]. Together, they limit the first reader's interpretation of the repeat as an unexpected jump.
- The moment strips show brief position shifts at 17.5 and 28.4 seconds that the half-second frames can miss, but neither establishes skipped messages [p231, p383].

Claims:

- "Scrolling intermittently jumps backward unexpectedly." [ticket.md]: not shown - The timeline confirms changes in scroll direction, and the frames confirm a revisited image, but the user's scroll input is not visible. The moment strips do not establish that a position change was unsolicited.
- "Several messages are skipped before older messages appear." [ticket.md]: not shown - Message text and timestamps are too blurred to identify a missing post or verify a gap.
- "The issue also reproduces in Chrome 144 with the listed desktop and server versions." [ticket.md]: not shown - The recording shows one Mattermost window, without a Chrome reproduction or legible version information.
