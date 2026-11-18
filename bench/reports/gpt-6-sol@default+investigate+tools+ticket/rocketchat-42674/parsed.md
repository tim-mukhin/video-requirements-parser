# real/rocketchat-42674

_gpt-6-sol@default, 72 s; looked at: frames/0021.5.jpg, frames/0022.5.jpg, frames/0025.5.jpg, frames/0027.5.jpg, frames/0028.5.jpg, frames/moments/p217.jpg, frames/moments/p224.jpg, frames/moments/p234.jpg, frames/0025.0.jpg, frames/0026.0.jpg, frames/0026.5.jpg, frames/0030.5.jpg, frames/0031.5.jpg, frames/0034.5.jpg, frames/0038.5.jpg, frames/moments/p003.jpg, frames/0005.5.jpg, frames/0028.0.jpg, frames/0032.0.jpg, frames/0033.5.jpg, frames/0042.5.jpg_

With Notepad in front of Brave, hovering over Rocket.Chat's exposed emoji picker can place an emoji-name tooltip at the page's top-left instead of beside the emoji. The frames confirm the misplaced label identified by the watcher; the timeline identifies the taskbar click and the hover that preceded it.

## Emoji tooltip appears at page top-left when hovering over picker behind Notepad

Class: **intermittent**

Environment: Brave at open.rocket.chat/channel/sandbox on Windows, with Notepad in front. The ticket reports Windows 11, Brave 1.96.61 and Rocket.Chat Server 8.10; those versions are not visible in the video.

Steps:

1. In #sandbox, leave the composer emoji picker open. (00:01.5; p009)
2. Click the Notepad taskbar icon, leaving the picker exposed behind the Notepad window. (00:22.7; p186, p187)
3. Without refocusing Brave, move the pointer over the picker and hover the eye-in-speech-bubble emoji. (00:27.3; p228, p229, p231)

Expected (implied): The emoji-name tooltip appears beside the hovered emoji.

Actual: At 27.6 seconds, the white :eye_in_speech_bubble: tooltip appears at the page's top-left. At 28.5 seconds, it remains there while a second, dark tooltip appears beside the hovered emoji. Earlier, :white_heart: displayed its tooltip near the emoji with Notepad still in front.

Key events: p186, p187, p214, p216, p228, p231

Missed by the author:

- At 28.5 seconds, a dark tooltip appears beside the emoji while the misplaced white tooltip remains at the top-left [p228, p231].
- The picker remains responsive behind Notepad: its footer changes to the hovered emoji's name [p214, p228].

Claims:

- "Hovering over the picker after clicking another application can put a tooltip at the page's top-left." [ticket: Description]: confirmed - Notepad comes to the front after the taskbar click [p186, p187]; the eye-in-speech-bubble tooltip then appears at the page's top-left [p228, p231].
- "This affects some emojis, not all." [ticket: Actual behavior]: confirmed - In the hovers checked, white heart has a nearby tooltip [p214, p216], whereas eye-in-speech-bubble has a top-left tooltip [p228, p231]. This does not establish a fixed set of affected emojis.
- "Moving the pointer slightly may reposition the current tooltip; clicking inside Rocket.Chat restores normal behavior." [ticket: Additional context]: not shown - A nearby dark tooltip appears, but the misplaced white one remains. The recording does not demonstrate a click that refocuses Rocket.Chat after the failure.
- "The issue also reproduces in Chrome, on localhost and with two monitors; Alt+Tab did not reproduce it." [ticket: Client Setup Information and Additional context]: not shown - The recording shows Brave and Notepad on one display, not those other tests.
- "No new browser console errors appeared." [ticket: Relevant logs]: not shown - The browser console is not visible.
