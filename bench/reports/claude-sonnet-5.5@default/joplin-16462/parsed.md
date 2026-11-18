# real/joplin-16462

_claude-sonnet-5.5@default, 21 s; looked at: frames/000091.jpg, frames/000209.jpg, frames/000304.jpg_

In the Joplin mobile note editor with the in-note search bar open, the on-screen keyboard keeps hiding and reappearing, and the search bar jumps up and down with it. The search field never takes focus long enough to type. The video has no real narration, only a mis-transcribed 'Thank you.'.

## Keyboard flickers and the search bar jumps while the in-note search field is open (Joplin mobile editor)

Class: **intermittent**

Environment: Joplin mobile app (phone, portrait, dark theme, 5G). Note 'Testing!' in a notebook titled 'Mess…', editor open with the 'Search for...' bar above the toolbar and the keyboard (search action key). Screen recording is active (status pill, 12:33). Account and organization are not visible.

Steps:

1. Open the note 'Testing!' in the editor and open the search bar ('Search for...'). The opening action itself is not visible. (00:00.7; s001, p001)
2. The keyboard is up. The search bar and toolbar flicker between the keyboard-up and keyboard-down layout. The keyboard keys show 'M' tap marks and keyboard letters changing. (00:01.8; p003, p009, p015, p016)
3. Tap on the keyboard area again. The keyboard changes (letter rows change), and the search/toolbar layout shifts. (00:04.4; p018, p021, p027, p029)
4. The keyboard disappears. The search bar and toolbar drop to the lower part of the screen, with empty space where the keyboard was. (00:05.9; p036, p037)
5. The keyboard comes back and the search bar moves up again. (00:07.4; p038, p039, p040)
6. Tap the search field at the end. The text cursor is shown in the empty 'Search for...' field, and the keyboard is still up. (00:08.6; p063, s026)

Expected (implied): Tapping the search field keeps the keyboard open, and the search bar stays in one position above it so the user can type a query.

Actual: The keyboard hides and reappears several times (frames 000209 and 000224 show it gone and the search bar low on screen; frames 000091 and 000304 show it up). The search bar and toolbar jump with it. The keyboard-key tap marks (m, !, H, M) show repeated taps with no query text appearing in the field, which stays 'Search for...'. The exact failure is not clear from the video. The most likely candidate is the keyboard and search bar layout unstable during focus changes.

Key events: p036, p037, p038, p039, p063, s021, s022

Missed by the author:

- The keyboard disappears completely for about 1.5 s (00:05.9-00:07.4) while the search bar stays open (p036, p037, p038).
- Parser-reported icon and letter changes (n/U, O/0, d/P) on the keyboard recur at 00:01.8, 00:04.8 and 00:08.2, which suggests the keyboard is being redrawn in cycles (p006-p008, p024-p026, p059-p061).

Claims:

- "'Thank you.' is the only speech" [u001]: not shown - Probably a mis-transcription of silence or background noise. It carries no information about the problem.
