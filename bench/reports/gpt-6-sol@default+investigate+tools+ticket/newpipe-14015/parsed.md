# real/newpipe-14015

_gpt-6-sol@default, 34 s; looked at: frames/moments/p054.jpg, frames/moments/p046.jpg, frames/0018.0.jpg, frames/0022.5.jpg, frames/0013.5.jpg, frames/0000.0.jpg, frames/0002.0.jpg, frames/0003.0.jpg, frames/moments/p015.jpg, frames/0006.5.jpg, frames/0008.5.jpg, frames/0010.0.jpg, frames/moments/p035.jpg, frames/0017.0.jpg_

The supplied recording does not reproduce the ticket’s YouTube Kids playback failure. It shows a news video shared from the regular YouTube feed to NewPipe; after loading, the video plays.

## Supplied recording plays a regular YouTube video rather than reproducing the YouTube Kids failure

Class: **not-a-bug**

Environment: YouTube and NewPipe with Vietnamese interface text. The ticket states NewPipe 0.29.2, Android 8, and Samsung Galaxy S7; those details are not visible in this recording.

Steps:

1. Open the overflow menu for the Báo Tuổi Trẻ trucking video in YouTube’s home feed (the trigger is not visible). (00:01.9; p006)
2. Open Share, then the expanded sharing options (the triggers are not visible). (00:03.1; p008, p027)
3. Choose NewPipe from the sharing options (the trigger is not visible). (00:08.4; p027, p040)
4. Choose NewPipe’s video player option (the trigger is not visible). (00:10.0; p040, p042)

Expected (implied): The selected video plays in NewPipe.

Actual: NewPipe displays a loading spinner, then plays the trucking video by about 17.7 seconds. The recording does not identify it as a YouTube Kids video or show a playback error.

Key events: p006, p027, p040, p042, p053, p054

Missed by the author:

- The shared item is visibly a Báo Tuổi Trẻ trucking news clip, not an identifiable YouTube Kids video [p006, p027].
- The apparent flicker after loading is the trucking footage playing, as the short-event frames show [p054]. The brief share-sheet changes are changing share targets, not a playback error [p015, p035].

Claims:

- "A YouTube Kids video cannot play." [ticket: YouTube Kids video cannot play]: not shown - The selected video is a Báo Tuổi Trẻ trucking news clip from the regular YouTube feed, and it plays in NewPipe. This does not test an identifiable YouTube Kids video.
- "The affected version is 0.29.2 and the device is a Samsung Galaxy S7 running Android 8." [ticket: Affected version; Affected Android/Custom ROM version; Affected device model]: not shown - No version, OS, or device-information screen appears.
