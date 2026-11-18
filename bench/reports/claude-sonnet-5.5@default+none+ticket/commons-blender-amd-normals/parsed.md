# real/commons-blender-amd-normals

_claude-sonnet-5.5@default, 15 s; looked at: nothing_

In Blender 2.9, an AMD driver update caused a normals rendering glitch, with Eevee when High Quality Normals was off and sometimes with Cycles. The ticket does not describe the visible symptoms. It was fixed in Blender 2.91.2, but without the video the exact behavior can't be confirmed.

## Blender 2.9: incorrect normals rendering on AMD GPUs after a driver update

Class: **wrong-data**

Environment: Blender 2.9 (Eevee, sometimes Cycles) on AMD GPU with a driver update. AMD Pro drivers possibly unaffected but untested. The recording shows a PolyHaven CC0 texture. Recorded with OBS. The OS and driver version are not stated.

Steps:

1. Install an affected AMD driver update and run Blender 2.9. (00:00.0; )
2. In Eevee, leave High Quality Normals disabled (or use Cycles) and display a textured object with normals, such as the PolyHaven texture in the video. (00:00.0; )
3. Observe the viewport or render. The ticket does not say what is wrong. (00:00.0; )

Expected (implied): Surface normals and shading render correctly.

Actual: Normals render incorrectly (a glitch or artifact). The exact appearance is not described. Some users saw the same glitch in Cycles, and older drivers were the only workaround there.

Key events: 

Claims:

- "The bug came from an AMD driver update around the time of the Blender 2.9 release." [a bug introduced around the time of Blender 2.9's release by an update to some AMD drivers]: not shown - No video is available. This is the reporter's assertion.
- "With Eevee, enabling High Quality Normals avoids the bug." [If you used Eevee, this had to do with not using High Quality Normals.]: not shown - This is the reporter's assertion and cannot be checked from the ticket.
- "It was fixed in Blender 2.91.2." [it ended up being fixed in the Blender 2.91.2. release]: not shown - The ticket links the fix, but I did not verify it.
- "AMD Pro drivers were free of the glitch." [I believe AMD Pro line drivers were free of this glitch, but couldn't test it.]: not shown - The reporter says this is untested.
