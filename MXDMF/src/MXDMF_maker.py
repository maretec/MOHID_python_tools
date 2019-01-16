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
        self.hdf5filename = []
        self.directory = []
        self.hdf5fileType = []
        self.timeStep = []
        #instantiating reader and writer classes
        self.hdf5reader = []
        self.xdmfwriter = []
        self.hdf5filename = []
        self.directory = []        
            
    def doFile(self, hdf5filename, directory):
        self.hdf5filename = os_dir.filename_without_ext(hdf5filename)
        self.directory = directory
        self.hdf5fileType = []
        self.timeStep = 1
        #instantiating reader and writer classes
        self.hdf5reader = reader.MHDF5Reader(hdf5filename, self.directory)
        
        #if file is valid, we create a xmdf writer object and feed it
        if self.hdf5reader.isValidFile():
            self.xdmfwriter = writer.MXDMFwriter()
            self.xdmfwriter.openFile(self.hdf5filename, self.directory)
            self.hdf5fileType = self.hdf5reader.getFileType()

            print('- [MXDMFmaker::doFile]:', self.hdf5fileType, 'file')
            
            while self.timeStep <= self.hdf5reader.getNumbTimeSteps():
                geoDims = self.hdf5reader.getGeoDims(self.timeStep)
                date = self.hdf5reader.getDate(self.timeStep)
                timeStamp = mdate.getTimeStampFromMOHIDDate(date)
                attributes = self.hdf5reader.getAllAttributesPath(self.timeStep)
                
                self.xdmfwriter.openGrid('Solution_'+str(self.timeStep).zfill(5))
                self.xdmfwriter.writeGeo(self.hdf5fileType,self.timeStep,timeStamp,geoDims)
                for attr in attributes:
                    self.xdmfwriter.writeAttribute(self.hdf5fileType,attr,geoDims)
                self.xdmfwriter.closeGrid()
                
                self.timeStep = self.timeStep + 1
        
            self.xdmfwriter.closeFile()
            print('- [MXDMFmaker::doFile]:', 'Wrote',self.hdf5filename+'.xdmf', 'file')
            
            
class GlueMXDMFmaker():
    def __init__(self):  
        self.gluefilenames = []
        self.gluedirectory = []
        self.hdf5reader = []
        
        #this will be a list of writers, one for each type of output
        self.xdmfwriter = []
        self.hdf5filename = []
        self.hdf5validFile = []
        self.hdf5fileType = []
        self.directory = []
    
    def openGlueWriter(self, filenames, directory):
        self.hdf5filename = filenames
        self.directory = directory
        
                
        #self.xdmfwriter.openFile(self.gluefilename, self.gluedirectory)
            
    def addFile(self, hdf5filename, absDirectory, directory):
        return 1
    
    
    
    
    
    