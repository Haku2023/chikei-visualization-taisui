# Synthetic presentation data

`synthetic_layer5_template.csv` contains fictional hills, a ridge, and a curved
channel generated from mathematical functions. No original elevation values,
terrain features, or statistics were used to generate it. Only the original
grid dimensions were retained: 212 rows (Y) by 252 columns (X).

The file is a numeric height matrix, with no header, index, coordinates, blank
cells, or trailing empty column. The application's CSV reader accepts this
format directly; the original file's trailing empty column is unnecessary.

## Present with fictional coordinates

1. Choose **Using .csv file** and **One File**.
2. Upload `synthetic_layer5_template.csv` using **Upload File One**.
3. Leave **Layer_One** unselected (or clear it). Enter these values manually:

   | Field | Value |
   | --- | ---: |
   | Xmin1 | 0 |
   | Xmax1 | 1260 |
   | Ymin1 | 0 |
   | Ymax1 | 1060 |
   | dx | 5 |
   | dy | 5 |

4. Keep the default **downward** row orientation, then click **Generate-csv**
   for 3D or **Generate-2D** for contours.

These fictional bounds preserve the Layer 5 spacing and dimensions:
`(1260 - 0) / 5 = 252` columns and `(1060 - 0) / 5 = 212` rows.
Cell centers run from X=2.5 to 1257.5 and Y=2.5 to 1057.5.
Label the presentation as synthetic demonstration data.

## How layer selection works

The Python app does not detect a layer or geographic boundary from CSV contents
or its filename. Selecting a layer fills the coordinate fields from the
`layermapping` dictionary in the Python file. Selecting Layer 5 works with this
template's dimensions, but displays the existing geographic coordinates from
that dictionary. For fictional coordinates, use the values above after any
layer selection, and do not change the layer afterward (it resets the fields).

The original CSV and Python script have been left unchanged. This template does
not remove the geographic bounds already present in the Python source.
