# real/lo-174415

_gpt-6-sol@default, 71 s; looked at: frames/0040.0.jpg, frames/0042.0.jpg, frames/0043.0.jpg, frames/0044.0.jpg, frames/0054.0.jpg, frames/0055.0.jpg, frames/0056.0.jpg, frames/0058.0.jpg, frames/0061.0.jpg, frames/moments/p254.jpg, frames/moments/p261.jpg, frames/0005.0.jpg, frames/0010.0.jpg, frames/0013.0.jpg, frames/0019.0.jpg, frames/0021.0.jpg, frames/0028.0.jpg, frames/0032.0.jpg, frames/0035.0.jpg, frames/0046.0.jpg, frames/0048.0.jpg, frames/0050.0.jpg, looks/0040.90-0041.90-550_125_310_390/sheet.jpg, looks/0042.60-0043.80-550_125_310_390/sheet.jpg, looks/0045.70-0046.50-20_150_190_115/sheet.jpg, looks/0041.00-0041.80-1020_190_300_610/sheet.jpg, looks/0042.70-0043.60-1020_190_300_610/sheet.jpg, looks/0041.00-0041.80-1020_190_300_610/041.300.jpg, looks/0042.70-0043.60-1020_190_300_610/043.200.jpg, frames/0049.0.jpg, frames/0057.0.jpg_

In LibreOffice Calc, dragging the generated Data field from Column Fields to Row Fields in Pivot Table Layout leaves it in Column Fields, so Sales and Cost remain side by side. Moving Data on the worksheet instead displays the measures vertically.

## Pivot Table Layout does not move the generated Data field between field areas

Class: **silent-fail**

Environment: LibreOffice Calc, workbook 'Calculated Fields in Pivot Table in LibreOffice Calc.ods'. The ticket reports version 26.8, but the video does not show the version.

Steps:

1. With source range A1:F25 selected, create a pivot table from Current selection. (00:18.0; p090, p096, p103, p106)
2. Place Salesperson in Filters, Region in Row Fields, and Sales and Cost in Data Fields; create the pivot table with Data in Column Fields. (00:26.5; p131, p132, p138, p142, p147, p157, p158)
3. Open the pivot table's Properties. (00:38.9; p180, p186, p189)
4. Drag Data from Column Fields toward Row Fields; repeat the attempt. (00:41.0; p190, p198, p204, p207, p209)

Expected (implied): Data moves to Row Fields, displaying the Sales and Cost measures vertically.

Actual: Data remains selected in Column Fields, Row Fields still contains only Region, and accepting the dialog leaves Sum - Sales and Sum - Cost as adjacent worksheet columns. No error message appears.

Key events: p189, p190, p198, p204, p207, p209, p215, p232, p233, p251, p254, p261

Missed by the author:

- The dialog also has Salesperson in Filters and Region in Row Fields [p189]; the worksheet subsequently shows that moving Data to rows works [p233, p251].
- The attempt to move Data back from Row Fields toward Column Fields later also leaves Column Fields empty in the checked frames [p254, p261].

Claims:

- "Dragging Data to Row Fields has no effect even with multiple data fields; no error appears." [ticket description and actual results]: confirmed - The dialog shows Sum - Sales and Sum - Cost. The timeline records the attempts, and the intervening frames show a prohibited-drop cursor; Data stays in Column Fields.
- "Removing Data causes it to return to Column Fields when the dialog is reopened." [ticket actual results]: not shown - Data is removed in an earlier, unpopulated layout, but the later layout belongs to a newly created pivot table, not a reopening of that layout.
- "Data can be moved directly on the worksheet by holding Ctrl and dragging it into the row area." [ticket additional info]: confirmed - The worksheet changes from adjacent measures to vertical measures [p232, p233], and Properties later shows Data in Row Fields [p251]. The cursor and keys are not visible during the move, so the video cannot establish the exact gesture or whether Ctrl was held.
- "The issue always reproduces, occurs with different field configurations, and is documented in the Calc Guide." [ticket reproducibility and additional info]: not shown - The video shows one populated configuration and does not show the guide.
