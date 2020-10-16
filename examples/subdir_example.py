import dataimport
dataimport.set_path('subdir')
import dataimport.test.csv as csvfile
print(list(csvfile))
