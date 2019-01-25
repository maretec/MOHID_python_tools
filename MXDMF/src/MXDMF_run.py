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
#    !global pupetter script for launching xdmf writer objects over hdf5 MOHID outputs
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

import os
import sys
import argparse

sys.path.append('../../Common')
import os_dir

import MXDMF_maker

def run():
    
    #cmd line argument parsing---------------------------
    argParser = argparse.ArgumentParser(description='Indexes MOHID outputs in xmdf files. Use -h for help.')
    argParser.add_argument("-i", "--input", dest="datadir",
                    help="input directory containing .hdf5 files or subdirectories with them", metavar="dir")
    argParser.add_argument("-g", "--glue", dest="glueFiles", default=False,
                    help="option to atempt to produce a master indexer, that 'glues' all of the files")
    argParser.add_argument("-fd", "--firstdate", dest="firstDate", default='',
                    help="option to control the first date for the master indexer, format as 2000-08-19 01:01:37")
    argParser.add_argument("-ld", "--lastdate", dest="lastDate", default='',
                    help="option to control the last date for the master indexer, format as 2000-08-19 01:01:37")
    args = argParser.parse_args()

    datadir = getattr(args,'datadir')
    if datadir == None: #reverting to the test files
        basepath = os.path.dirname(__file__)
        datadir = os.path.abspath(os.path.join(basepath, "..", "TestFiles"))        
    glueFiles = getattr(args,'glueFiles')
    if glueFiles != False:
        glueFiles = True
    firstDate = str(getattr(args,'firstDate'))
    lastDate = str(getattr(args,'lastDate'))
        
    print('-> Main directory is', datadir)
    if glueFiles:
        print('-> Attempting to glue files')
    if firstDate != '':
        print('-> First date to be indexed is', firstDate)
    if lastDate != '':
        print('-> First date to be indexed is', lastDate)    
    #------------------------------------------------------    
    
    #files may be in sub directories
    subdirs = os_dir.get_immediate_subdirectories(datadir)
    #if subdirs is empty then just point to the main directory
    if subdirs == []:
        subdirs = [datadir]
    
    foundFiles = 0
    #create mxdmf_maker class objects
    singleXDMF = MXDMF_maker.MXDMFmaker()
    glueXDMF = MXDMF_maker.MXDMFmaker(glueFiles)
    
    #Creating files to index to if glue is required
    if glueFiles:
        ignoreGlueDir = []
        for subdir in subdirs: #we need to search for hotstart files and ignore them
            absSubDir = os.path.abspath(os.path.join(datadir, subdir))
            hdf5files = os_dir.get_contained_files(absSubDir,'.hdf5')
            if '_1' in hdf5files[0]: #this is the current convention
                ignoreGlueDir.append(subdir)
        for subdir in subdirs: #going to search for the first good dir and create empty .xdmf files based on those
            if subdir not in ignoreGlueDir:
                absSubDir = os.path.abspath(os.path.join(datadir, subdir))
                hdf5files = os_dir.get_contained_files(absSubDir,'.hdf5')
                glueXDMF.openGlueWriter(hdf5files,absSubDir,datadir)
                break
    
    #Run the thing
    #go through all subdirs
    for subdir in subdirs:
        absSubDir = os.path.abspath(os.path.join(datadir, subdir))
        hdf5files = os_dir.get_contained_files(absSubDir,'.hdf5')
        for hdf5file in hdf5files:
            print('--> Processing file', hdf5file) 
            #create an xdmf file with the same name as 
            #the hdf5, on the same directory
            singleXDMF.doFile(hdf5file,absSubDir)
            if glueFiles and (subdir not in ignoreGlueDir):
                #add to the gluing file
                glueXDMF.addFile(hdf5file,absSubDir,subdir,firstDate,lastDate)
            foundFiles = foundFiles + 1
    
    if glueFiles:
        glueXDMF.closeGlueWriter()
    
    if foundFiles == 0:
        print('-> No files found. Are you sure the directory is correct?')
    else:
        print('-> Finished. Processed ' + str(foundFiles) + ' files')
            
run()