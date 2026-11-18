# real/commons-blender-amd-normals

_claude-sonnet-5.5@default, 29 s; looked at: frames/0000.0.jpg, frames/0010.0.jpg, frames/0020.0.jpg, frames/0030.0.jpg, frames/0040.0.jpg, frames/0052.0.jpg, frames/0017.0.jpg, frames/0025.0.jpg_

In Blender, the 3D viewport shows a scene with a ground floor. In Material Preview (shading mode inferred from the header) the shading is garbled: smeared, blurry, with dotted, scattered coloured lights and dark surfaces. In Rendered/Cycles view (around 17–20 s) the scene renders correctly, with noise. This matches the ticket's AMD driver normals bug, but the video alone cannot show the cause.

## Blender 2.9 viewport shading is garbled in Material Preview (AMD driver normals bug)

Class: **wrong-data**

Environment: Blender 2.9x on Windows (Windows file browser visible at left; folder path under C:\Users\...\Documents). Viewport in User Perspective, object Ground.001 selected in the outliner, Floor material with a concrete_floor_02_diff_4k.png image texture, Bright/Contrast and Mix nodes feeding a Principled BSDF. The Properties editor shows View Layer passes. The GPU/driver is not visible; the ticket says AMD.

Steps:

1. Open the scene in Blender with Ground.001 selected and the viewport in Material Preview. The scene is shown with smeared, blurry shading and dotted coloured light artifacts instead of a textured scene. (00:00.0; 0000.0)
2. The artifacts keep changing as the view moves (inferred from the changing framing). The shading stays wrong. (00:10.0; 0010.0)
3. The viewport shading appears to be switched to Rendered (Cycles). It shows 'Updating Images', and the viewport is briefly empty. (00:17.0; 0017.0)
4. The Cycles render ('Path Tracing Sample 2/16') shows the grass and the concrete geometry correctly, with only sampling noise. (00:20.0; 0020.0)
5. The viewport returns to Material Preview. The surfaces are flat dark grey with no texture or lighting. (00:25.0; 0025.0)
6. Material Preview shows smeared, garbled surfaces again. (00:30.0; 0030.0)
7. Dotted, glowing coloured artifacts remain in Material Preview. (00:40.0; 0040.0, 0052.0)

Expected (implied): Material Preview should show the textured floor and walls with correct lighting and normals, as the Rendered view does.

Actual: Material Preview shows distorted, blurry shading with dotted rainbow-coloured light speckles and dark or flat surfaces. The Rendered view is correct at 20 s.

Key events: 0000.0, 0020.0, 0030.0, 0040.0

Missed by the author:

- At 20 s the Rendered (Cycles) view is correct while Material Preview is broken, so the glitch is specific to the preview shading mode (0020.0).
- At 25 s Material Preview shows flat dark grey surfaces with no texture (0025.0).

Claims:

- "Bug is caused by AMD drivers" [introduced by an update to some AMD drivers]: not shown - No GPU or driver information is visible in the frames.
- "Eevee glitch related to High Quality Normals" [If you used Eevee, this had to do with not using High Quality Normals]: not shown - The render settings are not opened. A Cycles-style 'Path Tracing Sample' overlay appears in the Rendered view.
- "Some people got this on Cycles too" [Some people got this error on Cycles too]: refuted - In this video the Rendered view at 20 s looks correct. Only Material Preview is garbled.
- "The program did not crash" [without the program crashing]: confirmed - Blender stays responsive throughout the 52 s.
