# Flex layout hug and fill do not respond correctly

Source: https://github.com/penpot/penpot/issues/8176  (reporter: sara-dndg, filed 2026-01-23)

**Describe the bug**
Hug Content and Fill containers inside a flex layout do not render correctly when layout changes are triggered by interactions.

**Steps to Reproduce**
1. Create a card with a flex layout that contains other flex elements, such as text, images, or buttons.
2. Trigger different interactions (e.g. remove an element or extend the card content).
4. The Hug and Fill settings do not update correctly, even though they appear as applied in the UI. 

**Expected behavior**
Hug Content and Fill containers should update and respond correctly when interactions are triggered.

**Screenshots or screen recordings**
[attachment: recording.mp4]

**Desktop (please complete the following information):**
OS: MacOS
Google Chrome
Version 143.0.7499.193
