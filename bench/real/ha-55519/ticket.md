# Automation Conditions editor unusably slow in WebKit

Source: https://github.com/home-assistant/frontend/issues/55519  (reporter: inventor7777, filed 2026-11-01)

### Checklist

- [x] I have updated to the latest available Home Assistant version.
- [x] I have cleared the cache of my browser.
- [x] I have tried a different browser to see if it is related to my browser.
- [ ] I have tried reproducing the issue in [safe mode](https://www.home-assistant.io/blog/2023/11/01/release-202311/#restarting-into-safe-mode) to rule out problems with unsupported custom resources.

### Describe the issue you are experiencing

When trying to add a condition in WebKit on Safari PWA on macOS 15.8.1, the frontend becomes unusably slow.

### Describe the behavior you expected

I expected it to stay responsive.

### Steps to reproduce the issue

1. Have a lot of entities
2. Go to add a condition to an automation in WebKit
3. Unusably slow

### What version of Home Assistant Core has the issue?

2026.11.0b2

### What was the last working version of Home Assistant Core?

_No response_

### In which browser are you experiencing the issue?

Safari Version 27.0 (20625.1.29.18.28)

### Which operating system are you using to run this browser?

macOS Sequoia 15.8.1

### State of relevant entities

```txt

```

### Problem-relevant frontend configuration

```yaml

```

### JavaScript errors shown in your browser console/inspector

```txt
No errors
```

### Additional information

Does not appear to reproduce inside Opera.

I wish I could tell you what was happening, but agentic tools use their own versions of Chromium and I am no expert in web development.

<-- Failed to upload "Screen Recording 2026-10-31 at 19.30.20_1.mp4" -->

[attachment: recording.mp4]

It bogged down my MacBook Pro so much that some of the mouse clicks are not even registered.
