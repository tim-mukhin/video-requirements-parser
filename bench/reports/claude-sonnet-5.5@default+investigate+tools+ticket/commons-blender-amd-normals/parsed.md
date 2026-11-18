# real/commons-blender-amd-normals

_claude-sonnet-5.5@default, 24 s; looked at: frames/0010.0.jpg, frames/0020.0.jpg_

In Blender, the 3D viewport in Material Preview shows garbled shading: smeared surfaces, a dotted grid pattern and coloured light speckles. After the author switches to Rendered (Cycles), the same scene looks correct, with sampling noise only. When they switch back to Material Preview, the artifacts return. The video points to a viewport/GPU-driver rendering fault in the preview mode. The ticket attributes it to an AMD driver update, but the video cannot show that.

## Blender 2.9 Material Preview viewport shading is garbled, while the Rendered (Cycles) view of the same scene is correct

Class: **wrong-data**

Environment: Blender 2.9x, with a Windows file browser at left (C:\Users\P...\Documents), the 3D viewport in User Perspective, a node editor and a Properties editor (View Layer passes) with Ground.001 selected. The Floor material has concrete_floor_02_diff_4k.png feeding Bright/Contrast, then Mix, then Principled BSDF. The GPU and driver are not visible.

Steps:

1. Start with the Floor scene in Material Preview (the viewport header shows Material Preview as the active mode). The viewport shows smeared surfaces, a dotted grid pattern and coloured light speckles instead of a textured floor and walls. The view also changes continuously while it is orbited or panned. (00:10.0; p060, p061)
2. Switch the viewport shading to Rendered. A tooltip 'Method to display/shade objects in the 3D View: Rendered' is visible just before, and the status shows Initializing, Updating Shaders, Updating Geometry BVH and Updating Images. The click itself is not visible because no cursor is shown. The tooltip vanishing at 14.2 s is the tooltip closing, not a mode reverting. (00:14.1; p066, p067, p071, p072, p073)
3. Cycles renders the scene correctly. The grass, the concrete walls and the floor are all correct, with only sampling noise ('Path Tracing Sample 2/16' up to 13/16). (00:19.5; p076, p081, p083)
4. Switch back to Material Preview (tooltip 'Material Preview' at 24.2 s). The garbled, dotted shading returns and stays through the end of the video at about 52 s. The surfaces are dark or flat at about 25 s. (00:24.2; p084, p085, p086)

Expected (implied): Material Preview should show the textured floor and walls with correct lighting and normals, as the Rendered view does.

Actual: Material Preview shows distorted, blurry shading with a dotted pattern, rainbow speckles and dark surfaces. Rendered at about 20 s is correct, so the fault is in the viewport preview path. There is no error message and no crash.

Key events: p060, p066, p076, p081, p084, p085

Missed by the author:

- At about 14.2 s the timeline flags the Rendered tooltip as 'went back by itself' (p069). The tooltip text changing is just the tooltip closing, not a bug.
- The Rendered view at about 20 s is correct while Material Preview is wrong, so the fault is specific to the preview shading (p076, p081).

Claims:

- "The bug was introduced by an update to some AMD drivers" [ticket]: not shown - No GPU or driver information is visible. The video shows only the symptom.
- "In Eevee it relates to not using High Quality Normals" [ticket]: not shown - The render settings that would show this are not opened. The ticket text is the only source for this.
- "Some people also got this error on Cycles" [ticket]: refuted - This is a claim about other people. In this video the Cycles Rendered view at about 20 s is correct, and only Material Preview is garbled.
- "Recorded without the program crashing" [ticket]: confirmed - Blender keeps responding for the whole recording.
