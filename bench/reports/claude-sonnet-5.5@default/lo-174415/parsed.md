# real/lo-174415

_claude-sonnet-5.5@default, 30 s; looked at: frames/001839.jpg, frames/001459.jpg, frames/001760.jpg_

The author builds a pivot table in LibreOffice Calc: Salesperson as filter, Region as row, Sales and Cost as data fields. They then reopen the pivot layout several times to move the Data field between rows and columns. No error, failed action or wrong value is visible, and the only speech is "Thank you." The video does not show what was supposed to be wrong.

## No defect visible: pivot table layout walkthrough in LibreOffice Calc (calculated-field entry never used)

Class: **not-a-bug**

Environment: LibreOffice Calc, file "Calculated Fields in Pivot Table in LibreOffice Calc.ods". A custom green tabbed/ribbon-style toolbar is shown. Source data is A1:F25 (Date, Region, Salesperson, Product, Sales, Cost). The Select Source and Pivot Table Layout dialogs are used. No accounts or organizations are visible. The cursor is followed for 93% of the video; it is not found at 00:47.3-00:48.5.

Steps:

1. Open Insert > Pivot Table... on the A1:F25 data (the first attempt, which was abandoned). (00:01.9; p005, p009, p013)
2. Confirm the Select Source dialog with OK. The Pivot Table Layout dialog opens. (00:03.4; p031, p034)
3. Click in the layout dialog and then OK (00:14.1). The result is not visible, and the author then repeats the Insert > Pivot Table... sequence. (00:05.5; p036, p062, p070)
4. Repeat Insert > Pivot Table... > OK on the same source, which opens the layout dialog again. (00:16.8; p087, p088, p094, p103, p104)
5. Drag fields in the layout dialog and confirm. The pivot table appears with Salesperson as filter, Region as rows, and Sum - Sales and Sum - Cost as data fields. (00:34.9; p115, p126, p136, p143, p150)
6. Right-click a pivot cell. The context menu offers Properties... and Calculated Field.... The author chooses Properties..., and the layout dialog opens again. (00:38.9; p172, p178, p181)
7. Rearrange the layout. Data is moved between the column and row areas in the dialog, with OK at 00:44.2, and the table switches between Data-in-columns and Data-in-rows. (00:41.7; p190, p207, p229, p231)
8. Open Properties... again, move the Data field, and press OK. The final table has Region rows with alternating Sum - Sales and Sum - Cost lines. Totals are $54,600.00 sales and $29,840.00 cost. (00:52.9; p244, p250, p258, p261, p265)

Expected (implied): Not stated by the author. Implied: a pivot table is created with the chosen fields and layout.

Actual: The pivot table is created and re-laid-out as chosen. Region totals are consistent with the grand totals: sales 9,600+22,200+12,450+10,350 = 54,600, and cost 6,820+6,840+8,750+7,430 = 29,840. No error dialog or failed action is visible. The Calculated Field... menu entry appears (p172, p243), but it is never clicked, so no calculated field is created or tested. If a defect was intended, such as the missing calculated field, the video does not show it.

Key events: p150, p172, p229, p243, p265

Missed by the author:

- The first pivot creation at 00:03-00:14 appears to leave no visible result, and the author repeats the whole sequence at 00:15-00:35 (p070, p087). It is unclear whether the first pivot was created at all.
- The context menu has a "Calculated Field..." entry (p172, p243). The video title concerns calculated fields, but the author never opens it.

Claims:

- ""Thank you." is the only speech, so the author makes no claim about a problem." [u003]: not shown - Nothing in the speech describes expected or actual behaviour.
