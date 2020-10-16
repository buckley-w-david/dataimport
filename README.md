# data-import

`import` data files via import-hook trickery

## Installation

```
 $ pip install dataimport
```

## Usage

```python
>>> import dataimport.test.csv as csv_file
>>> print(list(csv_file))
[['col1', 'col2', 'col3', 'col4'], ['1', '2', '3', '4'], ['5', '6', '7', '8'], ['9', '10', '11', '12'], ['13', '14', '15', '16'], ['17', '18', '19', '20']]
```

`csv` and `json` loaders are included, but adding or replacing a loader is easy!

```python
>>> import dataimport
>>> import pandas
>>> dataimport.register('csv', pandas.read_csv)
>>> import dataimport.test.csv as datatable
>>> print(datatable)
   col1  col2  col3  col4
0     1     2     3     4
1     5     6     7     8
2     9    10    11    12
3    13    14    15    16
4    17    18    19    20
```
