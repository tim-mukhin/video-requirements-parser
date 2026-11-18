# real/resolve-yt-NAlREQjCvKE

_claude-sonnet-5.5@default, 49 s; looked at: frames/0000.0.jpg, frames/0008.0.jpg, frames/0016.0.jpg, frames/0024.0.jpg, frames/0032.0.jpg, frames/0040.0.jpg, frames/0048.0.jpg, frames/0056.0.jpg, frames/0064.0.jpg, frames/0072.0.jpg, frames/0080.0.jpg, frames/0088.0.jpg, frames/0096.0.jpg, frames/0036.0.jpg, frames/0044.0.jpg, frames/0068.0.jpg, frames/0084.0.jpg, frames/0092.0.jpg, frames/0076.0.jpg, frames/0090.0.jpg_

In DaVinci Resolve Studio 19.1 (Fusion page), a 3D scene has an Outer sphere and an Inner blue sphere. The Outer sphere is textured with a world-flag map whose empty areas should be transparent. With the keyed texture, the transparent areas still hide the Inner sphere. With the PNG's own alpha, the Inner sphere is visible. The ticket is empty, so the reporter's claim is inferred from the video only.

## Fusion 3D: transparent areas of the keyed texture on the Outer sphere still hide the Inner sphere behind it

Class: **wrong-data**

Environment: DaVinci Resolve Studio 19.1 build 12 on Windows (German taskbar, 30.11.2024). Project 'VTR-Logo', Fusion page. Nodes: ImageNoAlpha -> ChromaKeyer1, ImageWithAlpha, Outer (sphere), Inner (sphere), Merge3D1, MediaOut1. The Inner sphere is blue. Both images are a flag world map ('..p_of_World_(2023)_With_Alpha.png' is the visible clip name). The ticket does not name a version or setup.

Steps:

1. Start on the Fusion page after the splash screen. The viewer shows only the plain blue Inner sphere, and the Outer sphere has no texture connected. Inspector shows the Inner node. (00:08.0; 0008.0, 0016.0)
2. Drag a connection from ImageWithAlpha (the PNG with a real alpha channel) into the Outer node (inferred from the yellow line being dragged). The viewer then shows the map on a globe with the blue Inner sphere visible through the transparent areas, as expected. (00:32.0; 0032.0, 0036.0, 0040.0, 0044.0)
3. Disconnect ImageWithAlpha from Outer (inferred). The sphere turns plain white. Then view ChromaKeyer1 (the keyed ImageNoAlpha), which shows the map on a checkerboard, i.e. transparent where keyed. (00:48.0; 0048.0, 0056.0)
4. Connect ChromaKeyer1 output to the Outer node. The globe now shows the flags with torn, dark gaps. The blue Inner sphere, which sits at the centre, is not visible through the keyed transparent areas. (01:04.0; 0064.0, 0076.0, 0080.0)
5. Select Inner and drag its X translation in the viewer or Inspector (about 1.37 and 0.6). The blue sphere moves out to the right, but the part of it that overlaps the Outer sphere's volume is cut off with a hard vertical edge. So the transparent texels of the Outer sphere still block the Inner sphere. (01:24.0; 0084.0, 0088.0, 0090.0, 0092.0)

Expected (implied): Fully keyed (transparent) areas of the Outer sphere's texture should be invisible and should not hide the Inner sphere. The result should look like the ImageWithAlpha case, where the blue sphere shows through.

Actual: With ChromaKeyer1 feeding Outer, the Inner sphere is hidden inside the globe and clipped where it crosses the Outer sphere. With ImageWithAlpha feeding Outer, the Inner sphere is visible through the gaps.

Key events: 0040.0, 0080.0, 0088.0, 0092.0

Missed by the author:

- The ImageWithAlpha case shows the blue sphere through the transparent areas (0040.0, 0044.0, 0072.0), so only the ChromaKeyer path loses it.
- The Inner sphere is clipped by the Outer sphere as it moves out (0088.0, 0090.0, 0092.0), which suggests keyed pixels still write depth or the alpha is not fully zero. This is my reading, not stated in the video.

Claims:

- "The ticket contains no text, so there are no claims from the reporter to check." []: not shown - ticket.md has only a title and a source link, and the video has no sound.
