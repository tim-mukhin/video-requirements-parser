# real/lo-174415

_claude-sonnet-5.5@default, 43 s; looked at: frames/0000.0.jpg, frames/0005.0.jpg, frames/0010.0.jpg, frames/0015.0.jpg, frames/0020.0.jpg, frames/0025.0.jpg, frames/0030.0.jpg, frames/0035.0.jpg, frames/0040.0.jpg, frames/0045.0.jpg, frames/0050.0.jpg, frames/0055.0.jpg, frames/0061.0.jpg, frames/0012.0.jpg, frames/0038.0.jpg, frames/0042.0.jpg, frames/0052.0.jpg, frames/0058.0.jpg, frames/0018.0.jpg, frames/0043.0.jpg, frames/0048.0.jpg_

In the Pivot Table Layout dialog, the auto-generated Data field stays in Column Fields when dragged toward Row Fields. The same move works on the sheet (Data ends up in the row area), and the dialog then shows Data under Row Fields. The video supports the ticket, but the ticket's description of the workaround is only partly visible.

## Pivot Table Layout dialog: Data field cannot be dragged from Column Fields to Row Fields

Class: **silent-fail**

Environment: LibreOffice Calc (file 'Calculated Fields in Pivot Table in LibreOffice Calc.ods'), Windows-style UI. Source data A1:F25 (Date, Region, Salesperson, Product, Sales, Cost). The version number is not visible in the frames, so the ticket's 26.8 is not confirmed.

Steps:

1. Select A1:F25 and open the Pivot Table Layout dialog (Insert > Pivot Table, inferred). The dialog opens with an auto-generated 'Data' item in Column Fields. (00:05.0; 0005.0, 0015.0, 0018.0)
2. Drag 'Data' from Column Fields toward Row Fields (drag inferred from the cursor and selection). It stays in Column Fields; no error is shown. (00:10.0; 0010.0, 0012.0)
3. Reopen the dialog and build the layout: Salesperson in Filters, Region in Rows, Sum - Sales and Sum - Cost in Data Fields. Click OK. (00:25.0; 0020.0, 0025.0, 0030.0, 0035.0)
4. The pivot table is created with Data in the column header row. Reopen the layout dialog: Data is still in Column Fields and a drag to Row Fields has no effect. (00:38.0; 0038.0, 0040.0, 0042.0, 0043.0)
5. On the sheet, drag the 'Data' header (probably with Ctrl held, as the ticket says; the key is not visible). The pivot reorganises with Data in the rows. (00:45.0; 0045.0, 0048.0, 0050.0)
6. Reopen the layout dialog: Data is now listed under Row Fields, above Region. (00:55.0; 0052.0, 0055.0, 0058.0)

Expected (implied): The Data field can be dragged from Column Fields to Row Fields inside the dialog, as it can on the sheet.

Actual: Dragging Data inside the Pivot Table Layout dialog does nothing and shows no message. Moving it on the sheet works.

Key events: 0010.0, 0012.0, 0043.0, 0050.0, 0055.0

Missed by the author:

- The drag already fails at 0012.0 on the empty layout, before any Sales or Cost data fields are added, so more than one data field is not required.
- After the sheet drag, Data appears in the dialog's Row Fields (0055.0), so the dialog can display Data in rows. Only the drag inside the dialog fails.

Claims:

- "Data cannot be moved from Column Fields to Row Fields in the dialog" [ticket]: confirmed - Data stays in Column Fields after the drag attempts (0012.0, 0043.0).
- "No error appears" [ticket]: confirmed - No message is shown in any frame.
- "The Data field can be moved on the worksheet by Ctrl+drag" [ticket]: confirmed - Data moves to the rows (0050.0, 0055.0). The Ctrl key itself is not visible.
- "Removing the Data field makes it return to Column Fields when the dialog is reopened" [ticket]: not shown - The video never removes the Data field.
- "The Calc Guide documents moving the Data field between Column and Row Fields" [ticket]: not shown - The guide is not shown.
- "Reproducible with Sales and Cost in Data Fields" [ticket]: not shown - The failed drag at 0012.0 happens before any data fields are added. It also fails afterwards (0043.0), so the failure does not depend on them.
