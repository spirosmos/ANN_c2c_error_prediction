# ANN_c2c_error_prediction

A pretrained network for predicting the per vertex geometric error of the manufactured object produced by the binder jetting printer ZPrinter 450. 

## Dependencies

For ann_predictor.py
- Python 3.6 or later
- Tensorflow 2.7.0
- Pandas 1.3.4
- Numpy
- Joblib 1.1.0

For export_CSV_from_OBJ.py
- Python 3.6 or later
- Numpy
- IGL
- Scipy


## Reference

ArcivX link

## extract_CSV_from_OBJ.py

Exports the features in a .csv file, given any .obj model as input.

```sh
python export_CSV_from_OBJ.py yourModel.obj
```
Example of features
| x | y | z | Gauss Curvature | Mean Curvature | Internal Angle-AVG | Internal Angle-Min | Internal Angle-Max | Normal's Anlge On Z-axis |  Distance from bounding box |
| ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ |
| 118.462959 | 55.829819 | 5.898669 | -0.088429 | 1.115727 | 45.041894 | 21.655226 | 66.665803 | 86.064389 | 5.741143 |
| 112.507225 | 47.683815 | 18.451500 | 0.420510 | 0.859329 | 59.604654 | 29.939070 | 96.713844 | 103.230509 | 15.915016 |
| 100.989685 | 31.305315 | 59.740143 | -0.497328 | 0.023250 | 51.684147 | 33.436291 | 65.549049 | 78.435304 | 5.703400 |

## ann_predictor.py

Produces a .ply file of the vertices and the predicted per vertex dimensional error (in milimeters), given a .csv file of the features of any model as input. 

```sh
python ann_predictor.py yourData.csv
```
