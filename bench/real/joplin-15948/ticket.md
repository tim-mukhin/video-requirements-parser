# Desktop: Possible to temporarily delete read-only notes when multiple notes are selected

Source: https://github.com/laurent22/joplin/issues/15948  (reporter: personalizedrefrigerator, filed 2026-07-15)

### Operating system

Linux

### Joplin version

3.7.9

### Desktop version info

Joplin 3.7.9 (dev, linux)

Device: linux, unknown
Client ID: e0957bfc8b494320bf8213279fbf3840
Sync Version: 3
Profile Version: 53
Keychain Supported: No
Alternative instance ID: -
Sync target: Joplin Cloud
Editor: Markdown

Revision: fd76c4052a (pr/desktop/ai-cancel-chat)

Backup: 1.5.1
Freehand Drawing: 4.3.0

### Current behaviour

To reproduce:
1. Select multiple read-only notes (e.g. from a Joplin Cloud share).
2. Click "Delete".
3. Observe that the notes have been deleted.
4. Sync.
5. Observe that the notes have been recreated.

Screen recording:

[attachment: recording.mp4]

### Expected behaviour

It should not be possible to delete read-only notes (even temporarily).

### Logs

_No response_
