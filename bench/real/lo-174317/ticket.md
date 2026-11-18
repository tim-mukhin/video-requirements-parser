# Error related to restore the file with the “Automatically save the document instead” option enabled.

Source: https://bugs.documentfoundation.org/show_bug.cgi?id=174317  (reporter: <email>, filed 2026-11-03)

Description:
When the “Automatically save the document instead” option is enabled, after autosave and a LibreOffice crash, a file recovery dialog box is displayed. When recovery is accepted, instead of the expected file opening, a chain of dialog boxes will be displayed (document recovery -> recovery error (The file '' is corrupt) -> Repaire error -> Original document recovered -> recovery was interrupted). This defect does not seem to affect the file saving process itself. After the chain of dialog boxes, the autosaved file opens normally.

Its looks like a regression, as this issue is not present in 24.2.0.1, but already exist in 25.8.0.1.

Steps to Reproduce:
1. Create .odt file on Desktop and then open it in LibreOffice Writer
2. Set Tools -> Options -> Load/Save -> General -> "Save AutoRecovery information every: * minutes" and “Automatically save the document instead” option in enabled
3. Write some text
4. Wait until the autosave is completed
5. Kill soffice.bin process
6. Open LibreOffice again

Actual Results:
A chain of recovery dialogs are displayed

Expected Results:
Autosaved document open without any addition steps

Reproducible: Always

User Profile Reset: No

Additional Info:
exists at least on:
Version: 25.8.0.1 (X86_64)
Build ID: 127f2cf27c25aaac008a1045ebfed22015cb3064
CPU threads: 16; OS: Linux 6.12; UI render: default; VCL: kf5 (cairo+xcb)
Locale: ru-RU (ru_RU.UTF-8); UI: en-US
Calc: threaded

still repro on:
Version: 26.8.0.3.0+ (X86_64)
Build ID: 77909295eab86f8712d508d80a15c2ccf247bb99
CPU threads: 16; OS: Linux 6.12; UI render: default; VCL: kf5 (cairo+xcb)
Locale: ru-RU (ru_RU.UTF-8); UI: en-US
Calc: threaded
