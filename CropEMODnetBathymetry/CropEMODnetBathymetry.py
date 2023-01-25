# -*- coding: utf-8 -*-
# Author: Alexandre Correia / MARETEC
# Email: alexandre.c.correia@tecnico.ulisboa.pt
# Last update: 2002-03-06

# This script crops a bathymetry file from the EMODnet bathymetry service. Will probably work for 
# other sources of bathymetry but was not tested.
# At the moment assumes data comes in the following order: lon, lat, Z or X, Y, Z
#

# intrinsic python libraries
import sys

# user made code
sys.path.append('../')
from mohid_reader import mohid_dat_reader


def crop_bathymetry(dat):
    # attributting input file data to variables
    input_file = dat['INPUT_FILE']
    output_file = dat['OUTPUT_FILE']

    lon_min = float(dat['LON_MIN'])
    lon_max = float(dat['LON_MAX'])
    lat_min = float(dat['LAT_MIN'])
    lat_max = float(dat['LAT_MAX'])

    input_separator = dat['INPUT_SEPARATOR']

    # default output separator is whitespace
    if 'OUTPUT_SEPARATOR' in dat.keys():
        output_separator = dat['OUTPUT_SEPARATOR']
    else:
        output_separator = ' '

    if 'WRITE_MOHID_XYZ_BLOCK' in dat.keys() and dat['WRITE_MOHID_XYZ_BLOCK']:
        MOHIDxyzBlock = True
    else:
        MOHIDxyzBlock = False

    # opens the input and output files
    f1 = open(input_file, 'r')
    f2 = open(output_file, 'w')

    # if WRITE_MOHID_XYZ_BLOCK is True writes the MOHID xyz block
    if MOHIDxyzBlock:
        f2.write('<begin_xyz>\n')

    # cycling through all the data lines
    while True:
        # reads line from the original file
        l = f1.readline()
        # if line is empty, end of file has been reached, exits cycle
        if l == '':
            break
        # removing whitespaces from beggining and end of line
        l = l.strip()
        # removes seperator from the end of the line if one is found
        if l.endswith(input_separator):
            l = l.rstrip(input_separator)
        # removes linebreak characther from end of the line
        l = l.strip('\n')
        # splits l string into a list of strings
        l = l.split(input_separator)
        # transforms l from a list of stings to a list of float numbers
        l = list(map(lambda x: float(x), l))
        # checks if data point is inside or outside given limits
        if lon_min <= l[0] <= lon_max and lat_min <= l[1] <= lat_max:
            # when inside limits writes the line to the new file with the given separator
            l = list(map(lambda x: str(x), l))
            f2.write(output_separator.join(l) + '\n')

    if MOHIDxyzBlock:
        f2.write('<end_xyz>\n')

    # closing files
    f1.close()
    f2.close()


def main():
    print('Working...')
    dat = mohid_dat_reader.get_mohid_dat('CropEMODnetBathymetry.dat')
    print(dat)
    crop_bathymetry(dat)
    print('Finished.')


if __name__ == '__main__':
    main()