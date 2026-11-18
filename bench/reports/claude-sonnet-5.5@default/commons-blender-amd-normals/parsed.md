# real/commons-blender-amd-normals

_claude-sonnet-5.5@default, 29 s; looked at: frames/000857.jpg, frames/001375.jpg, frames/001453.jpg, frames/003097.jpg, frames/002691.jpg_

In Blender (a project file, V#19019), the 3D viewport first renders the scene normally in Cycles Rendered mode. After the author switches it to Material Preview and orbits/pans the view, the viewport shows a garbled picture: smeared geometry and coloured speckles. Only a single short remark of speech is heard, and it says nothing about the problem.

## Viewport shows corrupted shading with coloured speckles after switching from Rendered to Material Preview (AMD, normals)

Class: **wrong-data**

Environment: Blender with the file path C:\Users\P...\Documents, 3D viewport on top, Shader Editor below (material 'Floor', concrete_floor_02_diff_4k.png), Outliner with Ground.001 selected. Cycles Path Tracing in the viewport. The folder name suggests an AMD GPU, but no hardware is visible.

Steps:

1. With Ground.001 selected, the viewport starts the Rendered mode (the tooltip reads 'Method to display/shade objects: Rendered'). 'Initializing', 'Updating Shaders', 'Updating Images' and 'Updating Lights' messages follow. (00:14.1; p064, p065, p069, p071, p073)
2. Cycles path tracing converges (samples 1/16 up to 13/16). The scene renders correctly: textured concrete, grass, walls. (00:19.5; p074, p081, p082)
3. The viewport shading changes to Material Preview (tooltip 'Material Preview'). The click is not visible, because the video shows no cursor. (00:24.2; p082, p083)
4. The user orbits and pans the view (Rotate View/Pan View hints). The viewport turns into a blurry, smeared scene with bright coloured dots and a dark dotted grid pattern. The viewport tooltip text gives no error. (00:44.8; p250, p267, p269)

Expected (implied): The viewport shows a clean Material Preview of the scene, with correct lighting and normals, like the earlier Rendered view.

Actual: The final Material Preview frames show a blurred, distorted scene with coloured light speckles and dotted patterns. No error message is shown.

Key events: p082, p250, p267, p269, p270

Missed by the author:

- The only utterance 'Thank you.' (u002) is unrelated, so the author never describes the corruption.
- At 00:14.2 the tooltip text changed from 'Rendered' to 'Camera | Ground' within 0.1 s with no visible click [p067]. This is a tooltip closing, not a mode change.
- Cycles samples are set to 16 (13/16 visible), so the Rendered view converges only to a low sample count [p082].
