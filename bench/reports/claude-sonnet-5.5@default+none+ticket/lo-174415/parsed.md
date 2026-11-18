# real/lo-174415

_claude-sonnet-5.5@default, 15 s; looked at: nothing_

In LibreOffice Calc 26.8, the automatically generated Data field in the Pivot Table Layout dialog can't be dragged from Column Fields to Row Fields. Nothing happens and no error appears. The user can't show data values vertically from the dialog, though a Ctrl+drag on the worksheet works.

## Calc Pivot Table Layout dialog: Data field cannot be dragged from Column Fields to Row Fields

Class: **silent-fail**

Environment: LibreOffice Calc 26.8 (OS not stated). Pivot Table Layout dialog with Sales and Cost in Data Fields. User profile not reset. No accounts or organizations involved.

Steps:

1. Open Calc and create a Pivot Table from a dataset. (00:00.0; )
2. Add Sales and Cost to the Data Fields area. (00:00.0; )
3. Open the Pivot Table Layout dialog. (00:00.0; )
4. Drag the automatically generated Data field from Column Fields to Row Fields. (00:00.0; )

Expected (speech): The Data field moves from Column Fields to Row Fields, so data values display vertically instead of horizontally.

Actual: The Data field does not move and no error message appears. If the Data field is removed, reopening the dialog restores it to Column Fields. The report says this happens every time and with different field configurations.

Key events: 

Claims:

- "The Data field can be moved on the worksheet with Ctrl+drag." [I can successfully move the Data field directly on the worksheet by holding Ctrl and dragging it into the row area of the Pivot Table.]: not shown - Ticket text only, no video.
- "The Calc Guide documents moving the Data field between Column Fields and Row Fields." [The LibreOffice Calc Guide documents that the Data field can be moved between Column Fields and Row Fields.]: not shown - Ticket text only, no video; the Guide was not checked.
- "The problem is reproducible every time." [Reproducible: Always]: not shown - Ticket text only, no video.
