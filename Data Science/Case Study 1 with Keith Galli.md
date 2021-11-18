#### Methods

##### Clean NaN(nulls) or Filtering Out unwanted data

```
nan_df = all_data[all_data.isna().any(axis=1)]
nan_df.head()
```

##### Clean up str from int()
`all_data['Sales'] = all_data['Quantity Ordered'] * all_data['Price Each']` 

#### Useful Commands

`os.listdir()` will get you everything that's in a directory- files and directories

If you want just files, you could either filter this down using `os.path`

```
from os import litdir
from os.path import isfile, join
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
```

Or can use `os.walk()` which yields 2 list for each directory - splitting it into files and dirs.

```
from os import walk

f = []
for (dirpath, dirnames, filenames) in walk(mypath):
	f.extend(filenames)
	break
```

`pandas.concat` - concatenate 

`pd.read_csv("file_name.csv")` - read CSV file
`<DataFrameName>.to_csv("<file_name>.csv", index=False)` -- export data frame into a new file

