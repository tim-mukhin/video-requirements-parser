# real/gshell-9522

_claude-sonnet-5.5@default, 13 s; looked at: nothing_

Choosing Power Saver in the battery settings shows the message "performance mode temporarily disabled due to high operating temperature", although the device is not reported as hot. The reporter says Performance mode can still be picked, so the message looks wrong and misleading. The ticket is brief and there is no video to confirm it.

## Power Saver selection in battery settings shows 'performance mode temporarily disabled due to high operating temperature' without overheating

Class: **error-shown**

Environment: Fedora 45, GNOME Shell with no extensions enabled. Hardware, GNOME and power-profiles-daemon versions, and the settings app are not given.

Steps:

1. Open battery settings (Settings > Power/Battery). (00:00.0; )
2. Select the Power Saver mode. (00:00.0; )
3. Look for the "performance mode temporarily disabled due to high operating temperature" message. (00:00.0; )

Expected (implied): No thermal warning appears when selecting Power Saver while the device is not hot. If Performance were really disabled, it would not be selectable.

Actual: The message "performance mode temporarily disabled due to high operating temperature" appears even though the device is not hot. The reporter says Performance mode can still be selected.

Key events: 

Claims:

- "The device is not at a high operating temperature." [despite that not being the case]: not shown - No temperature data or video. This is the reporter's assertion only.
- "Performance mode can still be selected despite the message." [it doesnt really stop me from picking the performance mode anyways]: not shown - Cannot be checked without the recording.
- "The bug happens with no extensions enabled." [happens even without any extensions being enabled]: not shown - Reporter's statement only.
