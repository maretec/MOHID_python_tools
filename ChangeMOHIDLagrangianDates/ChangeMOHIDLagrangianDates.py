# -*- coding: utf-8 -*-
# Author: Alexandre Correia / MARETEC
# Email: alexandre.c.correia@tecnico.ulisboa.pt
# Last update: 2002-03-06
#
# This script finds the lines that specify the start and end of a MOHIDLagrangian settings .xml file
# and replaces the date values by what is specified in a .dat file.
#

# intrinsic python libraries
import os
import sys
import shutil
import logging
from datetime import datetime

# user made code
sys.path.append('../')
from mohid_reader import mohid_dat_reader


def setup_logger():
    global log
    log = logging.getLogger(__name__)
    log.setLevel(logging.INFO)
    formatter = logging.Formatter(
        fmt='%(asctime)s| %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    # sends logs to stdout
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    log.addHandler(ch)


def change_dates(dat):
    # making a backup of the .xml the file
    shutil.copy2(dat['MOHID_XML_FILE'], dat['MOHID_XML_FILE'] + '.bak')
    
    # opening and getting the current .xml file
    with open(dat['MOHID_XML_FILE'], 'r') as f:
        ls = f.readlines()
    
    # rewriting the .xml file
    f = open(dat['MOHID_XML_FILE'], 'w')
    for l in ls:
        # if line starts with '<parameter' and 'Start' is found, replaces the start date
        if l.strip().startswith('<parameter') and l.find('Start') != -1:
            # writes the line until value is found, then replaces the date
            f.write(
                l[:l.find('value')+5] + '="' + datetime.strftime(dat['START'],'%Y %m %d %H %M %S')
            )
            # writes what's after the date value from the original file
            l = l[l.find('value')+5:]
            l = l[l.find('"')+1:]
            l = l[l.find('"'):]
            f.write(l)
        # if line starts with '<parameter' and 'End' is found, replaces the end date
        elif l.strip().startswith('<parameter') and l.find('End') != -1:
            # writes the line until value is found, then replaces the date
            f.write(
                l[:l.find('value')+5] + '="' + datetime.strftime(dat['END'],'%Y %m %d %H %M %S')
            )
            # writes what's after the date value from the original file
            l = l[l.find('value')+5:]
            l = l[l.find('"')+1:]
            l = l[l.find('"'):]
            f.write(l)
        # if line doesn't start with '<parameter' or 'Start' and 'End' are not found, writes the
        # line with no change
        else:
            f.write(l)
    
    # closing the .xml file
    f.close()
    
    # deletes the backup of the .xml file
    os.remove(dat['MOHID_XML_FILE'] + '.bak')


def main():
    print('{:#^100}'.format(' Starting '+os.path.basename(__file__)+' ', fill='#'))
    setup_logger()
    dat = mohid_dat_reader.get_mohid_dat(os.path.basename(__file__).replace('.py','.dat'))
    log.info('Changing date values in ' + dat['MOHID_XML_FILE'])
    change_dates(dat)
    log.info('Finished sucessfully')


if __name__ == '__main__':
    main()
