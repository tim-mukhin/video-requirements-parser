# real/blender-yt-tSQ5b7zBOa0

_gpt-6-sol@default, 47 s; looked at: frames/0148.0.jpg, frames/0152.0.jpg, frames/0164.0.jpg, frames/0182.0.jpg, frames/0150.0.jpg, frames/0154.0.jpg, frames/moments/p1247.jpg, frames/0146.0.jpg, frames/0156.0.jpg, frames/0162.0.jpg_

The reporter demonstrates that enabling Individual on Blender’s Extrude Mesh node changes which generated face is selected by a face index. The resulting openings move around the mesh, making index-based face selection difficult to predict; the video does not establish that the ordering changes between repeated evaluations of the same settings.

## Extrude Mesh Individual mode produces an unexpected face-index order

Class: **wrong-data**

Environment: Blender 3.6.0 Beta on Windows; Geometry Nodes workspace, selected Cube with a Geometry Nodes modifier.

Steps:

1. Create a mesh from a Curve Line and a Curve Circle with resolution 8, then select a face by index and pass it through Extrude Mesh and Delete Geometry configured for Face / All. (00:04.7; p023, p025, p027, p029, u002)
2. With Extrude Mesh Individual off, change the Delete Geometry comparison index to inspect successive generated faces. (02:08.8; u016, p739, p801, u021, u024)
3. Turn on Extrude Mesh Individual and change the deletion index again; different positions around the extrusion open as the index changes. (02:31.4; p1178, u031, p1262, p1292, p1344, p1389)

Expected (speech): Generated face indices should follow a predictable order when extruding individual faces, as the reporter expects from the non-Individual case.

Actual: With Individual enabled, changing the indexed face selected for deletion produces openings in an order the reporter cannot account for. The frames confirm the openings, but do not establish the correct index-to-face mapping or show the same settings producing different results.

Key events: u024, p1178, u031, p1262, p1292, p1344, p1389, u036, u038

Missed by the author:

- The visible opening is produced through Delete Geometry set to Face / All; an opening alone does not prove that the wrong face was deleted [p027, p1520].
- The ticket supplies only a generic bug-report title, not a specific failure or reproduction claim. The screen identifies Blender 3.6.0 Beta [p1129].

Claims:

- "Individual faces go in a completely different order." [u031]: confirmed - The timeline records the Individual toggle and subsequent index changes; frames show the deletion opening at different positions.
- "The ordering is non-deterministic." [u038]: not shown - The reporter changes indices and views, but does not demonstrate different results from repeated evaluations with identical settings.
