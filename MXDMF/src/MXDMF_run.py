# -*- coding: utf-8 -*-

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
        
    print '-> Main directory is', datadir
    #files may be in sub directories
    subdirs = os_dir.get_immediate_subdirectories(datadir)
    #if subdirs is empty then just point to the main directory, as a list
    if subdirs == []:
        subdirs = [datadir]
    
    foundFiles = 0
    #go through all subdirs 
    for subdir in subdirs:
        hdf5files = os_dir.get_contained_files(subdir,'.hdf5')
        for hdf5file in hdf5files:
            #create an xdmf file with the same name as 
            #the hdf5, on the same directory
            #this constructor takes care of all of that
            print '--> Processing file', hdf5file
            writexdmf = MXDMF_maker.MXDMFmaker(hdf5file,subdir)
            foundFiles = foundFiles + 1
    
    if foundFiles == 0:
        print '-> No files found. Are you sure the directory is correct?'
    else:
        print '-> Processed ' + str(foundFiles) + ' files'
            
run()