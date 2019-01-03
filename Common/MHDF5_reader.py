# -*- coding: utf-8 -*-

import h5py
import numpy as np

class MHDF5Reader:
    #given a file name for an hdf5 file and a directory where it is located
    #this constructor: 
    #opens the file
    #checks if it is a valid MOHID output
    #checks the type of MOHID file (hydro, lagrangian, etc)
    #checks if the version of eulerian files is high enough (must have Corners3D) 
    def __init__(self, filename, directory):
        self.filename = filename
        self.directory = directory
        self.f = h5py.File(self.directory +'/'+ self.filename, 'r')
        self.validfile = 0
        self.filetype = []
        self.fkeys = self.f.keys()
        self.fTimeSteps = self.f['Time'].keys()
        
        self.MOHIDkeys = ['Grid', 'Results', 'Time']
        self.hydroVars = ['baroclinic force X', 'baroclinic force Y', 'velocity U', 'velocity V', 'velocity W']
        self.lagrangianVars = []
        
        #check if file is a valid MOHID output
        if all(i in self.fkeys for i in self.MOHIDkeys):
            self.validfile = 1
        else:
            for key in self.MOHIDkeys:
                if key not in self.fkeys:
                    print '- [MHDF5Reader::init]: file does not have', key, 'group, not a MOHID output, ignoring'
                    
        #check for file type
        if self.validfile == 1:
            #checking for Hydrodynamic files
            if 'water level' in self.f['Results'].keys():
                self.filetype = 'Hydrodynamic'
                if 'Corners3D' not in self.f['Grid'].keys():
                    print '- [MHDF5Reader::init]: old hydrodynamic file, without mesh information, ignoring'
                    self.validfile = 0
            #cheking for Lagrangian files 
            if 'Group_1' in self.f['Results'].keys():
                self.filetype = 'Lagrangian'
                
    def isValidFile(self):
        return self.validfile
                
    #returns the file type as a string
    def getFileType(self):
        if self.validfile == 1:
            return self.filetype
        else:
            print '- [MHDF5Reader::getFileType]: invalid file, no type, ignoring'
     
    #returns the number of time steps in the file
    def getNumbTimeSteps(self):
        if self.validfile == 1:
            return len(self.fTimeSteps)
        else:
            print '- [MHDF5Reader::getNumbTimeSteps]: invalid file, ignoring'
    
    #returns the date of a time step in the file
    def getDate(self, timeIndex):
        if self.validfile == 1:
            date=self.f['Time'][self.fTimeSteps[timeIndex-1]][:].transpose()
            date=''.join(str(e) for e in date)
            return date
        else:
            print '- [MHDF5Reader::getDate]: invalid file, ignoring'
                
    #returns an array with the geometry dimensions
    def getGeoDims(self, timeIndex):
        if self.validfile == 1:
            if self.filetype != 'Lagrangian':
                return self.f['Grid']['Corners3D']['Latitude'].shape
            if self.filetype == 'Lagrangian':
                timeVar = 'Latitude_' + str(timeIndex).zfill(5)
                return self.f['Results']['Group_1']['Data_1D']['Latitude'][timeVar].size
        else:
            print '- [MHDF5Reader::getGeoDims]: invalid file, no geometry, ignoring'
        