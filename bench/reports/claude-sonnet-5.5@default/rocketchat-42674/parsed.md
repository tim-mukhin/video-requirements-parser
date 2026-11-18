# real/rocketchat-42674

_claude-sonnet-5.5@default, 26 s; looked at: frames/000489.jpg, frames/000821.jpg, frames/001270.jpg, frames/000046.jpg_

In the Rocket.Chat emoji picker, hovering an emoji often shows its name tooltip in the wrong place. It sits at the top-left of the page, over the 'Enter your E2E password' banner, instead of next to the emoji. Several tooltips also flash for under a second. Speech is a single 'Thank you.' and says nothing about the problem.

## Emoji picker tooltip is positioned at the top-left of the page (over the E2E banner) instead of next to the hovered emoji

Class: **wrong-data**

Environment: Brave browser on Windows, open.rocket.chat/channel/sandbox, dark theme. The emoji picker is open from the composer. A Notepad window opens in front at 00:22. A banner reading 'Enter your E2E password' stays visible throughout.

Steps:

1. Open the emoji picker in #sandbox. The opening click is not visible in the timeline, but the picker is already open at video start (Smileys & People section). (00:00.2; p001, p002)
2. Move the cursor over emojis in the grid. A tooltip such as ':upside_down:' or ':melting_face:' flashes for under a second. (00:01.6; p011, p013, p016)
3. Keep hovering and clicking emojis (for example the eye_in_speech_bubble emoji at 00:27). The tooltip ':eye_in_speech_bubble:' renders at the top-left of the page, overlapping the 'Enter your E2E password' text, far from the cursor. It is mixed with the banner text in OCR ('Entpreyewr 5a5nassword'). (00:27.3; p227, p228, p230, p231, p232)
4. Hover emojis near the left edge of the grid (for example at x≈651, y≈422–425). Tooltips ':speech_left:' and ':heart_hands:' again show over the banner at top-left. The banner text is overwritten and then restored when the tooltip goes away. (00:30.7; p233, p236, p237, p241, p249, p252)
5. Hover another emoji (':call_me:'). The tooltip appears at top-left over the banner and also next to the cursor at the same time. (00:41.8; p291, p292, p296, p297)

Expected (implied): The emoji name tooltip appears right next to the hovered emoji (and is not drawn over unrelated page content such as the E2E banner).

Actual: Tooltips are drawn at the top-left of the viewport, covering the 'Enter your E2E password' banner, away from the hovered emoji. Many also appear only briefly. At the end of the video a tooltip is correctly beside the cursor (frames/001270.jpg) at the same moment another is still at the top-left, so placement is inconsistent.

Key events: p228, p230, p231, p232, p236, p237, p252, p292, p297

Missed by the author:

- The tooltip is drawn over the E2E banner at the top-left of the page rather than beside the emoji (p228, p231, p236, p252, p292; frames/000821.jpg, frames/001270.jpg).
- Tooltips flash for 0.1–0.9 s, so some are barely visible (p003, p013, p033, p065).
- During the clicks the emoji picker stays open and the composer shows no inserted emoji ('Message #sandbox' is empty in frames/001270.jpg).

Claims:

- "The single utterance 'Thank you.' is a speech-recognition result and not a bug claim." [u002]: not shown - The author does not describe the problem; the bug is inferred from the screen only.
