# real/lo-174317

_claude-sonnet-5.5@default, 45 s; looked at: frames/0001.0.jpg, frames/0010.0.jpg, frames/0025.0.jpg, frames/0040.0.jpg, frames/0055.0.jpg, frames/0070.0.jpg, frames/0085.0.jpg, frames/0100.0.jpg, frames/0076.0.jpg, frames/0079.0.jpg, frames/0082.0.jpg, frames/0088.0.jpg, frames/0092.0.jpg, frames/0096.0.jpg, frames/0104.0.jpg, frames/0108.0.jpg, frames/0098.0.jpg, frames/0102.0.jpg, frames/0012.0.jpg, frames/0090.0.jpg, frames/0006.0.jpg, frames/0014.0.jpg_

In LibreOffice Dev 27.2 on Linux, the reporter set the AutoRecovery interval to 1 minute, typed text, waited, and killed the process. On restart the recovery dialog offered the file, but 'Recover Selected' led to a chain of 'file is corrupt', 'could not be repaired' and 'Original document recovered' dialogs. The text was eventually restored, but the user had to go through several error dialogs to get it.

## Document recovery after a crash shows a chain of 'corrupt file / could not be repaired' dialogs before the document opens

Class: **error-shown**

Environment: Konsole terminal and LibreOffice Dev 27.2 Writer on a KDE-like Linux desktop (Russian locale, English UI). The profile was reset first with rm -rf ~/.config/libreofficedev. The file is '/home/user/Testing files/temp-empty-file.odt', launched with the libreofficedev27.2 command. The ticket's versions (25.8 and 26.8) do not match the 27.2 build in the video.

Steps:

1. In Konsole, delete the profile (rm -rf /home/user/.config/libreofficedev) and launch libreofficedev27.2 with temp-empty-file.odt. An empty Writer document opens. (00:01.0; 0001.0, 0012.0)
2. Open Tools > Options > Load/Save > General (inferred from the dialog). 'Save AutoRecovery information every' is checked and set to 1 minute. 'Automatically save the document instead' is unchecked in the frame at 10 s. Whether it was later ticked, and OK pressed, is not visible. (00:10.0; 0006.0, 0010.0, 0014.0)
3. Type 'Some text' in the document (inferred from the typed text; the typing itself is not visible). The status bar shows 2 words, 9 characters. Wait roughly 1.5 minutes without touching the document. (00:25.0; 0025.0, 0055.0, 0085.0)
4. Terminate LibreOffice. A launch was run in the terminal at 90 s and Ctrl-C (^C) appears by 92 s; the kill itself is inferred. (01:30.0; 0090.0, 0092.0)
5. Start libreofficedev27.2 again without a file argument. The Document Recovery dialog lists temp-empty-file.odt as 'Not recovered yet'. Click 'Recover Selected'. (01:38.0; 0096.0, 0098.0)
6. A dialog says the file 'temp-empty-file.odt' is corrupt and asks whether to repair it. The user chooses Yes (inferred). (01:40.0; 0100.0)
7. A second dialog says the file 'could not be repaired and therefore cannot be opened'. (01:42.0; 0102.0)
8. Document Recovery finishes with status 'Original document recovered'. After Finish, the Writer document opens with 'Some text'. (01:44.0; 0104.0, 0108.0)

Expected (implied): After a crash, the recovered document opens straight from the recovery dialog with no corruption or repair errors.

Actual: Recovery shows a 'file is corrupt, repair?' prompt, then a 'could not be repaired and cannot be opened' error, then the recovery list says 'Original document recovered'. The document does contain 'Some text' at the end.

Key events: 0098.0, 0100.0, 0102.0, 0104.0, 0108.0

Missed by the author:

- The 'Automatically save the document instead' checkbox is unchecked in the only options frame (0010.0).
- The video was recorded on build 27.2, not on the versions named in the ticket.
- A second launch with the file was started and interrupted with Ctrl-C (0090.0, 0092.0) before the recovery run.

Claims:

- "A chain of recovery dialogs appears instead of the document opening." [A chain of recovery dialogs are displayed]: confirmed - The frames show recovery, then 'corrupt, repair?' (0100.0), then 'could not be repaired' (0102.0), then 'Original document recovered' (0104.0). A separate 'Repair error' dialog and a final 'recovery was interrupted' message were not in the sampled frames.
- "The 'Automatically save the document instead' option was enabled." [Automatically save the document instead option in enabled]: not shown - The checkbox is unchecked at 10 s, and the video never shows it ticked or the dialog confirmed.
- "The autosaved document opens normally after the dialogs." [After the chain of dialog boxes, the autosaved file opens normally.]: confirmed - The text 'Some text' is shown at 0108.0.
- "The bug is a regression from 24.2 and appears in 25.8 and 26.8." [this issue is not present in 24.2.0.1, but already exist in 25.8.0.1]: not shown - The video only shows a 27.2 build. No other version is compared.
