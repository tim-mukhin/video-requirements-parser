# real/lo-174317

_gpt-6-sol@default, 46 s; looked at: frames/0009.0.jpg, frames/0011.0.jpg, frames/0087.0.jpg, frames/0091.0.jpg, frames/0100.0.jpg, frames/moments/p142.jpg, frames/0097.0.jpg, frames/0102.0.jpg, frames/0104.0.jpg, frames/0105.0.jpg, frames/0106.0.jpg, frames/moments/p003.jpg, frames/moments/p085.jpg, frames/0089.0.jpg, frames/0096.0.jpg, frames/0013.0.jpg, frames/0086.0.jpg, frames/moments/p077.jpg_

After LibreOfficeDev is relaunched, recovering an ODT with automatic document saving enabled produces corruption, failed-repair and interrupted-recovery dialogs. The document eventually opens with its text, but the warnings and extra steps make recovery appear to have failed.

## Automatic-save recovery reports corruption before opening the ODT

Class: **error-shown**

Environment: LibreOfficeDev 27.2 Writer on a Linux KDE desktop, launched from Konsole; /home/user/Testing files/temp-empty-file.odt.

Steps:

1. Open /home/user/Testing files/temp-empty-file.odt in Writer. (00:00.9; p001, p006)
2. In Tools > Options > Load/Save > General, set AutoRecovery to 1 minute, enable “Automatically save the document instead,” and apply the settings. (00:07.6; p046, p063, p069, p073, p076)
3. Type “Some text” and leave the document open for over a minute. (00:16.8; p128, p129, p131)
4. Interrupt the running session from Konsole, then launch LibreOfficeDev again; Document Recovery opens. (01:30.7; p139, p162, p164, p166)
5. Click “Recover Selected” for temp-empty-file.odt. (01:39.0; p166, p173, p174)

Expected (implied): After recovery is accepted, the document opens without corruption or repair dialogs.

Actual: Writer says 'temp-empty-file.odt' is corrupt. After “Yes,” it says the file could not be repaired; the recovery window then marks the original document recovered. Clicking “Finish” opens an interrupted-recovery dialog. After “Cancel,” Writer displays “Some text”; the video does not establish which saved copy supplied it. [p174, p177, p178, p184, p190, p191, p201, p203]

Key events: p069, p073, p128, p139, p166, p173, p174, p178, p184, p191, p203

Missed by the author:

- The settings show a 1-minute AutoRecovery interval and “Always create backup copy” checked. [p047, p063, p069]
- Before the first document opens, Konsole reports an error removing a LibreOfficeDev profile directory; during recovery it also reports library-loading errors. The video does not establish either as the cause. [p002, p187]
- The interrupted-recovery dialog offers to save temp-empty-file.odt under /home/user/Документы; the user clicks “Cancel.” [p191, p201]

Claims:

- "Recovery shows a chain of corruption, failed-repair and interrupted-recovery dialogs." [ticket.md: Description]: confirmed - The timeline records the sequence and the frames show the dialogs. [p174, p178, p184, p191]
- "The corruption error shows an empty filename." [ticket.md: Description]: refuted - The dialog names 'temp-empty-file.odt'. [p174]
- "The autosaved file opens normally and saving itself is unaffected." [ticket.md: Description]: not shown - Writer eventually displays the entered text, but the recording does not identify the copy opened or inspect the file on disk. [p184, p201, p203]
- "The ODT was created on the Desktop." [ticket.md: Steps to Reproduce 1]: refuted - The visible command opens an ODT under /home/user/Testing files; creation is not shown. [p001, p082]
- "Autosave completed before the interruption." [ticket.md: Steps to Reproduce 4]: not shown - More than a minute passes with the document open, but no completed autosave is demonstrated. [p128, p131, p139]
- "The soffice.bin process was killed." [ticket.md: Steps to Reproduce 5]: not shown - Konsole shows ^C and returns to a prompt, not a process-specific kill. [p139]
- "The issue reproduces always, exists in 25.8 and 26.8, and is absent in 24.2." [ticket.md: Reproducible / Additional Info]: not shown - The video shows one recovery attempt in LibreOfficeDev 27.2, with no version comparison. [p167, p173]
