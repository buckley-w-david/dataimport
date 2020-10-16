import dataimport
import pandas
dataimport.register('csv', pandas.read_csv)

import dataimport.test.csv as datatable
print(datatable)
