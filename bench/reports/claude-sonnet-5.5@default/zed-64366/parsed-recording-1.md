# real/zed-64366

_claude-sonnet-5.5@default, 24 s; looked at: frames/000117.jpg, frames/000527.jpg_

The video shows the Zed project panel (jellyfin-web, src folder, Ubuntu) on the right edge of the window. The author repeatedly opens the right-click context menu and scrolls the file list. The panel flickers: context-menu items flash and vanish, and the list jumps between scroll positions. One folder label, 'strings', first reads as garbled and then reverts by itself. The cause is not visible, and the author says almost nothing (one word, 'you').

## Zed project panel flickers and jumps: context-menu items flash, a row label reverts by itself, and the tree scroll position shifts

Class: **intermittent**

Environment: Zed editor on Ubuntu, project jellyfin-web, branch main / fix/tizen-pause-key, project panel showing src/ (folders and files). A 'Restart to Update' button is in the title bar. config.json is drawn greyed out.

Steps:

1. Open the project panel's context menu (New File, New Folder, Reveal in File Manager, Find in Folder... and so on) by right-clicking an entry. The trigger is not visible, because keys and right-clicks are not seen. The menu items flash and disappear several times within about 2 s. (00:00.1; p001, p008, p009, p016, p017, p024)
2. Click in the tree at [1178, 456]. The tree re-renders with a different layout, and a flash of 'elements' appears. (00:03.8; p031, p032, p033)
3. Click 'constants'. The context menu appears again, then its items flash and vanish. (00:04.9; p037, p038, p041, p047, p048, p049)
4. Click in the tree at [1173, 535], then click 'hooks' three times. The context menu opens again and its entries flash. The 'Find in Folder' label also appears distorted ('Find in Foldqr'). (00:11.0; p067, p070, p071, p072, p073, p076, p077)
5. Scroll the panel by clicking its scrollbar at [1816, 436]. The list jumps: the folder rows move out of view and then reappear. (00:15.9; p098, p099, p100, p101)
6. Click config.json. The tree jumps to a scrolled position, and the row 'strings' first shows garbled text ('Jrin ins') and then reverts to 'strings' after 0.3 s with no click. (00:17.5; p102, p103, p104, p105)
7. Click apiclient.d.ts. The context menu opens again and flickers. Repeat the same with index.html, and 'Open in Default App' flashes before being clicked. (00:18.4; p107, p109, p110, p119, p120, p124, p125, p126, p129)

Expected (implied): The project panel should stay stable. Context-menu items should render once and stay until dismissed. Tree rows and labels should not flicker, garble, or change by themselves. The scroll position should not jump.

Actual: Context-menu entries (New File, Ctrl-N, Delete, Find in Folder and others) repeatedly flash on and off for 0.2–0.8 s. Icons inside the menu lose their drawing. A tree row label garbles and reverts by itself. The tree list jumps between scroll positions. A small 'Z'-like artifact flashes in the bottom-left of the editor area.

Key events: p105, p009, p017, p024, p088, p033, p099, p103, p126

Missed by the author:

- 'Jrin ins' reverted to 'strings' after 0.3 s with no click (p105, cross-check).
- Context-menu items flashed and disappeared within a fraction of a second, repeatedly (p017–p021, p047–p049, p059–p061, p088–p089).
- A 'Z'-like artifact appeared and disappeared in the bottom-left of the editor area throughout the video (p002, p056, p057, p086, p087, p111, p114, p131, p132).
