# Backticks are inserted at the previous backtick position after moving the cursor

Source: https://github.com/zed-industries/zed/issues/62058  (reporter: mustaphaboudouch, filed 2026-08-01)

### Reproduction steps

1. Open any file in Zed
2. Type a backtick character ( ` )
3. Move the cursor to a different position in the document (e.g. click elsewhere - do not use arrow keys)
4. Type another backtick character ( ` )

Here is a screen recording demonstrating the issue :

[attachment: recording.mp4]

### Current vs. Expected behavior

**Current behavior:** The second backtick is not inserted at the new cursor position. Instead, it gets written next to the first backtick that was typed earlier.

**Expected behavior:** The second backtick should be inserted exactly at the current cursor position, independent of where the previous backtick was typed.

### Zed version and system specs

- Zed version: 1.13.1
- OS: macOS Tahoe 26.6

### Attach Zed log file

<details><summary>Zed.log</summary>

```log

```
</details>

### Relevant Zed settings

Using default settings (no custom `settings.json` overrides).
<details><summary>settings.json</summary>

```json
{
  "icon_theme": "JetBrains New UI Icons (Dark)",
  "theme": "One Dark",
  "ui_font_size": 16.0,
  "buffer_font_size": 12.0
}
```
</details>

### Relevant Keymap

Using default keymap (no custom `keymap.json` overrides).
<details><summary>keymap.json</summary>

```json
[
  {
    "context": "Workspace",
    "bindings": {
      // "shift shift": "file_finder::Toggle"
    },
  },
  {
    "context": "Editor && vim_mode == insert",
    "bindings": {
      // "j k": "vim::NormalBefore"
    },
  },
]
```
</details>

### (for AI issues) Model provider details

_No response_

### If you are using WSL on Windows, what flavor of Linux are you using?

None
