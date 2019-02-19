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

class MXDMFmaker:
    def __init__(self):
        self.hdf5filename = []
        self.directory = []
        self.hdf5fileType = []
        self.timeStep = []
        #instantiating reader and writer classes
        self.hdf5reader = []
        self.xdmfwriter = []
            
    def doFile(self, hdf5filename, directory):
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
            print('- [MXDMFmaker::doFile]:', self.hdf5fileType, 'file')
            
            self.xdmfwriter.writeHeader()
            
            while self.timeStep <= self.hdf5Reader.getNumbTimeSteps():
                meshDims = self.hdf5Reader.getMeshDims(self.timeStep)
                dateStr = self.hdf5Reader.getDateStr(self.timeStep)
                timeStamp = mdate.getTimeStampFromDateString(dateStr)
                attributes = self.hdf5Reader.getAllAttributesPath(self.timeStep)
                
                self.xdmfWriter.openGrid('Solution_'+str(self.timeStep).zfill(5))
                self.xdmfWriter.writeGeo(self.hdf5FileType,self.timeStep,timeStamp,dateStr,meshDims,self.hdf5Reader.getGeoDims())
                for attr in attributes:
                    self.xdmfwriter.writeAttribute(self.hdf5fileType,attr,geoDims)
                self.xdmfwriter.closeGrid()
                
                self.timeStep = self.timeStep + 1
        
            self.xdmfWriter.closeFile()
            print('- [MXDMFmaker::doFile]:', 'Wrote',self.hdf5FileName+'.xdmf', 'file')
            
            
class GlueMXDMFmaker():
    def __init__(self):
        #set once
        self.glueFileName = []
        self.glueDirectory = []
        
        #this will be lists of things/objects, one for each type of output
        self.xdmfWriter = []
        self.hdf5FileName = []
        self.hdf5FileType = []
        self.usedTimes = []
        
        #to use at class calls
        self.hdf5Reader = []
        self.timeStep = []
        self.currDir = []
        self.currFileName = []
    
    def openGlueWriter(self, fileNames, absSubDir, directory):
        self.hdf5FileName = fileNames
        self.glueDirectory = directory
        
        for hdf5File in self.hdf5FileName:
            if '_1' not in hdf5File:
                self.hdf5Reader = reader.MHDF5Reader(hdf5File, absSubDir)
                if self.hdf5Reader.isValidFile():
                    self.glueFileName.append(os_dir.filename_without_ext(hdf5File))
                    self.xdmfWriter.append(writer.MXDMFwriter())
                    
                    self.xdmfWriter[-1].openFile(self.glueFileName[-1], self.glueDirectory)
                    self.hdf5FileType.append(self.hdf5Reader.getFileType())
                    self.usedTimes.append([])
            
    def addFile(self, hdf5FileName, absSubDir, subdir, firstDate='', lastDate=''):
        self.currFileName = os_dir.filename_without_ext(hdf5FileName)
        self.currDir = absSubDir
        self.hdf5Reader = reader.MHDF5Reader(hdf5FileName, self.currDir)
        if self.hdf5Reader.isValidFile():
            f = self.glueFileName.index(self.currFileName)
            self.timeStep = 1
            
            while self.timeStep <= self.hdf5Reader.getNumbTimeSteps():
                    meshDims = self.hdf5Reader.getMeshDims(self.timeStep)
                    dateStr = self.hdf5Reader.getDateStr(self.timeStep)
                    timeStamp = mdate.getTimeStampFromDateString(dateStr)
                    
                    #checking for exceptions to add the file
                    addStep = True
                    if firstDate != '':
                        firstDateStamp = mdate.getTimeStampFromDateString(firstDate)
                        if timeStamp < firstDateStamp:
                            addStep = False
                    if lastDate != '':
                        lastDateStamp = mdate.getTimeStampFromDateString(lastDate)
                        if timeStamp > lastDateStamp:
                            addStep = False
                    if timeStamp in self.usedTimes[f]:
                        addStep = False
                    
                    if addStep:
                        attributes = self.hdf5Reader.getAllAttributesPath(self.timeStep)                        
                        self.xdmfWriter[f].openGrid('Solution_'+str(self.timeStep).zfill(5))
                        self.xdmfWriter[f].writeGeo(self.hdf5FileType[f],self.timeStep,timeStamp,dateStr,meshDims,self.hdf5Reader.getGeoDims(),subdir+'/')
                        for attr in attributes:
                            self.xdmfWriter[f].writeAttribute(self.hdf5FileType[f],attr,meshDims,self.hdf5Reader.getGeoDims(),subdir+'/')
                        self.xdmfWriter[f].closeGrid()
                        self.usedTimes[f].append(timeStamp)
                    
                    self.timeStep = self.timeStep + 1
        
        
        print('- [MXDMFmaker::addFile]:', 'Indexed the',self.currFileName+'.hdf5', 'file')
    

    def closeGlueWriter(self):
        for xdmfWriter in self.xdmfWriter:
            xdmfWriter.closeFile()
    
    
    
    
    
    
