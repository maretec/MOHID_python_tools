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

sys.path.append('../../Common')
import os_dir

import MXDMF_maker

def run():
    if len(sys.argv) >1:
        datadir = sys.argv[1]
    else:
        basepath = os.path.dirname(__file__)
        datadir = os.path.abspath(os.path.join(basepath, "..", "TestFiles"))
        
    print('-> Main directory is', datadir)
    #files may be in sub directories
    subdirs = os_dir.get_immediate_subdirectories(datadir)
    #if subdirs is empty then just point to the main directory
    if subdirs == []:
        subdirs = [datadir]
    
    foundFiles = 0
    #create mxdmf_maker class objects
    singleXDMF = MXDMF_maker.MXDMFmaker()
    #go through all subdirs
    for subdir in subdirs:
        hdf5files = os_dir.get_contained_files(subdir,'.hdf5')
        for hdf5file in hdf5files:
            #create an xdmf file with the same name as 
            #the hdf5, on the same directory
            print('--> Processing file', hdf5file)           
            singleXDMF.doFile(hdf5file,subdir)
            foundFiles = foundFiles + 1
    
    if foundFiles == 0:
        print('-> No files found. Are you sure the directory is correct?')
    else:
        print('-> Finished. Processed ' + str(foundFiles) + ' files')
            
run()