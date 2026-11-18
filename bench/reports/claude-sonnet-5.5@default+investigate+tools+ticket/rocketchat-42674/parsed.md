# real/rocketchat-42674

_claude-sonnet-5.5@default, 31 s; looked at: frames/0028.0.jpg, frames/0025.5.jpg, frames/0020.5.jpg_

With the emoji picker open, the user clicked Notepad in the taskbar and moved the pointer back over the picker without clicking Rocket.Chat. Some emoji-name tooltips then appeared at the page's top-left corner, over the E2E banner, instead of next to the hovered emoji. Others, such as :white_heart:, still appeared in the right place.

## Emoji picker tooltips render at page top-left after focus moves to another app and the pointer returns without a click

Class: **wrong-data**

Environment: Brave on Windows 11 (taskbar visible), open.rocket.chat/channel/sandbox, dark theme, emoji picker open from the composer (Smileys & People). Notepad (Windows 11) overlaps the right side. The browser and server versions, Chrome and localhost are not visible in the video.

Steps:

1. Open the composer emoji picker in #sandbox and hover emojis. Tooltips and the preview panel appear next to the pointer (e.g. :palm_down_hand: at 20.0 s, correctly placed). (00:20.0; p176, p179)
2. Click the Notepad icon in the taskbar (cursor at 1209,1112). Notepad opens in front while the picker stays open, and the picker search loses its focus ring. (00:22.7; p185, p186, p187)
3. Move the pointer back over the picker without clicking Rocket.Chat and hover :white_heart:. Its tooltip is placed correctly, though greyed. (00:25.3; p213, p214)
4. Hover :eye_in_speech_bubble:. A white tooltip appears at the page's top-left over the 'Enter your E2E password' banner. This is the first misplaced tooltip, and the correct one beside the emoji is also shown. (00:27.3; p228, p229, p230, p231)
5. Repeat on other emojis: :speech_left:, :heart_hands:, :point_up_2:, :point_left: (about 39.8 s) and :call_me:. Each draws at the top-left again, the banner text being overwritten. Rocket.Chat is never clicked. (00:30.7; p236, p237, p249, p252, p273, p282, p292)

Expected (implied): Each tooltip appears next to the hovered emoji, as it did before the focus switch.

Actual: After focus moved to Notepad, some tooltips are drawn in the page's top-left corner, far from the hovered emoji. The correct tooltip is sometimes shown beside the emoji as well (28.0 s frame). The tooltip text is right and the preview panel still updates. In the video the tooltip is repositioned as the pointer moves between emojis (p243, p257, p277).

Key events: p186, p228, p230, p232, p237, p252, p273, p282, p292

Missed by the author:

- The correct tooltip stays beside the emoji at the same time as the misplaced one (frame 28.0 s), so a duplicate or stale tooltip is involved.
- The :white_heart: tooltip is greyed at 25.5 s while later ones are white, which suggests a different tooltip state after focus loss (p214).
- The misplaced tooltip hides the E2E banner text (p230, p237, p252, p273).

Claims:

- "Tooltips initially appear near the emojis" [ticket]: confirmed - Before Notepad (e.g. :palm_down_hand: at 20.0 s) tooltips are next to the pointer.
- "After clicking another app and moving back, some tooltips appear at top-left" [ticket]: confirmed - Seen from 27.3 s on, with OCR of the E2E banner text overwritten by the tooltip name.
- "Only some emojis are affected" [ticket]: confirmed - In the ones checked, :white_heart: (25.3 s) was placed correctly. Later hovers were misplaced.
- "Rocket.Chat was not clicked or refocused" [ticket]: confirmed - Notepad stays in front. No click on the page is seen up to the end of cursor tracking (44.2 s). The final 1.5 s are not tracked.
- "The Notepad click is a real click" [ticket]: confirmed - CLICK at the taskbar [1209,1112] at 22.7 s, followed by Notepad appearing.
- "Moving the pointer slightly repositions the tooltip" [ticket]: not shown - The video shows tooltips moving back to normal as the pointer moves to another emoji, but not a deliberate nudge.
- "Clicking inside Rocket.Chat restores normal behaviour; Alt+Tab does not reproduce it" [ticket]: not shown - No click back into Rocket.Chat and no Alt+Tab appear.
- "Also reproduced in Chrome and on localhost, with no console errors" [ticket]: not shown - Only Brave on open.rocket.chat is recorded. The console is not shown.
