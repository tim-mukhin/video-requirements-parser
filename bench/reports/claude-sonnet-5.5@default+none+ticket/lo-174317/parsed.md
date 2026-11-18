# real/lo-174317

_claude-sonnet-5.5@default, 18 s; looked at: nothing_

With "Automatically save the document instead" enabled, after an autosave and a killed soffice.bin, accepting recovery on restart shows a chain of error dialogs instead of opening the document. The autosaved file does open normally at the end. It looks like a regression: it is absent in 24.2.0.1 and present in 25.8.0.1 and 26.8.0.3.0+. Users see confusing corruption errors that suggest data loss, even though the data is recovered.

## Document recovery shows a chain of error dialogs when "Automatically save the document instead" is enabled

Class: **error-shown**

Environment: LibreOffice Writer, .odt file on Desktop. Linux 6.12 x86_64, VCL kf5 (cairo+xcb), locale ru-RU, UI en-US. Versions 25.8.0.1 (Build 127f2cf27c25aaac008a1045ebfed22015cb3064) and 26.8.0.3.0+ (Build 77909295eab86f8712d508d80a15c2ccf247bb99). Not present in 24.2.0.1. User profile not reset. No accounts or organizations involved.

Steps:

1. Create an .odt file on the Desktop and open it in LibreOffice Writer. (00:00.0; )
2. Go to Tools > Options > Load/Save > General. Enable "Save AutoRecovery information every: * minutes" and "Automatically save the document instead". (00:00.0; )
3. Type some text in the document. (00:00.0; )
4. Wait until the autosave has completed. (00:00.0; )
5. Kill the soffice.bin process. (00:00.0; )
6. Start LibreOffice again and accept the document recovery dialog. (00:00.0; )

Expected (speech): The autosaved document opens without any additional steps.

Actual: After recovery is accepted, a chain of dialogs appears: document recovery, then recovery error ("The file '' is corrupt"), then Repair error, then "Original document recovered", then "recovery was interrupted". The autosaved file then opens normally. Reproducible always.

Key events: 

Claims:

- "This is a regression: absent in 24.2.0.1, present in 25.8.0.1." [Its looks like a regression, as this issue is not present in 24.2.0.1, but already exist in 25.8.0.1.]: not shown - Based on the reporter's statement only. No video or logs, and no versions between 24.2 and 25.8 were tested.
- "The defect does not affect the file saving process itself." [This defect does not seem to affect the file saving process itself.]: not shown - The reporter hedges. The only support is that the autosaved file opens after the dialogs.
