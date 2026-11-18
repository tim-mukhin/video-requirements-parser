# real/blender-yt-tSQ5b7zBOa0

_claude-sonnet-5.5@default, 56 s; looked at: frames/0000.0.jpg, frames/0020.0.jpg, frames/0050.0.jpg, frames/0080.0.jpg, frames/0110.0.jpg, frames/0140.0.jpg, frames/0186.0.jpg, frames/0030.0.jpg, frames/0040.0.jpg, frames/0060.0.jpg, frames/0070.0.jpg, frames/0090.0.jpg, frames/0100.0.jpg, frames/0120.0.jpg, frames/0160.0.jpg, frames/0184.0.jpg, frames/0010.0.jpg, frames/0130.0.jpg, frames/0170.0.jpg, frames/0150.0.jpg, frames/0180.0.jpg, frames/0114.0.jpg, frames/0124.0.jpg, frames/0158.0.jpg, frames/0156.0.jpg_

A livestreamed Blender 3.6 beta session where the author builds a Geometry Nodes tree: Curve Circle → Curve to Mesh → Extrude Mesh → Delete Geometry, where Delete Geometry removes faces whose Index equals a typed number. The author changes the index value, mutes Extrude Mesh and toggles 'Individual', and also reads Extrude Mesh source on GitHub. The video suggests the face indices after Extrude Mesh don't match what is expected (especially with Individual), but with no sound and no on-screen text the exact complaint is unclear.

## Delete Geometry by Index after Extrude Mesh removes unexpected faces; behaviour changes with 'Individual' (suspected face-index ordering of extruded faces)

Class: **wrong-data**

Environment: Blender 3.6.0 Beta (version text at bottom right), Geometry Nodes workspace on object 'Cube'. A Spreadsheet is open (Evaluated, Vertex domain, 20 rows). OBS Studio runs for the Twitch stream (frame 0000). Firefox is used for github.com/blender/blender, node_geo_extrude_mesh.cc (frames 0110, 0130). Windows 10, 6/27/2023.

Steps:

1. The node tree is Curve Circle (Resolution 8) → Curve to Mesh (Curve Line profile) → Extrude Mesh (Faces) → Delete Geometry (Face domain, selection = Index == N) → Group Output. The result is a ring with part of the wall cut out and a block sticking out. (00:20.0; 0020.0)
2. Inferred: the author changes the Index Equal value (7 and 8 seen in the Index Equal nodes) and rotates the viewport. The deleted part of the mesh moves. (00:10.0; 0010.0, 0080.0, 0100.0)
3. Inferred: the author mutes Extrude Mesh (greyed out). The mesh becomes a plain ring with fewer vertices (16 rows). Un-muting restores it (20 rows). (00:50.0; 0040.0, 0050.0, 0060.0)
4. Inferred: the author changes the Index Equal value to 11. Different faces are deleted from the ring. (01:54.0; 0114.0)
5. Opens Firefox and the Blender source for node_geo_extrude_mesh.cc. Searches for 'individual', seen at extrude_individual_mesh_faces and the top_id/side_id selection handling. (01:50.0; 0110.0, 0124.0, 0130.0)
6. Back in Blender, ticks 'Individual' on Extrude Mesh. The geometry changes and the same index value now deletes a different face. Later the author unticks it again and changes the index value (8 → 7). (02:36.0; 0156.0, 0158.0, 0170.0, 0180.0)

Expected (implied): Delete Geometry by Index after Extrude Mesh should remove a predictable face. The index order of the extruded faces should be consistent whether or not Individual is enabled. This is implied; there is no sound.

Actual: The faces removed for a given index differ between Individual on and off, and the extruded block appears at a different place in the mesh. The spreadsheet vertex order changes (compare frames 0020 and 0040). The author checks the C++ source, which suggests suspicion about how face indices are ordered or assigned after extrusion.

Key events: 0020.0, 0114.0, 0130.0, 0158.0, 0180.0

Missed by the author:

- Not applicable: no audio, so it is unknown what the author noticed. The spreadsheet row count changes (16 vs 20) when Extrude Mesh is muted (0040, 0050 vs 0060).

Claims:

- "The ticket gives only a title and a stream link; it states no specific claim." [Blender Bug Report 2]: not shown - No concrete defect is stated. The frames show a nodes experiment and source reading. The exact failure is unclear. The likeliest candidate is that Extrude Mesh output face indices are unexpected or inconsistent with Individual toggled.
