# -*- coding: utf-8 -*-

#this class is resposible for, given a MOHID HDF5 file, reading it's fields
#and writting a correspoing XDMF file

import sys
sys.path.append('../../Common')
import os_dir

import MXDMF_writer as writer

###############################################################################

class MXDMFmaker:
    def __init__(self, hdf5filename, directory):
        self.hdf5filename = os_dir.filename_without_ext(hdf5filename)
        self.directory = directory
        self.xdmfwriter = writer.MXDMFwriter(self.hdf5filename, self.directory)
        
        self.xdmfwriter.openfile()
        self.xdmfwriter.writeheader()