# -*- coding: utf-8 -*-

# HDFtoXYZ
# This tool converts MOHID Lagrangian HDF5 files to a collection of xyz csv 
# files, one per time step


import h5py
import numpy as np

def MOHIDLagHdf5toNetcdf(filename,in_t=0,outdir=''):
    f = h5py.File(filename,'r')
    
    TimestepsX = f['Results']['Group_1']['Data_1D']['Longitude'].keys()
    TimestepsY = f['Results']['Group_1']['Data_1D']['Latitude'].keys()
    TimestepsZ = f['Results']['Group_1']['Data_1D']['Z Pos'].keys()
    TimestepsOid = f['Results']['Group_1']['Data_1D']['Origin ID'].keys()
    
    t=in_t
    for time in range(0,len(TimestepsX)):
        
        X=f['Results']['Group_1']['Data_1D']['Longitude'][TimestepsX[time]][:]
        Y=f['Results']['Group_1']['Data_1D']['Latitude'][TimestepsY[time]][:]
        Z=f['Results']['Group_1']['Data_1D']['Z Pos'][TimestepsZ[time]][:]
        OiD=f['Results']['Group_1']['Data_1D']['Origin ID'][TimestepsOid[time]][:]
        #Z=np.zeros(len(X))
        
        XYZ=np.stack((X,Y,Z,OiD)).transpose()
        np.savetxt(outdir+'XYZ'+str(t)+'.csv',XYZ,delimiter=',')
        t=t+1
        
    return t

# Change your filename hereD:\PV_data\PCOMS_Lagrangian\temp
filename = 'D:\\PV_data\\PCOMS_Lagrangian\\temp\\Lagrangian.hdf5'
t = MOHIDLagHdf5toNetcdf(filename)