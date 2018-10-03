# -*- coding: utf-8 -*-

# HDFtoXYZ
# This tool converts MOHID Lagrangian HDF5 files to a collection of xyz csv 
# files, one per time step


import h5py
import numpy as np

# Change your filename here
#filename = 'C:\\Users\\administrator\\Documents\\GitHub\\HDFtoXYZ\\Lagrangian_1.hdf5'
def MOHIDLagHdf5toNetcdf(filename,in_t=0,outdir=''):
    f = h5py.File(filename,'r')
    
    TimestepsX = f['Results']['Group_1']['Data_1D']['Longitude'].keys()
    TimestepsY = f['Results']['Group_1']['Data_1D']['Latitude'].keys()
    TimestepsZ = f['Results']['Group_1']['Data_1D']['Z Pos'].keys()
    
    t=in_t
    for time in range(0,len(TimestepsX)):
        
        X=f['Results']['Group_1']['Data_1D']['Longitude'][TimestepsX[time]][:]
        Y=f['Results']['Group_1']['Data_1D']['Latitude'][TimestepsY[time]][:]
        #Z=f['Results']['Group_1']['Data_1D']['Z Pos'][TimestepsZ[time]][:]
        Z=np.zeros(len(X))
        
        XYZ=np.stack((X,Y,Z)).transpose()
        np.savetxt(outdir+'XYZ'+str(t)+'.csv',XYZ,delimiter=';')
        t=t+1
        
    return t