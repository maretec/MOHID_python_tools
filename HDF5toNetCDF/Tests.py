# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 11:44:48 2018

@author: RBC_workhorse
"""

import h5py
import numpy as np

filename = 'D:\PV_data\Atlantic_Lagrangian\Hydrodynamic2\hdf_files\Myocean_North_Atlantic_2016-05-30_2016-06-01_Surface.hdf5'
f = h5py.File(filename,'r')

TimeList = f['Time'].keys()

TT=f['Time'][TimeList[0]][:].transpose()
data_db = ''.join(str(e) for e in TT)

key = data_db

for time in range(1,len(TimeList)):
        TT=f['Time'][TimeList[time]][:].transpose()
        data_db=np.vstack(((data_db,''.join(str(e) for e in TT))))
        
print data_db

for sublist in data_db:
    if sublist == key:
        print "Found it!", sublist