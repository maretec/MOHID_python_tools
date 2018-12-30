# -*- coding: utf-8 -*-

import os
import sys
sys.path.append('../../Common')

import os_dir as os_dir

################################################################################

#MOHID output hdf file directory
basepath = os.path.dirname(__file__)
datadir = os.path.abspath(os.path.join(basepath, "..", "TestFiles"))
print '--> Main working directory is', datadir 
#subdirs = os_dir.get_immediate_subdirectories(datadir)
#print subdirs
files = os_dir.get_contained_files(datadir,'.hdf5')
print files