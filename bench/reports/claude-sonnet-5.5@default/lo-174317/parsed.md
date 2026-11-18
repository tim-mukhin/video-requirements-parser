# real/lo-174317

_claude-sonnet-5.5@default, 30 s; looked at: nothing_

LibreOfficeDev Writer was launched with a wiped profile, and the author changed an autosave option and typed "Some text". About 1:29 a click in the document was followed by Writer leaving the front, and the author stopped the process in the terminal with ^C. After a relaunch, Document Recovery reported the file as corrupt and could not repair it. It then said "Original document recovered" and ended with an "interrupted" prompt. After Cancel the document opened with its text, so the recovery messages contradict each other.

## Writer stops responding or crashes after a click; Document Recovery says the file is corrupt, then "recovered", then "interrupted"

Class: **error-shown**

Environment: LibreOfficeDev 27.2 development build (Writer) on Linux (hostname rosa-fj6yfb), Russian locale. It was launched from Konsole as `libreofficedev27.2 '/home/user/Testing files/temp-empty-file.odt'` after `rm -rf ~/.config/libreofficedev`. A second window at the end appears to be a Russian-language bug tracker. No accounts are visible.

Steps:

1. Delete the profile and launch Writer on temp-empty-file.odt from Konsole. A first-run Welcome sidebar appears. (00:00.9; p001, p006, p007)
2. Open Tools > Options > Load/Save > General, tick "Automatically save the document instead" and click Apply. (00:10.0; p069, p073)
3. Confirm the dialog. The Writer window then goes away and the Konsole is shown. Relaunch Writer with the same command; the Tip of the Day appears. (00:11.4; p076, p081, p082, p085, p088)
4. Type "Some text" into the document; the status bar shows 2 words, 9 characters. (00:16.8; p127, p128)
5. Click in the Writer window at 01:29.6. Writer leaves the front and Konsole (oosplash) is shown. The cursor cannot be followed for the next ~6 s and ^C appears in the terminal. (01:29.6; p134, p136, p138)
6. Relaunch Writer from the terminal. The Document Recovery dialog opens; click "Recover Selected". (01:32.1; p141, p163, p170)
7. A message says temp-empty-file.odt is corrupt and offers to repair it. Click "Yes" and get "could not be repaired", then click OK. (01:39.0; p171, p174, p175, p180)
8. The dialog now says "Original document recovered" and the terminal shows missing gcc3.so and java.so. Click "Finish", get "The automatic recovery process was interrupted", and click Cancel. (01:43.5; p181, p184, p187, p188, p198)
9. Writer opens temp-empty-file.odt with "Some text" (2 words, 9 characters). (01:46.3; p200)

Expected (implied): Writer keeps running. If it has to recover, Document Recovery restores the file and reports one consistent result, without a "corrupt" or "could not be repaired" error.

Actual: After a click in the document, Writer stopped being the front window and the author stopped the process with ^C. Document Recovery then called the file corrupt, failed to repair it, and reported "Original document recovered". After that came "automatic recovery process was interrupted" and missing-library warnings. The document did open afterwards with "Some text", so the corruption and repair-failure messages contradict the outcome.

Key events: p134, p136, p138, p163, p171, p175, p181, p184, p188, p200

Missed by the author:

- A similar earlier episode: after Apply and OK in Options, Writer left the front at 00:12 and was relaunched from Konsole (p076, p081, p082). The trigger is not visible, and the author did not mention it.
- The first launch printed warnings: failed removal of the profile's extensions directory and an OpenCL driver check failure (p002, p004).
- The recovery messages contradict each other: "corrupt" and "could not be repaired" (p171, p175), then "Original document recovered" (p181), then "interrupted" (p188).
- Missing libraries gcc3.so and java.so were reported during recovery (p184).
- The cursor is not tracked at 01:30.3-01:36.6, so what actually caused the stop cannot be seen. The ^C is seen as text only (p138).

Claims:

- ""Thank you." is the only speech. It makes no claims about the bug." [u004]: not shown - The utterance is a sign-off, and the cause of the problem is not stated anywhere in the audio.
