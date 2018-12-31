# -*- coding: utf-8 -*-

import os
import sys

sys.path.append('../../Common')
import os_dir

import MXDMF_maker

################################################################################

#file directory where MOHID hdf5 files are, or subdirectories with them 
basepath = os.path.dirname(__file__)
datadir = os.path.abspath(os.path.join(basepath, "..", "TestFiles"))
print '--> Main working directory is', datadir
#files may be in sub directories
subdirs = os_dir.get_immediate_subdirectories(datadir)
#if subdirs is empty then just point to the main directory, as a list
if subdirs == []:
    subdirs = [datadir]

#go through all subdirs 
for subdir in subdirs:
    hdf5files = os_dir.get_contained_files(subdir,'.hdf5')
    print hdf5files
    for hdf5file in hdf5files:
        writexdmf = MXDMF_maker.MXDMFmaker(hdf5file,subdir)