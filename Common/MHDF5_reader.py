# -*- coding: utf-8 -*-

import h5py
import numpy as np

class MHDF5Reader:
    def __init__(self, filename, directory):
        self.filename = filename
        self.directory = directory
        self.f = h5py.File(self.directory +'/'+ self.filename, 'r')
        self.validfile = 0
        self.filetype = []
        self.fkeys = self.f.keys()
        
        self.MOHIDkeys = ['Grid', 'Results', 'Time']
        self.hydroVars = ['baroclinic force X', 'baroclinic force Y', 'velocity U', 'velocity V', 'velocity W']
        self.lagrangianVars = []
        
        #check if file is a valid MOHID output
        if all(i in self.fkeys for i in self.MOHIDkeys):
            self.validfile = 1
        else:
            for key in self.MOHIDkeys:
                if key not in self.fkeys:
                    print '- File does not have', key, 'group, not from MOHID, ignoring'
                    
        #check for file type
        if self.validfile == 1:
            #checking for Hydrodynamic files
            if 'water level' in self.f['Results'].keys():
                self.filetype = 'Hydrodynamic'
                if 'Corners3D' not in self.f['Grid'].keys():
                    print '- Old hydrodynamic file, without mesh information, ignoring'
                    self.validfile = 0
            #cheking for Lagrangian files 
            if 'Group_1' in self.f['Results'].keys():
                self.filetype = 'Lagrangian'
                
    def getFileType(self):
        return self.filetype
                
    def getMeshDims(self):
        return 1
        