# -*- coding: utf-8 -*-

# csv2HDF5
# This tool converts a [date,lon,lat] csv file into a MOHID compatible Lagrangian HDF5 file

import os
import sys
import re

basepath = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(basepath, '../../Common')))

import os_dir

import h5py
import numpy as np
import pandas as pd


###################functions#######################
def csv2HDF5_Lag(fileName, datadir):
    
    df = pd.read_csv(datadir+'/'+fileName, skipinitialspace=True, delimiter=";")
    header = list(df)
    Date = df.Fecha
    Lat = df.Lat
    Lon = df.Lon
    ZPos = np.zeros(len(Lat))
    Dates = []
    for date in Date:
        Dates.append(re.findall('\d+', date))
    Dates = (np.array(Dates, dtype=np.float32)).transpose()
    
    cleanFileName = os_dir.filename_without_ext(fileName)    
    with h5py.File(datadir+'/'+cleanFileName+'.hdf5', "w") as f:  
        Grid = f.create_group("Grid")
        Results = f.create_group("Results")
        Group_1 = Results.create_group("Group_1")
        Data_1D = Group_1.create_group("Data_1D")
        Latitude = Data_1D.create_group("Latitude")
        Longitude = Data_1D.create_group("Longitude")
        Z_Pos = Data_1D.create_group("Z Pos")
        Time = f.create_group("Time")
        
        counter = 1
        for lats in Lat:
            fieldName = 'Latitude_'+str(counter).zfill(5)
            dset = Latitude.create_dataset(fieldName, data=lats)
            counter = counter + 1
    
        counter = 1
        for lons in Lon:
            fieldName = 'Longitude_'+str(counter).zfill(5)
            dset = Longitude.create_dataset(fieldName, data=lons)
            counter = counter + 1
            
        counter = 1
        for zpos in ZPos:
            fieldName = 'Z Position_'+str(counter).zfill(5)
            dset = Z_Pos.create_dataset(fieldName, data=zpos)
            counter = counter + 1
        
        counter = 1
        for column in Dates.T:
            fieldName = 'Time_'+str(counter).zfill(5)
            #dset = Time.create_dataset(fieldName, data=dates)
            dset = Time.create_dataset(fieldName, data=column)
            counter = counter + 1


###################run it#########################
datadir = 'testFiles'
datadir = os.path.abspath(os.path.join(basepath, "..", datadir))

csvFiles = os_dir.get_contained_files(datadir,'.csv')
for csvFile in csvFiles:
    t = csv2HDF5_Lag(csvFile, datadir) 

