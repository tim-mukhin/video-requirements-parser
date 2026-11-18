# real/rocketchat-42674

_claude-sonnet-5.5@default, 15 s; looked at: nothing_

After the composer emoji picker is opened and another application such as Notepad is clicked, hovering emojis in Rocket.Chat without clicking back in sometimes shows the tooltip at the page's top-left instead of near the emoji. It is a cosmetic problem, but it makes the tooltips misleading and hard to use. Clicking inside Rocket.Chat restores normal behavior.

## Some emoji picker tooltips appear at top-left after focus moves to another application

Class: **wrong-data**

Environment: Rocket.Chat Server 8.10 on open.rocket.chat and localhost. Brave 1.96.61 and Google Chrome 154.0.8037.99 (64-bit), Windows 11. Notepad was the other application. The ticket gives no account or organization.

Steps:

1. Open a conversation and the composer emoji picker. (00:00.0; )
2. Hover over emojis. Their tooltips initially appear near them. (00:00.0; )
3. Leave the picker open and click another application, such as Notepad. (00:00.0; )
4. Move the pointer back over the picker without clicking Rocket.Chat. (00:00.0; )
5. Hover over different emojis. (00:00.0; )

Expected (speech): The tooltip appears near the hovered emoji.

Actual: For some emojis, not all, the white emoji-name tooltip appears at the page's top-left instead of near the hovered emoji. Moving the pointer slightly may reposition the current tooltip, but the problem can recur on other emojis. Clicking inside Rocket.Chat restores normal behavior. No new console errors.

Key events: 

Claims:

- "Alt+Tab did not reproduce it in an earlier test." [Alt+Tab did not reproduce it in an earlier test.]: not shown - No video; the ticket only reports this, and it is not clear how reliable the test was.
- "It reproduces with Notepad on the same display, and a second monitor is not required." [I reproduced it with Rocket.Chat and Notepad on the same display.]: not shown - No video was available to check this.
- **R1** [stated] Emoji picker tooltips must be positioned near the hovered emoji even when the browser window has lost focus and the pointer re-enters without a click. - Expected behavior section of the ticket
