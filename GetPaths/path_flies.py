# -*- coding: utf-8 -*-
import  os


###############################################################################
def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]

def get_contained_files(a_dir,extension):
    return [file for file in os.listdir(a_dir)
            if file.endswith(extension)]    
###############################################################################

#basedir= 'D:\\Climatology\\DATA\\CMEMS\\2018-07'
#File_ext='12.hdf5'

basedir= 'D:\\algarve\\Data\\RADAR\\totals'
File_ext='.tuv'

hdf5files = get_contained_files(basedir,File_ext)

with open('your_file.txt', 'w') as f:
    for fl in hdf5files:
        fullpath = basedir + '\\'
        OUTPUTFILENAME = os.path.join(fullpath, fl) + "\n"     
        f.write(OUTPUTFILENAME)
  
    
