# MapasDeCampos
Created by: Joao Rodrigues @ hidromod https://hidromod.com/

Last Update: 01-10-2019

MapasDeCampos creates figures for almost any MOHID hdf5 file format and MOHID time series files and any variable. Main purpose is for production and operational use, it can generate:

   - 2D plots of any variable inside MOHID hdf5 files 
   - 1D plots of MOHID time series 
   - Plot statistical comparison between two hdf5 in mohid format, that come from ComapreHDF5 tool 
    
## Prerequisities:
        - Python 3.7 
        - h5py
        - basemap
        - proj4

## How to use this code:
This code has several test cases, each test case, has their own bash and PythonFigures.dat which is the main driver of the code.

### TestFiles/Compare2Hdf5
Produce a .png images with 4 plots:
   - Time averge model 
   - Time average obervation
   - Time average bias
   - Space averge  Time series

INPUT:
   - RGF0.hdf5  – hdf5 with differences that come from Compare2Hdf5 tool
   - 0/1/2, time series
   - PythonFigures.dat rules for the python
    
RUN:
Just run the bash :)
    Run.bat where you need to adapt the python.exe path.

## Known Errors:
If you get an error like this:

         from mpl_toolkits.basemap import Basemap
        File "C:\ProgramData\Anaconda3\lib\site-packages\mpl_toolkits\basemap\__init__.py", line 155, in <module>
         pyproj_datadir = os.environ['PROJ_LIB']
        File "C:\ProgramData\Anaconda3\lib\os.py", line 678, in __getitem__
          raise KeyError(key) from None
        KeyError: 'PROJ_LIB'

Go to src/moduloMapsBasemaps.py and uncomment line 5 and add the path where project4 is located
