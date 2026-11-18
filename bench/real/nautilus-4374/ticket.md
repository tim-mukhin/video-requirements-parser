# "File / Folder names cannot contain `/`" warning perists after rename modal is opened and closed

Source: https://gitlab.gnome.org/GNOME/nautilus/-/issues/4374  (reporter: Francis Nimick (@fnimick), filed 2026-11-06)

# Affected Version

- Version:

  51.1
- Distribution:

  Bazzite 51
- Also happens with development version: Yes / No

# Steps to reproduce

1. Open a rename menu and type a `/` character in the file or directory name, and the "File / Folder names cannot contain `/`" warning is triggered
2. Close the rename menu by clicking outside or pressing escape
3. Open the rename menu again, on any file or folder, and see that the warning is present even though the name does not contain the`/` character 

# Expected Behavior

the warning should not persist into a new rename session

# Actual Behavior

the warning persists into a new rename operation (in the same window / tab only)

[attachment: recording.mp4]

# Additional Information
