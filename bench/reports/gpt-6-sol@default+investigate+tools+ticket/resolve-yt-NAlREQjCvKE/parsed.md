# real/resolve-yt-NAlREQjCvKE

_gpt-6-sol@default, 37 s; looked at: frames/0035.0.jpg, frames/0058.0.jpg, frames/0071.0.jpg, frames/0087.0.jpg, frames/0094.0.jpg, frames/moments/p125.jpg, frames/0062.0.jpg, frames/0068.0.jpg, frames/0076.0.jpg, frames/0083.0.jpg, frames/moments/p216.jpg, frames/0051.0.jpg_

In DaVinci Resolve's Fusion viewer, an outer globe textured with a chroma-keyed map shows gaps instead of the blue inner sphere. The same setup shows the inner sphere through a map image with an existing alpha channel, so the difference affects the intended globe composite.

## Chroma-keyed outer globe does not reveal inner sphere

Class: **silent-fail**

Environment: DaVinci Resolve Studio 19.1 Build 12 on Windows; Fusion page of the VTR-Logo project, with Inner and Outer feeding Merge3D1.

Steps:

1. With Inner and Outer in the Merge3D1 composition, use the map without an alpha channel as the input to ChromaKeyer1. (00:48.0; p095, p097, p104)
2. Connect ChromaKeyer1's output to Outer's material input and view Merge3D1. (00:55.2; p124, p131, p160, p159)

Expected (speech): The blue inner sphere should be visible through the keyed-out parts of the outer map, as it is with the map image that has an alpha channel.

Actual: The keyed map's gaps reveal the Fusion viewer grid, not the blue sphere. Moving Inner sideways exposes the sphere; returning its Translation X to 0 hides it again.

Key events: p097, p124, p131, p159, p214, p220, p245

Missed by the author:

- The no-alpha source has a pale blue background, while ChromaKeyer1's viewer shows that background as transparent before it is applied to Outer [p097, p121].
- MediaOut1 is disconnected from Merge3D1; the demonstrated failure is in the Fusion viewer, not a shown final output [p159].

Claims:

- "The image with an alpha channel reveals the inner sphere." [u005]: confirmed - The Merge3D1 viewer shows a blue globe behind the flags at 00:35 and again after the alpha image is reconnected at 01:11.
- "Using the chroma-keyed image makes the inner sphere invisible." [u008]: confirmed - The Merge3D1 viewer shows gaps through to the grid at 01:02. The sphere is still present: it becomes visible when Inner is moved sideways.
- "The filed ticket identifies a specific failure." [ticket.md]: not shown - The ticket contains only a generic bug-report heading and source metadata; the failure is demonstrated in the video.
