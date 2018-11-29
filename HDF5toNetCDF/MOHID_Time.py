# -*- coding: utf-8 -*-

import os
from MOHIDHDFtoNetcdf   import MOHIDHdf5toNetcdf
from MOHIDLagHDFtoXYZ   import MOHIDLagHdf5toNetcdf

###############################################################################
def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]
    
def get_contained_files(a_dir,extension):
    return [file for file in os.listdir(a_dir)
            if file.endswith(extension)]

def mkdir_safe(a_dir):
    if not os.path.exists(a_dir):
        os.makedirs(a_dir)
    
###############################################################################

dataDumpDir = 'GluedData'
mkdir_safe(dataDumpDir)
dataDumpDir = dataDumpDir + '\\'

###############################################################################

#hydrodynamic files
basedir = 'D:\PV_data\Atlantic_Lagrangian\Hydrodynamic2'
subdirs = get_immediate_subdirectories(basedir)
#print subdirs

time_stride = 1

t=0
dates = [['0']]
for subdir in subdirs:
    fullpath = basedir + '\\' + subdir
    print 'searching in ', fullpath
    hdf5files = get_contained_files(fullpath,'.hdf5')
    print 'found files ', hdf5files
    for dayfiles in hdf5files:
        print 'processing ', dayfiles, ', Time ', t
        fullfilename = fullpath + '\\' + dayfiles
        t, dates = MOHIDHdf5toNetcdf(fullfilename,dates,t,time_stride,dataDumpDir)
            
###############################################################################

#Lagrangian files
basedir = 'D:\PV_data\Atlantic_Lagrangian\Lagrangian2'
subdirs = get_immediate_subdirectories(basedir)
#print subdirs

t=0
dates = [['0']]
for subdir in subdirs:
    fullpath = basedir + '\\' + subdir
    print 'searching in ', fullpath
    hdf5files = get_contained_files(fullpath,'.hdf5')
    print 'found files ', hdf5files
    for dayfiles in hdf5files:
        print 'processing ', dayfiles, ', Time ', t
        fullfilename = fullpath + '\\' + dayfiles
        t, dates = MOHIDLagHdf5toNetcdf(fullfilename,dates,t,dataDumpDir)