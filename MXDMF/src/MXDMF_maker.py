# -*- coding: utf-8 -*-

#this class is resposible for, given a MOHID HDF5 file, reading it's fields
#and writting a correspoing XDMF file
#it is composed of a number of objects from other classes, that do most of the 
#actual work. This is the pupeteer...

import sys
sys.path.append('../../Common')
import os_dir

import MXDMF_writer as writer
import MHDF5_reader as reader

###############################################################################

class MXDMFmaker:
    def __init__(self, hdf5filename, directory):
        self.hdf5filename = os_dir.filename_without_ext(hdf5filename)
        self.directory = directory
        self.hdf5fileType = []
        self.timeStep = 1
        #instantiating reader and writer classes
        self.hdf5reader = reader.MHDF5Reader(hdf5filename, self.directory)
        
        #if file is valid, we create a xmdf writer object and feed it
        if self.hdf5reader.isValidFile():
            self.xdmfwriter = writer.MXDMFwriter(self.hdf5filename, self.directory)
            self.hdf5fileType = self.hdf5reader.getFileType()
            print '--->', self.hdf5fileType, 'file'
            
            self.xdmfwriter.writeHeader()
            
            while self.timeStep <= self.hdf5reader.getNumbTimeSteps():
                geoDims = self.hdf5reader.getGeoDims(self.timeStep)
                date = self.hdf5reader.getDate(self.timeStep)
                
                self.xdmfwriter.writeGeo(self.hdf5fileType,self.timeStep,date,geoDims)
                self.xdmfwriter.writeAttribute(self.hdf5fileType,self.timeStep,date,geoDims)
                
                self.timeStep = self.timeStep + 1
        
            self.xdmfwriter.closeFile()
            
        print '--->', 'Wrote',self.hdf5filename+'.xdmf', 'file'
        
            