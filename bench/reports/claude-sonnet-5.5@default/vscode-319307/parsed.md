# real/vscode-319307

_claude-sonnet-5.5@default, 27 s; looked at: frames/000313.jpg, frames/000183.jpg, frames/000345.jpg_

The author repeatedly drags the 'Farewell message' chat pane in a two-pane split view of the Sessions window, with a drop overlay shown. The panes swap and flicker several times, and the video ends with the order reversed from the start. The video has no audio, so the intended problem is unstated. The most likely issue is unreliable or flickering drag-and-drop reordering of chat panes.

## Dragging a chat pane in a split view makes the panes flicker and swap unpredictably

Class: **intermittent**

Environment: VS Code Sessions window, workspace vscode-distro, branch setting-important (+5 -5). Two chat panes, 'Farewell message' (Bye / Goodbye!) and 'User greeting' (Hello? / Hi! How can I help you?), plus a Changes panel with index.src.js. Model Claude Opus 4.6 (Internal only). Each pane shows an MCP server 'paypal' notice.

Steps:

1. Start with 'Farewell message' as the left pane and 'User greeting' as the right pane. (00:00.0; p001)
2. Click the 'Farewell message' pane header at (431, 86) to start a drag. A drag ghost appears and the layout flashes. (00:02.0; p006, p007, p008)
3. The panes re-render and the 'Farewell message' title flashes, then a new click on it follows. (00:03.7; p014, p015, p017)
4. Click the title again. A drag ghost 'Farewell message' and a grey drop overlay cover the right pane while the pane contents are swapped. (00:04.5; p018, p020, p021)
5. Two more click-and-drag attempts follow, the last at (1451, 320), and the layout flashes again. (00:05.3; p023, p028, p029)
6. The pane contents are re-rendered with their titles and messages replaced. The final layout has 'User greeting' on the left and 'Farewell message' on the right, the reverse of the start. (00:07.7; p034, p035, p036, p046, p047)

Expected (implied): One drag moves the pane to the chosen slot once, with a stable layout and no flicker.

Actual: Each drag makes the panes flash and re-render. Titles and contents change place several times, and the final order differs from the start. The cursor is not followed in the last second, so the drop at the end is not visible.

Key events: p006, p018, p021, p028, p034, p046, p047, p051, p052

Missed by the author:

- The panes re-render with several flashes and 'Bye'/'Hello?' text swapping (p018, p029, p031, p043, p045).
- The window title still says 'Farewell message' at the end. The sidebar still highlights 'Farewell message' even though 'User greeting' is now the left pane (p005, p030).
- Icons in the pane header controls vanish in the last 0.5 s (p050, p051, p052).
