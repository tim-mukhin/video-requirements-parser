# Bug: New Folder input field persists previous folder name

Source: https://github.com/excalidraw/excalidraw/issues/11376  (reporter: Shaanworkspace, filed 2026-05-22)

### Description
I noticed a UI/UX bug in the Excalidraw desktop app (macOS) where the "New Folder" dialog does not clear its state after a folder is created. 

### Steps to Reproduce
1. Open the Excalidraw desktop application.
2. Click on the **New Folder** button.
3. Type a name (e.g., `Try1`) and confirm.
4. Click the **New Folder** button again.

### Expected Behavior
The input field should be empty, or at least show a default placeholder like "Untitled Folder," allowing for a fresh entry.

### Actual Behavior
The input field is prefilled with the string from the last created folder (e.g., `Try1`). This requires the user to manually backspace or select all text to delete it before typing a new name.

### Impact
While minor, it creates a repetitive friction point for users organizing their workspace with multiple folders. It deviates from standard UI patterns where input modals should reset upon successful submission.

### Environment
- **Platform:** macOS
- **App Version:** Version 1.7.3 (59)
- **Installation:** Desktop Download (not web version)

### Media
I have attached a screen recording demonstrating this behavior below.

[attachment: recording.mp4]

---
**Note for Maintainers:** I am interested in contributing to Excalidraw. If this is a confirmed bug and the fix is straightforward, I would be happy to submit a PR to help resolve this.
