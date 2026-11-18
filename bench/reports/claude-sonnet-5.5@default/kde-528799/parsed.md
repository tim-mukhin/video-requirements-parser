# real/kde-528799

_claude-sonnet-5.5@default, 23 s; looked at: frames/000174.jpg, frames/000266.jpg, frames/000402.jpg_

A silent screen recording of Krita on an Android tablet. The author drags a transform box on the Mask layer of an unsaved document, and the box's X, Y and width values jump back and forth while 'Updating...' flashes. The recording has no audio, so the intended problem is not stated.

## Krita transform tool on a mask layer: box position and size jump and show 'Updating...' during resize

Class: **wrong-data**

Environment: Krita (getaroom.kra and '[Not Saved]' tabs) on an Android tablet or phone-like device (status bar clock 5:40, XRecorder screen recording). The Mask layer is selected and the Transform tool is active. Zoom is about 90%.

Steps:

1. Start the recording in XRecorder (tap at the record button, then the recorder counts up). (00:00.6; p001, p002)
2. Switch to Krita with the '[Not Saved]' document open (the trigger is not visible). (00:05.2; p018)
3. Zoom the canvas (82% to 90%) and open the Transform tool on the Mask layer. The Tool Options show X/Y/W/H values and 'Updating... 0%' appears. (00:08.8; p021, p027, p029)
4. Drag a handle of the transform box. The geometry values jump between runs (e.g. 248.64/127.48, then 238.31/148.16, then 223.23/178.34, then 183.46/257.90), and 'Updating... 33%/25%/0%' flashes. (00:11.9; p037, p038, p047, p052, p057, p058, p060)
5. Repeat the drag: the box is shown skewed, overlapping the left panel, then the values jump back to 223.18/178.43, which is close to the earlier state. (00:20.9; p074, p083)

Expected (implied): The transform box follows the drag smoothly and stays a clean rectangle. Tool Options values change consistently and no repeated 'Updating...' progress appears.

Actual: While transforming on the Mask layer, the box becomes skewed (frame 000266 shows a slanted box extending over the left panel). The X/Y/W values oscillate erratically between frames, and 'Updating...' progress flashes repeatedly. Near the end the values return to about the earlier state (223.18/178.43). The author then opens the 'Stop sharing screen?' dialog to end the recording.

Key events: p027, p029, p037, p047, p057, p060, p067, p074, p083, p089

Missed by the author:

- Nothing was said, so nothing can be shown as missed. The 'Updating...' flashes [p054], [p058], [p065] and the quick value changes [p057], [p060], [p074] are brief and easy to miss.
- The 'Press CTRL... from center' and 'Click and drag... selection' hints alternate in the status bar [p055], [p063], [p066], [p080], which suggests the tool switched state during the drag.
