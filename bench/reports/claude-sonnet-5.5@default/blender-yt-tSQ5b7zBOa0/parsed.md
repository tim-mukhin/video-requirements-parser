# real/blender-yt-tSQ5b7zBOa0

_claude-sonnet-5.5@default, 46 s; looked at: nothing_

In Blender 3.6 Beta Geometry Nodes, a curve-to-mesh cylinder goes through Extrude Mesh and then Delete Geometry (Face) with Index == B. The author says the faces created by the extrusion are indexed in an order that is hard to predict. With Individual off, the order follows the edge indices. With Individual on, the order is completely different, and the author calls it non-deterministic. The video shows the order differs between the two modes, but it never shows the behaviour changing from run to run on identical settings.

## Extrude Mesh: face index order of the new faces is unpredictable (follows edge indices, and changes completely with Individual on)

Class: **wrong-data**

Environment: Blender 3.6.0 Beta on Windows (taskbar clock dated 6/27/2023). Geometry Nodes workspace with a Cube object and a GeometryNodes modifier. Node graph: Curve Line, Curve Circle (Resolution 8, Radius 1 m), Curve to Mesh, Extrude Mesh (Faces mode, Offset Scale 1.0), Delete Geometry (Face domain), and an Integer Equal (Compare) node fed by Index. Spreadsheet open. A Firefox tab showing node_geo_extrude_mesh.cc#L770 on GitHub.

Steps:

1. Build the graph: Curve Line and Curve Circle (Resolution 8) go into Curve to Mesh, then Extrude Mesh, then Delete Geometry (Face). The deletion Selection is Index Equal B. The author builds this in the first part of the video. (00:14.0; p104, p110, p123, p156, p196)
2. Show that Index B = 7 deletes face 7, and that raising B to the last index (curve resolution 8) leaves nothing deleted. (00:39.3; u006, u007, u008, p545)
3. Open the spreadsheet face domain to show the numbering of the edges: the vertical edges first, then the bottom ones, then the top ones. (00:56.3; u010, u011, u012, u013, u014)
4. Turn Individual off, so faces are extruded as one region, and step B through 7, 8, 9, 10, 11. The deleted faces follow the edge index order, not the face index order. (01:20.1; u016, u018, u019, u021, u022, u023, u024, p922, p925)
5. Read the extrude source at node_geo_extrude_mesh.cc line 770. The author says it iterates the original edges in index order. (01:50.5; u025, u026, u027, p1014, p1086, p1087)
6. Return to Blender and set Individual back to on. The author says the faces then go in a completely different order, and steps B through values 9, 10, 11 and so on. (02:30.4; u031, p1180, p1181, p1393, p1396)
7. Repeatedly change B and click around the viewport. The author concludes the order is not random but that he cannot describe it, and that it is non-deterministic. (02:51.8; u035, u036, u037, u038, p1493, p1502, p1510)

Expected (implied): The author implies that face indices of an extruded mesh should be predictable, so that Index == N in Delete Geometry removes a predictable face. The video does not state this explicitly.

Actual: With Individual off, the new side faces get indices that follow the original edge order, so they are not in a simple face order. With Individual on, the order is described as completely different and hard to predict. The author could not find a rule for the order.

Key events: u006, u008, u024, u025, u027, u031, u035, u036, u038, p1014, p1180, p1181

Missed by the author:

- The Extrude Mesh node is shown as a duplicated or flickering node for a moment during several rebuilds, for example p623-p654. This is probably a UI redraw and not related to the face ordering.

Claims:

- "With Individual off, extruded faces are created following the edge indices." [u024]: confirmed - The Delete Geometry results move with B in the same way as the edge numbering shown in the spreadsheet. The source view at p1014 and p1086-p1087 shows the loop over the original edges in index order (read from OCR).
- "The code is on line 770 of node_geo_extrude_mesh.cc, and it gets the edges in order of index." [u027]: confirmed - The GitHub URL ending in #L770 is visible (p1014), and the OCR text of the code scrolled past shows a loop over orig_edges.index_range() (p1086).
- "With Individual on, the order is completely different." [u031]: not shown - The toggle click is seen (p1180, p1181), but the OCR is too noisy to check the resulting order. The author never states the order.
- "It picks one randomly, so it is non-deterministic." [u035]: refuted - The author himself says in u036 that it is not random, and the video never repeats an identical setup to show a different result. Only different settings give different results.
