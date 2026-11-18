# real/blender-yt-5bCFMDuojZE

_gpt-6-sol@default, 35 s; looked at: frames/0026.0.jpg, frames/0060.0.jpg, frames/0080.0.jpg, frames/0134.0.jpg, frames/0178.0.jpg, frames/moments/p329.jpg, frames/moments/p659.jpg, frames/0190.0.jpg, frames/0062.0.jpg_

Blender's Geometry Nodes editor responds slowly to selection and node movement in a large node tree. The video shows a useful contrast: interaction is quicker after the node count is reduced to 8,000, then becomes sluggish again as nodes are added.

## Geometry Nodes editor lags when navigating and selecting in a large node tree

Class: **stuck**

Environment: Blender 3.4.1, Geometry Nodes workspace, bug 7.blend; Cube selected with a Geometry Nodes modifier and Node Counter visible.

Steps:

1. With the Node Counter showing 47,990, start a box selection in the Geometry Nodes editor; the selection remains active through 01:02.8 as the author demonstrates the delay. (00:58.6; p244, p245, p256, u015, u016)
2. Reduce the node count to 8,000 and repeat selection and movement in the editor; responses are visibly quicker. (01:18.4; p326, p329, p333, p346, p353, u021)
3. Restore and add nodes to reach 55,988, then box-select again; the selection started at 03:11.7 does not visibly complete until 03:14.5. (03:11.7; p396, p578, p892, p896, p901, p904, p905)

Expected (speech): Selection, dragging and other node-editor interactions should respond promptly even in a large tree.

Actual: At high node counts, the editor visibly lags during selection and movement. At 8,000 nodes, comparable interactions are quicker. The empty viewport is a separate observation, not the demonstrated failure: the large network is disconnected from the node wired to Group Output.

Key events: p244, p256, p262, p326, p329, p396, p578, p892, p901, p905, p969

Missed by the author:

- The screen shows zero evaluated mesh vertices and a large network disconnected from the node wired to Group Output; this explains the absent humanoid, which the frame-only watcher treated as the likely problem, but does not explain the demonstrated editor lag [p969, p1201].
- The short-lived redraw around 02:51.3 is visible in the moment frames, but it does not establish a separate wrong-data or output failure [p659, p684].

Claims:

- "The project has more than 14,000 nodes." [u001]: confirmed - The on-screen Node Counter shows 47,990 initially and 55,988 later; the video does not establish that all are humanoid-producing nodes.
- "Editor interaction gets slower as the node count increases." [u029]: confirmed - The timeline's selection states and the frames show quicker interaction at 8,000 nodes than during the later 55,988-node box selection.
- "The added network is not connected to the output." [u002]: confirmed - The frames show the large network separate from the small node wired to Group Output.
- "The delay has nothing to do with output evaluation time." [u045]: not shown - A Group Output timing of about 0.96 ms is visible, but the video does not isolate the cause of the editor delay.
