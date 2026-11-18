# real/lo-174317

_claude-sonnet-5.5@default, 33 s; looked at: frames/0011.0.jpg, frames/0104.0.jpg_

After a LibreOfficeDev 27.2 Writer session was killed with Ctrl-C, with AutoRecovery set to 1 minute and "Automatically save the document instead" ticked, the Document Recovery wizard did not just restore the file. Recover Selected led to a "file is corrupt, repair?" prompt, then "could not be repaired and cannot be opened", then "Original document recovered", then an "automatic recovery process was interrupted" Save/Cancel dialog. The Writer document with 'Some text' still opened afterwards.

## Document recovery after a crash shows a chain of corrupt/repair/interrupted dialogs before the autosaved document opens

Class: **error-shown**

Environment: LibreOfficeDev 27.2 Writer on Linux (Russian locale, English UI, KDE-style desktop), started from Konsole as libreofficedev27.2. Profile reset first with rm -rf ~/.config/libreofficedev. File: /home/user/Testing files/temp-empty-file.odt. The ticket names builds 25.8 and 26.8; the video shows 27.2.

Steps:

1. In Konsole, delete the profile and launch libreofficedev27.2 with temp-empty-file.odt (empty Writer document opens; first-run Welcome box). (00:00.9; p001, p006, p007)
2. Tools > Options > Load/Save > General: set 'Save AutoRecovery information every' to 1 minute (the field was clicked and edited). (00:08.3; p046, p047, p063)
3. Tick 'Automatically save the document instead' (checked in the frame at 11 s together with the 1-minute interval), click Apply, then close the dialog. (00:10.0; p069, p073, p076)
4. Type 'Some text' in the document (the typing itself is not shown; the text appears and the status bar reads 2 words, 9 characters). Leave the document alone for about 70 s. (00:16.8; p128, p129)
5. Kill the process: the cursor goes to Konsole and ^C appears, Writer disappears. The trigger is not directly visible, but the ^C is. (01:29.6; p135, p137, p139)
6. Start libreofficedev27.2 again without a file argument. Document Recovery opens listing temp-empty-file.odt as 'Not recovered yet'. Click 'Recover Selected'. The cursor is not tracked 01:30.3-01:36.6, so the launch is inferred from the typed command. (01:36.8; p143, p167, p173)
7. A 'file is corrupt, repair?' prompt appears; click Yes. (01:39.0; p174, p177)
8. A 'could not be repaired and therefore cannot be opened' error appears; click OK. (01:41.5; p178, p183)
9. Recovery finishes with status 'Original document recovered'; click Finish. (01:43.5; p184, p190)
10. An 'automatic recovery process was interrupted' dialog offers Save (to /home/user/Документы) or Cancel; click Cancel. The Writer document opens with 'Some text', 2 words, 9 characters. (01:44.9; p191, p201, p203)

Expected (implied): Recovery opens the autosaved document directly, without corruption, repair or 'interrupted' dialogs.

Actual: Recovery shows a corrupt-file prompt, a repair-failed error, an 'Original document recovered' status and an 'interrupted' Save/Cancel dialog. After Cancel the document with 'Some text' opens anyway, so the data is not lost.

Key events: p173, p174, p178, p184, p191, p203

Missed by the author:

- The cursor is not tracked 01:30.3-01:36.6, so the relaunch before the recovery dialog is inferred from the typed command (p143).
- The status after recovery is 'Original document recovered', not the autosaved version (p184), even though 'Some text' is in the final document.
- The 'interrupted' dialog offers Save to a folder or Cancel (p191); the author chose Cancel and the document still opened (p201, p203).
- An earlier launch with the file argument was interrupted with ^C before the recovery run, so the crash was simulated with Ctrl-C in the terminal rather than killing soffice.bin as the ticket says (p139).

Claims:

- "A chain of recovery dialogs appears instead of the file opening." [ticket]: confirmed - Seen at 01:39.0 (p174), 01:41.5 (p178), 01:43.5 (p184) and 01:44.9 (p191). The separate 'Repair error' dialog from the ticket is not seen as a distinct window; the 'could not be repaired' message is probably the same dialog.
- "The 'Automatically save the document instead' option was enabled." [ticket]: confirmed - The frame at 11 s shows the checkbox ticked with a 1-minute interval, after the click at 10.0 s (p069) and Apply (p073). The first reader's note that it was unchecked is refuted by this frame.
- "After the dialogs the autosaved file opens normally." [ticket]: confirmed - The Writer window with 'Some text' (2 words, 9 characters) appears at 01:46.3 (p203).
- "This is a regression: not present in 24.2.0.1, present in 25.8.0.1." [ticket]: not shown - Only a 27.2 build appears in the video; no other version is compared.
- "Reproducible: Always." [ticket]: not shown - The video shows one run only.
