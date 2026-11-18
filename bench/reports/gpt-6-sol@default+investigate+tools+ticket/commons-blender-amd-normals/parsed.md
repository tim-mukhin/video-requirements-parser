# real/commons-blender-amd-normals

_gpt-6-sol@default, 42 s; looked at: frames/0012.0.jpg, frames/0021.0.jpg, frames/0025.0.jpg, frames/0030.0.jpg, frames/moments/p090.jpg, frames/moments/p066.jpg, frames/0036.0.jpg, frames/0042.0.jpg, frames/0044.0.jpg, frames/0049.0.jpg, frames/moments/p207.jpg, frames/moments/p181.jpg, frames/moments/p067.jpg, frames/0033.0.jpg, frames/0039.0.jpg, frames/0024.0.jpg, frames/0014.5.jpg_

Blender's Material Preview displays a concrete scene as dark, untextured surfaces that become distorted and speckled as the view moves. The same scene appears textured and coherent in the rendered viewport, so Material Preview cannot be used to inspect it reliably.

## Material Preview corrupts concrete scene while rendered viewport looks normal

Class: **wrong-data**

Environment: Blender 3D viewport and Shader Editor; Ground.001 is selected and its Floor material includes a concrete image texture. Blender version, GPU, driver and High Quality Normals setting are not visible.

Steps:

1. Open the scene in rendered viewport shading (the trigger is not visible); the concrete floor and walls render normally. (00:14.1; p066, p067, p076, p081)
2. Open Material Preview shading (the trigger is not visible). (00:24.2; p084, p085)
3. Move the viewport around the scene (the input is not visible). (00:29.2; p097, p104, p124, p168)

Expected (implied): Material Preview should show the scene's surfaces and geometry coherently as the view moves.

Actual: At 24.6 s the scene becomes a mostly dark, untextured silhouette. As the view moves, surfaces appear clipped or stretched and develop bright patches and colored speckles; the selected floor's orange outline remains visible. The frames establish the visual corruption, while the timeline identifies the shading change and subsequent movement [p085, p090, p104, p115, p168].

Key events: p076, p081, p084, p085, p090, p104, p115, p168

Missed by the author:

- The rendered viewport provides a working comparison immediately before Material Preview fails [p076, p081, p084, p085].
- The Floor material's concrete image texture remains present in the Shader Editor while the preview fails to display it [p085].
- The brief disappearance of the Rendered-shading tooltip at 14.2 s accompanies viewport initialization, not an observed shading-mode revert; the moment frames settle this apparent timeline anomaly [p066, p067, p069].

Claims:

- "The recording captures a visual bug without Blender crashing." [ticket]: confirmed - The viewport is visibly corrupted in Material Preview, and Blender remains open through the end of the recording.
- "An AMD driver update introduced the issue around Blender 2.9." [ticket]: not shown - Neither the Blender version nor GPU or driver details are shown.
- "In Eevee the issue depends on High Quality Normals being disabled." [ticket]: not shown - The recording does not show the render-engine selection or that setting.
- "Other users encountered the issue in Cycles and needed older AMD drivers." [ticket]: not shown - The rendered viewport works in this recording; other users' results and driver rollbacks are not tested.
- "Blender 2.91.2 fixed the issue, and AMD Pro drivers might be unaffected." [ticket]: not shown - There is no version or driver comparison.
