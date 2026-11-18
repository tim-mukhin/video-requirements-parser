# Calc Pivot Table Layout: Cannot drag Data field from Column Fields to Row Fields

Source: https://bugs.documentfoundation.org/show_bug.cgi?id=174415  (reporter: <email>, filed 2026-11-09)

Description:
In LibreOffice Calc 26.8, the automatically generated Data field in the Pivot Table Layout dialog cannot be moved from Column Fields to Row Fields. Dragging the field has no effect, even when multiple data fields are present.

Steps to Reproduce:
1. Open LibreOffice Calc and create a Pivot Table from a dataset.
2. Add Sales and Cost to the Data Fields area.
3. Open the Pivot Table Layout dialog.
4. Attempt to drag the automatically generated Data field from Column Fields to Row Fields.

Actual Results:
The Data field does not move to Row Fields. No error message appears.

Removing the Data field entirely causes LibreOffice to restore it to Column Fields when the Pivot Table Layout dialog is reopened.

Expected Results:
The Data field should move from Column Fields to Row Fields when dragged within the Pivot Table Layout dialog, allowing data values to be displayed vertically instead of horizontally.

Reproducible: Always

User Profile Reset: No

Additional Info:
The issue occurs consistently, even when using different field configurations.

I can successfully move the Data field directly on the worksheet by holding Ctrl and dragging it into the row area of the Pivot Table.

The LibreOffice Calc Guide documents that the Data field can be moved between Column Fields and Row Fields.
