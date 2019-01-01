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
        if self.fkeys == self.MOHIDkeys:
            #file is a valid MOHID output
            self.validfile = 1
        else:
            for key in self.MOHIDkeys:
                if key not in self.fkeys:
                    print 'File does not have', key, 'group, not from MOHID, ignoring'
        self.hydroVars = ['baroclinic force X', 'baroclinic force Y', 'velocity U', 'velocity V', 'velocity W']
        
        
    def getFileType(self):
        if self.validfile == 1:
            #checking for Hydrodynamic files
            if 'water level' in self.f['Results'].keys():
                print '---> Hydrodynamic file'
                self.filetype = 'hydrodynamic'
            #cheking for Lagrangian files 
            if 'Group_1' in self.f['Results'].keys():
                print '---> Lagrangian file'
                self.filetype = 'lagrangian'