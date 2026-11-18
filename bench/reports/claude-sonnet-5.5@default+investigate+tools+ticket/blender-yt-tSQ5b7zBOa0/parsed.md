# real/blender-yt-tSQ5b7zBOa0

_claude-sonnet-5.5@default, 27 s; looked at: frames/0158.0.jpg_

In Blender 3.6 beta Geometry Nodes, Delete Geometry by Index after Extrude Mesh (Faces) deletes faces in an order that is unclear to the author. With Individual off, face indices follow edge order. With Individual on, they follow a different order that the author cannot describe. The ticket is only a title and a stream link, so the complaint comes from the narration and screen.

## Extrude Mesh face index order is unpredictable when Individual is enabled

Class: **wrong-data**

Environment: Blender 3.6.0 Beta, Geometry Nodes workspace, object 'Cube'. Spreadsheet (Evaluated, Vertex domain). Node tree: Curve Circle (Resolution 8) → Curve to Mesh → Extrude Mesh (Faces) → Delete Geometry (Face domain, selection = Index Equal N) → Group Output. Firefox shows the Blender source on GitHub (extrude mesh node, around line 770). Windows, streamed via Twitch.

Steps:

1. Build Curve Circle (res 8) → Curve to Mesh → Extrude Mesh → Delete Geometry with selection Index == 7. The author says index 7 is the last face of the 8-sided ring and that 8 deletes nothing. (00:39.3; u006, u007, u008)
2. Individual off: the author walks through the face order. It follows the edge order: vertical edges, then bottom, then top. (00:56.3; u010, u014, u018, u024)
3. Open the Blender source in Firefox. The author reads that faces are created by iterating edges in index order. (01:50.5; u025, u027)
4. Return to Blender, set the Index Equal value to 8, and tick Individual on Extrude Mesh. The deleted face and the extrusion layout change (Individual is checked in the 02:38 frame). (02:29.9; u030, u031, p1175)
5. Repeat with different index values. The author cannot find a pattern in which face is removed. (02:45.0; u033, u034, u036, u037)

Expected (implied): With Individual on, the face index order after Extrude Mesh should be predictable and documented, like the edge-ordered case.

Actual: With Individual on, the face indices follow an order the author cannot describe. The same index deletes a different face than with Individual off.

Key events: u006, u018, u024, u031, u035, u036, u038, p1175

Missed by the author:

- The spreadsheet row count changes between 16 and 20 when Extrude Mesh is muted and un-muted. This is expected for muting and is not a defect.

Claims:

- "With Individual off, face indices follow the edge index order." [u024]: confirmed - The narration matches the source read on screen (u027). The deleted faces were not individually checked against it.
- "With Individual on, the order is completely different and 'non-deterministic'." [u038]: not shown - The order does change with Individual. The video does not test repeatability, and the author himself says it is 'not random' (u036), so non-deterministic is the author's characterisation.
- "The ticket gives no concrete claim." [u001]: not shown - The ticket has only a title and a stream link. The defect description comes from the narration.
