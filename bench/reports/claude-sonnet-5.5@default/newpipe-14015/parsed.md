# real/newpipe-14015

_claude-sonnet-5.5@default, 25 s; looked at: frames/000220.jpg, frames/000260.jpg, frames/000350.jpg, frames/000444.jpg_

On a phone, a YouTube video is shared to NewPipe and opened in NewPipe's player with the "Always" option on the app chooser. The only speech is an unrelated channel-subscribe phrase, so the author states no problem. The screen shows nothing that visibly fails, so the defect cannot be determined; the autoplay/queue area is the most likely candidate.

## Unclear: NewPipe opened from YouTube; no failure stated or clearly visible (autoplay/queue area is the candidate)

Class: **silent-fail**

Environment: Android phone, portrait, screen recorded with Mobizen (Vietnamese UI). YouTube app, its share/long-press menu, then the NewPipe app: opens from a chooser, shows a red splash screen, then the video page with Add / Background / Popup / Download buttons and an autoplay toggle ("Tự động thêm vào hàng đợi"). Battery 80%, clock 07:32–07:33.

Steps:

1. On the YouTube home feed, open a video's menu. It lists Save to Watch later, Save to playlist, Download video, Share, and others. The tap that opens it is not visible. (00:01.9; p006)
2. In the share sheet (Facebook, Bluetooth, Messages, Copy link, etc.), pick NewPipe. The pick is not visible. The sheet flashes and the feed reappears. (00:03.1; p008, p015, p026)
3. An "Open with NewPipe" chooser appears with the options: show info, play video, play in popup, play in background, download, add to playlist. It offers "Just once" and "Always". The 'Play video' row is highlighted. (00:08.4; p040)
4. NewPipe shows a red splash screen, then the video page. The "Next" section is empty and the autoplay toggle ("Tự động thêm vào hàng đợi") is shown. (00:13.4; p042, p045, p046)
5. Tap at [213, 311] on the autoplay toggle row. The toggle changes and the recommended list appears below, with the toggle shown off. (00:13.4; p048, p053)

Expected (implied): The video page loads, the related list under "Next" is populated, and the autoplay toggle behaves consistently with the list.

Actual: No error is shown. The "Next" section is empty when the page first opens and fills in about 3.6 s later. The share sheet and chooser flash and the YouTube feed reappears between steps. The UI looks inconsistent but no action visibly fails.

Key events: p040, p045, p046, p048, p053

Missed by the author:

- The share sheet and the Facebook/Messages row flashed briefly and the YouTube feed reappeared before the chooser (p015–p018, p026).
- The "Next" section is empty at first and fills in later (p045, p053).

Claims:

- ""Please subscribe to support our channel" (Vietnamese)" [u001]: not shown - This is a channel promo phrase and says nothing about the app behaviour.
