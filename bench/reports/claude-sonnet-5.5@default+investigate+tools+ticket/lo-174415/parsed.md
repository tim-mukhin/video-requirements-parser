# real/lo-174415

_claude-sonnet-5.5@default, 42 s; looked at: frames/0043.0.jpg, frames/0058.0.jpg, frames/0010.0.jpg, frames/0055.0.jpg, frames/0061.0.jpg, frames/0050.0.jpg, frames/0012.0.jpg, frames/0038.0.jpg_

In Calc's Pivot Table Layout dialog, the auto-generated 'Data' field stays in Column Fields when dragged to Row Fields, and no error appears. The same move works by dragging the Data header on the sheet, and the dialog then shows Data under Row Fields. The video supports the ticket's core claim.

## Pivot Table Layout dialog: Data field cannot be dragged from Column Fields to Row Fields (silent)

Class: **silent-fail**

Environment: LibreOffice Calc, file 'Calculated Fields in Pivot Table in LibreOffice Calc.ods'. Source data A1:F25 (Date, Region, Salesperson, Product, Sales, Cost). The version is not visible, so the ticket's 26.8 is not confirmed. No speech beyond 'Thank you.'.

Steps:

1. Select A1:F25, open Insert > Pivot Table, accept 'Current selection'. The Pivot Table Layout dialog opens with 'Data' already in Column Fields. (00:04.3; p013, p034)
2. Drag 'Data' from Column Fields toward Row Fields. The dialog stays empty apart from Data in Column Fields, and no message appears. This happens on an empty layout, before any data fields exist. (00:09.6; p067, p070)
3. Build the layout: Salesperson in Filters, Region in Row Fields, Sum - Sales and Sum - Cost in Data Fields. Click OK. The pivot is created with 'Data' in the column header row. (00:35.5; p134, p138, p147, p151, p158)
4. Reopen the layout dialog (right-click pivot > Properties). Data is still in Column Fields with Region in Row Fields. (00:40.5; p186, p189)
5. Try the drag again inside the dialog. Data stays in Column Fields. The dialog is closed with OK. (00:42.7; p204, p207, p212)
6. On the sheet, drag the 'Data' header into the row area (Ctrl is not visible). The pivot reorganises with Data in the rows. (00:45.9; p226, p230, p233)
7. Reopen the dialog. Data now appears under Row Fields above Region, so the dialog can display Data in rows. (00:54.9; p248, p250)

Expected (implied): Dragging Data from Column Fields to Row Fields in the dialog moves it, as it does on the sheet.

Actual: The dialog drag has no effect and shows no error. Data stays in Column Fields (frames 0012.0, 0043.0). Moving it on the sheet works (0050.0), and the dialog then lists it under Row Fields (0055.0, 0058.0).

Key events: p067, p189, p207, p233, p250

Missed by the author:

- The first drag already fails on the empty layout, before Sales and Cost are added (p067).
- After the sheet move, the dialog shows Data under Row Fields (frames 0055.0, 0058.0), so the dialog can represent Data in rows. Only the drag inside it fails.
- Between 55.8 s and 58.3 s further drags inside the dialog were made, and the final sheet at 61.2 s shows Region before Data (p267). So a reorder within Row Fields seems to work, but this is not fully verified.

Claims:

- "Data cannot be moved from Column Fields to Row Fields in the dialog" [ticket]: confirmed - Data stays in Column Fields after the drags at 9.6 s and 42-43 s.
- "No error message appears" [ticket]: confirmed - No message appears in any frame checked.
- "Data moves on the worksheet with Ctrl+drag" [ticket]: confirmed - Data moves into the rows at 48.6 s (p233). The Ctrl key and the click are not seen (cursor not found 47.3-48.5 s).
- "Failure happens even with multiple data fields" [ticket]: not shown - It already fails at 9.6 s with no data fields, and again at 42-43 s with two. So the data fields are not a condition.
- "Removing the Data field makes it return to Column Fields on reopening" [ticket]: not shown - The video never removes Data.
- "The Calc Guide documents moving Data between Column and Row Fields" [ticket]: not shown - The guide is not shown.
- "Reproducible always" [ticket]: not shown - Only two or three attempts are seen, and all of them fail.
