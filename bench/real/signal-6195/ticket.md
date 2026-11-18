# Image markup near top of the window triggers window dragging instead on macOS

Source: https://github.com/signalapp/Signal-Desktop/issues/6195  (reporter: awaitlink, filed 2022-11-30)

- [x] I have searched open and closed issues for duplicates
- [x] I am using Signal-Desktop as provided by the Signal team, not a 3rd-party package.

---

### Bug Description

When trying to markup an image near the top of the window, the window is dragged instead.

### Steps to Reproduce

1. Attach an image to a message draft.
   Note: this issue appears may be more noticeable or easier to reproduce on "portrait-oriented" images where height > width.
3. Press on the image to markup / edit it.
4. Make sure that Signal Desktop's width is such that the top of the image being edited is close to the top of the window.
5. Try to draw near the top of the screen.

**Actual Result:** Window dragging is often triggered, making it really hard to draw anything on the top of the image.
**Expected Result:** Either of:
- Window dragging is not triggered when touching the canvas.
- The canvas doesn't extend into the area that triggers window dragging.

### Screen recording

[attachment: recording.mp4]

### Platform Info

**Signal Version:** 6.0.0-beta.3
**Operating System:** macOS 13.1 Beta (22C5050e)
**Linked Device Version:** (not relevant)

### Link to Debug Log
https://debuglogs.org/desktop/6.0.0-beta.3/38a0d289244f92789b582450c552ff605271a63c8299f0c7222bd42efcd3f0b9.gz
