# -*- coding: utf-8 -*-

#    !------------------------------------------------------------------------------
#    !        IST/MARETEC, Water Modelling Group, Mohid modelling system
#    !------------------------------------------------------------------------------
#    !
#    ! TITLE         : MXDMF_run
#    ! PROJECT       : Mohid python tools
#    ! MODULE        : background
#    ! URL           : http://www.mohid.com
#    ! AFFILIATION   : IST/MARETEC, Marine Modelling Group
#    ! DATE          : January 2019
#    ! REVISION      : Canelas 0.1
#    !> @author
#    !> Ricardo Birjukovs Canelas
#    !
#    ! DESCRIPTION:
#    !this class is resposible for, given a MOHID HDF5 file, reading it's fields
#    !and writting a correspoing XDMF file
#    !it is composed of a number of objects from other classes, that do most of the 
#    !actual work. This is a pupeteer.
#    !------------------------------------------------------------------------------
#    
#    MIT License
#    
#    Copyright (c) 2018 RBCanelas
#    
#    Permission is hereby granted, free of charge, to any person obtaining a copy
#    of this software and associated documentation files (the "Software"), to deal
#    in the Software without restriction, including without limitation the rights
#    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#    copies of the Software, and to permit persons to whom the Software is
#    furnished to do so, subject to the following conditions:
#    
#    The above copyright notice and this permission notice shall be included in all
#    copies or substantial portions of the Software.
#    
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#    SOFTWARE.

import sys
sys.path.append('../../Common')
import os_dir
import MDateTime as mdate

import MXDMF_writer as writer
import MHDF5_reader as reader

###############################################################################


# a factory for our maker objects
def MXDMFmaker(glue = False):    
    if glue:
        return GlueMXDMFmaker()
    else:
        return SingleMXDMFmaker()
    

class SingleMXDMFmaker:
    def __init__(self):
        self.hdf5FileName = []
        self.directory = []
        self.hdf5FileType = []
        self.timeStep = []
        #instantiating reader and writer classes
        self.hdf5Reader = []
        self.xdmfWriter = []
        self.hdf5FileName = []
        self.directory = []        
            
    def doFile(self, hdf5FileName, directory):
        self.hdf5FileName = os_dir.filename_without_ext(hdf5FileName)
        self.directory = directory
        self.hdf5FileType = []
        self.timeStep = 1
        #instantiating reader and writer classes
        self.hdf5Reader = reader.MHDF5Reader(hdf5FileName, self.directory)
        
        #if file is valid, we create a xmdf writer object and feed it
        if self.hdf5Reader.isValidFile():
            self.xdmfWriter = writer.MXDMFwriter()
            self.xdmfWriter.openFile(self.hdf5FileName, self.directory)
            self.hdf5FileType = self.hdf5Reader.getFileType()

            print('- [MXDMFmaker::doFile]:', self.hdf5FileType, 'file')
            
            while self.timeStep <= self.hdf5Reader.getNumbTimeSteps():
                meshDims = self.hdf5Reader.getMeshDims(self.timeStep)
                date = self.hdf5Reader.getDate(self.timeStep)
                timeStamp = mdate.getTimeStampFromMOHIDDate(date)
                attributes = self.hdf5Reader.getAllAttributesPath(self.timeStep)
                
                self.xdmfWriter.openGrid('Solution_'+str(self.timeStep).zfill(5))
                self.xdmfWriter.writeGeo(self.hdf5FileType,self.timeStep,timeStamp,meshDims,self.hdf5Reader.getGeoDims())
                for attr in attributes:
                    self.xdmfWriter.writeAttribute(self.hdf5FileType,attr,meshDims,self.hdf5Reader.getGeoDims())
                self.xdmfWriter.closeGrid()
                
                self.timeStep = self.timeStep + 1
        
            self.xdmfWriter.closeFile()
            print('- [MXDMFmaker::doFile]:', 'Wrote',self.hdf5FileName+'.xdmf', 'file')
            
            
class GlueMXDMFmaker():
    def __init__(self):  
        self.glueFileName = []
        self.glueDirectory = []
        self.hdf5Reader = []
        
        #this will be a list of writers, one for each type of output
        self.xdmfWriter = []
        self.hdf5FileName = []
        self.hdf5validFile = []
        self.hdf5FileType = []
    
    def openGlueWriter(self, filenames, absSubDir, directory):
        self.hdf5FileName = filenames
        self.glueDirectory = directory
        
        f = 0
        for hdf5File in self.hdf5FileName:
            hdf5Reader = reader.MHDF5Reader(hdf5File, absSubDir)
            self.glueFileName[f] = os_dir.filename_without_ext(hdf5File)
            self.xdmfWriter[f] = writer.MXDMFwriter()
            self.xdmfWriter[f].openFile(self.glueFileName[f], self.gluedirectory)
            self.hdf5FileType[f] = hdf5Reader.getFileType()
        
        
                
        #self.xdmfWriter.openFile(self.gluefilename, self.gluedirectory)
            
    def addFile(self, hdf5FileName, absDirectory, directory):
        return 1
    
    
    
    
    
    