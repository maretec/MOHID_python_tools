# GetMeteoPy
Python script to download, glue, and interpolate metereological model data in hdf5 format to be used as forcing in a MOHID model.


## Requirements
### Software:
- a python 3 distribution
- PyYAML library ([pip](https://pypi.org/project/PyYAML/), [conda](https://anaconda.org/conda-forge/pyyaml))
- h5py library ([pip](https://pypi.org/project/h5py/), [conda](https://anaconda.org/conda-forge/h5py))
- ConvertToHDF5 tool from [MOHID](https://github.com/Mohid-Water-Modelling-System/Mohid)

### File requirements:
- `GetMeteoPy.dat` file with START and END dates in YYYY MM DD HH MM SS format
- `GetMeteoPy.yaml` file with the desired settings

## How does it work
GetMeteoPy uses the ConvertToHDF5 MOHID tool with the action [GLUES HDF5 FILES](http://wiki.mohid.com/index.php?title=ConvertToHDF5#GLUES_HDF5_FILES) to glue the meteo hdf5 file. After, it uses the action [INTERPOLATE GRIDS](http://wiki.mohid.com/index.php?title=ConvertToHDF5#INTERPOLATE_GRIDS) or the action [PATCH HDF5 FILES](http://wiki.mohid.com/index.php?title=ConvertToHDF5#PATCH_HDF5_FILES) to interpolate the results to the MOHID model bathymetry.

---

## Keywords
### List of keywords used in the `GetMeteoPy.yaml` file:
- `convertToHDF5exe`: `(string)` location of the ConvertToHDF5 tool
- `bathymetry`: `(string)` location of the bathymetry of your MOHID Water or Land domain
- `typeOfInterpolation`: `(integer)` option of interpolation used by the INTERPOLATE GRIDS and PATCH HDF5 FILES actions, see the [MOHID documentation](http://wiki.mohid.com/index.php?title=ConvertToHDF5#INTERPOLATE_GRIDS)
- `outputDirectory`: `(string)` directory to save the output of the program
- `outputPrefix`: `(string)` used to write the name of the HDF5 output file

- `meteoModels`: block of metereologic models to be used in the interpolation
  - `modelName1`: block of the first metereologic model, name is arbitrary but duplicates are not allowed
    - `meteoDirectory`: `(string)` directory where your metereologic HDF5 files are stored, program will search inside subdirectories
    - `meteoFileFormat`: `(string)` name of the files to be searched in the directory, dates are specified using [python datetime string codes](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes) at least year, month and day are expected. Given 2 sets of dates it's assumed to be the start and end of the HDF5 file. Given just 1 date it's assumed to be the start of the HDF5 file.
    - `meteoFileTotalSeconds`: `(integer)` if given just 1 date in `meteoFileFormat` it's necessary to give the number of sconds between the final and first instant of the HDF5 file.
    - `meteoRemoveStartupSeconds`: `(integer)` `(optional)` if your HDF5 files contains startup instant that you don't want to use, use this keyword with the amount of time in seconds to be discarded counting from the begining of the files.
    - `meteoDatFile`: `(string)` location of the bathymetry file of your metereologic model
    - `level`: `(integer)` if given more than 1 metereologic model use this keyword to specify the priority (smaller numbers are higher priority)
  - `modelName2`
    - `...`:`"..."`
    - `...`:`"..."`
- `propertiesToInterpolate`: `(optional)` if you don't want to interpolate all the properties present in the metereologic HDF5 files use this block with a list of properties to interpolate.
  - `"..."`
  - `"..."`
- `mohidKeywords`: `(optional)`
  - `GLUES HDF5 FILES`:
    - `...`:`"..."`
  - `INTERPOLATE GRIDS`:
    - `...`:`"..."`
  - `PATCH HDF5 FILES`:
    - `...`:`"..."`

---
## Example usage:
`GetMeteoPy.dat` file:
```yaml
START:                       2019 01 01 00 00 00
END:                         2019 01 02 00 00 00
```

`GetMeteoPy.yaml` file:
```yaml
convertToHDF5exe: "./ConvertToHDF5.exe"

bathymetry: "../../GeneralData/Bathymetry/Generic_Bathymetry.dat"

typeOfInterpolation: 3

outputDirectory: "./History/"
outputPrefix: "GenericName"

meteoModels:
  MM5:
    meteoDirectory: "//mwdata/Storage01/Meteo/MM5/MM5_D2_D3_6h/"
    meteoFileFormat: "D3_%Y%m%d%H_%Y%m%d%H.hdf5"
    meteoDatFile: "./D3.dat"

propertiesToInterpolate:
  - "air temperature"
  - "wind velocity X"
  - "wind velocity Y"

mohidKeywords:
  GLUES HDF5 FILES:
    BASE_GROUP: "Results"
    TIME_GROUP: "Time"
  INTERPOLATE GRIDS:
    DO_NOT_BELIEVE_MAP: 1
    COORD_TIP: 3
```

Output:

`./History/GenericName_2019-01-01_2019-01-02.hdf5`
