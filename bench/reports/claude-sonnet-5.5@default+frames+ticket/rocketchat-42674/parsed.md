# real/rocketchat-42674

_claude-sonnet-5.5@default, 30 s; looked at: frames, frames/0000.0.jpg, frames/0010.0.jpg, frames/0020.0.jpg, frames/0030.0.jpg, frames/0040.0.jpg, frames/0023.0.jpg, frames/0026.0.jpg, frames/0028.0.jpg, frames/0045.0.jpg_

With the emoji picker open, the user switches to Notepad, which opens over the page. After the pointer returns to the Rocket.Chat page without a click, some emoji-name tooltips (for example :eye_in_speech_bubble:, :point_left:, :call_me:) appear in the page's top-left corner instead of next to the hovered emoji. One tooltip, :white_heart:, still appears in the right place. The tooltip text is shown, but in the wrong place.

## Emoji picker tooltips render at page top-left after another app was clicked and the pointer returns without clicking Rocket.Chat

Class: **wrong-data**

Environment: Brave on Windows 11 (taskbar and clock are visible). open.rocket.chat/channel/sandbox, dark theme. Emoji picker open from the composer. Notepad (Windows 11 version) overlaps the right side of the window. The Brave version, server version and Chrome repro in the ticket are not visible in the video.

Steps:

1. Open the composer emoji picker in #sandbox. Hover emojis (the Frequently used and Smileys groups, then the people/body group). Tooltips and the preview panel appear normally near the pointer. (00:00.0; 0000.0, 0010.0, 0020.0)
2. Switch to Notepad, which opens over the right part of the screen while the picker stays open. The Notepad click is inferred: Notepad is in the foreground and the picker search box has lost its focus ring. (00:23.0; 0023.0)
3. Move the pointer back over the picker without clicking Rocket.Chat and hover an emoji. The :white_heart: tooltip is still positioned correctly, above the emoji. (00:26.0; 0026.0)
4. Hover other emojis. The :eye_in_speech_bubble: tooltip appears at the top-left of the page, over the 'Enter your E2E password' banner. A second, correctly placed tooltip is also visible next to the emoji. (00:28.0; 0028.0, 0030.0)
5. Hovering :point_left: and :call_me: also puts a white tooltip at the top-left. Rocket.Chat is never clicked and Notepad stays in front. (00:40.0; 0040.0, 0045.0)

Expected (implied): Each emoji tooltip appears next to the hovered emoji, as it did before switching to the other application.

Actual: After the focus switch, some tooltips are drawn at the top-left corner of the page, far from the hovered emoji. The preview panel at the bottom of the picker still updates correctly.

Key events: 0026.0, 0028.0, 0030.0, 0045.0

Missed by the author:

- The correctly placed tooltip stays on screen next to the emoji at the same time as the misplaced top-left one (0028.0), so a stale or duplicate tooltip may be involved.
- The picker search box loses its focus ring once Notepad takes focus (0023.0 and later), which matches the page having lost focus.

Claims:

- "Tooltips initially appear near the emojis" [Hover over emojis. Their tooltips initially appear near them.]: confirmed - The :white_heart: tooltip at 0026.0 and the preview panel at 0010.0 and 0020.0 are correct. No tooltip is shown near the pointer at 0000.0, 0010.0 or 0020.0.
- "After clicking another app and moving back, some tooltips appear at top-left" [The white emoji-name tooltip appears at the page's top-left]: confirmed - Shown at 0028.0, 0030.0, 0040.0 and 0045.0.
- "Only some emojis are affected" [This affects some emojis, not all.]: confirmed - :white_heart: at 0026.0 is placed correctly. The other tooltips seen after the switch are misplaced.
- "Rocket.Chat is not clicked or refocused" [without clicking or refocusing inside it]: confirmed - Notepad stays in front for the rest of the video and no click on the page is visible.
- "Moving the pointer slightly repositions the tooltip" [Moving the pointer slightly may reposition the current tooltip]: not shown - Not clearly shown. At 0028.0 a correct and a misplaced tooltip are visible together, but the video does not show a nudge fixing one.
- "Clicking inside Rocket.Chat restores normal behaviour, and Alt+Tab does not reproduce it" [Clicking inside Rocket.Chat restores normal behavior.]: not shown - The video never clicks back into Rocket.Chat and never uses Alt+Tab.
- "Reproduced on Chrome and localhost, with no console errors" [also reproduced in Google Chrome]: not shown - Only Brave on open.rocket.chat is recorded, and the console is not shown.
