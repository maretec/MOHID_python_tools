# -*- coding: utf-8 -*-

# HDFtoXYZ
# This tool converts MOHID Lagrangian HDF5 files to a collection of xyz csv 
# files, one per time step


import h5py
import numpy as np

def MOHIDLagHdf5toNetcdf(filename, dates= [['0']], in_t=0, outdir=''):
    f = h5py.File(filename,'r')
    
    TimestepsX = f['Results']['Group_1']['Data_1D']['Longitude'].keys()
    TimestepsY = f['Results']['Group_1']['Data_1D']['Latitude'].keys()
    TimestepsZ = f['Results']['Group_1']['Data_1D']['Z Pos'].keys()
    #TimestepsOid = f['Results']['Group_1']['Data_1D']['Origin ID'].keys()
    TimestepsOid = f['Results']['Group_1']['Data_1D']['Partic ID'].keys()
    TimeList = f['Time'].keys()
    
    t=in_t
    for time in range(0,len(TimestepsX)):
        readtime = 1
        date=f['Time'][TimeList[time]][:].transpose()
        date=''.join(str(e) for e in date)
        for sublist in dates:
            if sublist == date:
                readtime = 0
        if readtime == 1:
            dates=np.vstack((dates,date))
            X=f['Results']['Group_1']['Data_1D']['Longitude'][TimestepsX[time]][:]
            Y=f['Results']['Group_1']['Data_1D']['Latitude'][TimestepsY[time]][:]
            Z=f['Results']['Group_1']['Data_1D']['Z Pos'][TimestepsZ[time]][:]
            #OiD=f['Results']['Group_1']['Data_1D']['Origin ID'][TimestepsOid[time]][:]
            OiD=f['Results']['Group_1']['Data_1D']['Partic ID'][TimestepsOid[time]][:]
            #Z=np.zeros(len(X))
            
            XYZ=np.stack((X,Y,Z,OiD)).transpose()
            np.savetxt(outdir+'XYZ'+str(t)+'.csv',XYZ,delimiter=',')
            t=t+1
        
    return t, dates

# Change your filename hereD:\PV_data\PCOMS_Lagrangian\temp
#filename = 'D:\\PV_data\\PCOMS_Lagrangian\\temp\\Lagrangian.hdf5'
#t = MOHIDLagHdf5toNetcdf(filename)