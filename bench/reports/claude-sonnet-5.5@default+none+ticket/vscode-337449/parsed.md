# real/vscode-337449

_claude-sonnet-5.5@default, 13 s; looked at: nothing_

In VS Code 1.139.0 on macOS, the mouse cursor reportedly flickers between the pointer (hand) and the default arrow when hovering clickable UI elements, even with the mouse still. The reporter says it happens constantly and makes the editor hard to use. The ticket has no video, so this report rests on the text alone.

## Cursor flickers between pointer and default arrow over clickable UI elements in VS Code on macOS

Class: **intermittent**

Environment: VS Code 1.139.0, macOS (version not given). Affected areas: Activity Bar, Explorer, tabs, buttons. Extension state is unclear: the ticket reads 'Yes/No', so the template was not filled in. Account and organization are not given.

Steps:

1. Open VS Code 1.139.0 on macOS. (00:00.0; )
2. Move the mouse over a clickable element such as the Activity Bar, Explorer, a tab or a button. (00:00.0; )
3. Keep the mouse still and watch the cursor. (00:00.0; )

Expected (implied): The cursor stays a pointer (hand) while over a clickable element and does not change while the mouse is still.

Actual: The cursor keeps switching between the hand pointer and the default arrow while hovering clickable elements, even when the mouse is not moving.

Key events: 

Claims:

- "The flicker happens everywhere in VS Code, on all clickable elements." [anywhere in VS Code (Activity Bar, Explorer, tabs, buttons, etc.)]: not shown
- "The flicker occurs even when the mouse is not moving." [even when the mouse is not moving]: not shown
- "The problem is constant." [This happens constantly]: not shown
