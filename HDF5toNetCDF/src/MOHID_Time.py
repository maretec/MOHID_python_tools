# -*- coding: utf-8 -*-

import sys
sys.path.append('../../Common')
import os_dir as os_dir

from MOHIDHDFtoNetcdf   import MOHIDHdf5toNetcdf
from MOHIDLagHDFtoXYZ   import MOHIDLagHdf5toNetcdf

###############################################################################

dataDumpDir = 'GluedData'
os_dir.mkdir_safe(dataDumpDir)
dataDumpDir = dataDumpDir + '\\'

###############################################################################

#hydrodynamic files
basedir = 'D:\PV_data\Atlantic_Lagrangian\Hydrodynamic2'
subdirs = os_dir.get_immediate_subdirectories(basedir)
#print subdirs

time_stride = 1

t=0
dates = [['0']]
for subdir in subdirs:
    fullpath = basedir + '\\' + subdir
    print('searching in ', fullpath)
    hdf5files = os_dir.get_contained_files(fullpath,'.hdf5')
    print('found files ', hdf5files)
    for dayfiles in hdf5files:
        print('processing ', dayfiles, ', Time ', t)
        fullfilename = fullpath + '\\' + dayfiles
        t, dates = MOHIDHdf5toNetcdf(fullfilename,dates,t,time_stride,dataDumpDir)
            
###############################################################################

#Lagrangian files
basedir = 'D:\PV_data\Atlantic_Lagrangian\Lagrangian2'
subdirs = os_dir.get_immediate_subdirectories(basedir)
#print subdirs

t=0
dates = [['0']]
for subdir in subdirs:
    fullpath = basedir + '\\' + subdir
    print('searching in ', fullpath)
    hdf5files = os_dir.get_contained_files(fullpath,'.hdf5')
    print('found files ', hdf5files)
    for dayfiles in hdf5files:
        print('processing ', dayfiles, ', Time ', t)
        fullfilename = fullpath + '\\' + dayfiles
        t, dates = MOHIDLagHdf5toNetcdf(fullfilename,dates,t,dataDumpDir)