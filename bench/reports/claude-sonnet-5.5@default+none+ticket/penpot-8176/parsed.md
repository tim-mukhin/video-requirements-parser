# real/penpot-8176

_claude-sonnet-5.5@default, 14 s; looked at: nothing_

In Penpot, Hug Content and Fill containers inside a flex layout do not resize correctly when interactions change the layout, such as removing an element or extending the card content. The UI shows the settings as applied, but the rendering does not follow them, so interactive prototypes with flex cards look wrong.

## Flex layout Hug Content and Fill do not update after interaction-triggered layout changes

Class: **wrong-data**

Environment: Penpot (web) in Google Chrome 143.0.7499.193 on macOS. The Penpot version, account and organization are not given.

Steps:

1. Create a card with a flex layout that contains other flex elements, such as text, images or buttons, with Hug Content and Fill sizing set. (00:00.0; )
2. Trigger an interaction that changes the layout, for example removing an element or extending the card content. (00:00.0; )
3. Observe the card and its children: the Hug and Fill sizing does not update correctly, even though the UI shows it as applied. (00:00.0; )

Expected (speech): Hug Content and Fill containers update and resize correctly when interactions are triggered.

Actual: After an interaction changes the layout, Hug Content and Fill containers do not resize or re-render correctly. The sizing settings still appear as applied in the UI.

Key events: 

Claims:

- "Hug and Fill settings show as applied in the UI but are not honoured in the rendering after interactions." [The Hug and Fill settings do not update correctly, even though they appear as applied in the UI.]: not shown - There is no recording available. The ticket text is the only source.
