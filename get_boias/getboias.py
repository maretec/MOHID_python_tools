#!/home/jjdd/bin/miniconda2/envs/snirh/bin/python
#-*: 'coding: utf-8 -*-

import sys
import os
import os.path
import argparse
import datetime
from datetime import timedelta, date
import time
import re
#import netCDF4
#import numpy as np
import json
from ftplib import FTP
import shutil



def get_parser():

    """ Get parser object """
    parser=argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, description='A program to download timeseries from CMES')


    parser.add_argument('-v', '--verbose',
                        help="verbose",
                        action="store_true")

    parser.add_argument('-c', '--config',
                        help="path file stations list", default='stations_id.dat',
                        action='store', required=False)

    parser.add_argument('-s',dest='stations',
                        help='stations  id',
                        nargs='+', action='store', required=False)

    parser.add_argument('-strd', dest='strday', type=lambda d: datetime.datetime.strptime(d, '%Y%m%d'),
                        help="the Start Date :'format YYYYMMDD ",
                        required=False)
    parser.add_argument('-endd', dest='endday', type=lambda d: datetime.datetime.strptime(d, '%Y%m%d'),
                        help="the End Date format YYYYMMDD (Inclusive)",
                        required=False)

    parser.add_argument('-m', dest='monthly',
                        help='monthly type',
                        action='store_true', required=False)

    parser.add_argument('-strm', dest='strmonth', type=lambda d: datetime.datetime.strptime(d, '%Y%m'),
                        help="the Start Date :'format YYYYMM ",
                        required=False)
    parser.add_argument('-endm', dest='endmonth', type=lambda d: datetime.datetime.strptime(d, '%Y%m'),
                        help="the End Date format YYYYMM (Inclusive)",
                        required=False)

    parser.add_argument('-d', dest='output',
                        help='directory where output are downloadec',
                        default=os.path.dirname(os.path.abspath(__file__)) + '/dowload',
                        action='store', required=False)

    parser.add_argument('-u', dest='username',
                        help='Username to access FTP server',
                        default='your_user_name',
                        action='store', required=False)

    parser.add_argument('-p', dest='password',
                        help='Password to access FTP server',
                        default='your_password',
                        action='store', required=False)

    parser.add_argument('-mv', '--moveto', help="path to archive download files",
                        default='your_directory',
                        action="store", required=False)

    ## Assign args to variables
    args=parser.parse_args()


    if args.strmonth or args.endmonth:
        args.monthly = True

    if args.strday or args.endday:
        if not args.strday or not args.endday:
            print(" You must specify start and end day\n")
            parser.print_help()
            parser.exit()
            sys.exit(1)

    if args.strmonth or args.endmonth:
        if not args.strmonth or not args.endmonth:
            print(" You must specify start and end month\n")
            parser.print_help()
            parser.exit()
            sys.exit(1)

    ## add 1 month to workaround the daterange iteration
    if args.endmonth:
        args.endmonth = args.endmonth + datetime.timedelta(days=32)


    ## makedir output dir if not exist
    args.output=os.path.join(args.output, '')
    if not os.path.exists(args.output):
        os.makedirs(args.output)

    return args

def read_stations():
    if not args.stations and os.path.isfile(args.config):
        with open(args.config) as f:
            return json.load(f)
    else:
        return 0

def daterange(startDate, endDate, delta=timedelta(days=1)):
    currentDate = startDate
    while currentDate <= endDate:
        yield currentDate
        currentDate += delta

def download(station):
    hostname = 'nrt.cmems-du.eu'

    ## login FTP
    try:
        ftp = FTP(hostname)
        ftp.login(args.username,args.password)
    except:
        print (" ERROR: Cannot connect to the FTP server")
        sys.exit(1)
        return


    paths = ['/Core/INSITU_IBI_NRT_OBSERVATIONS_013_033', '/Core/INSITU_GLO_NRT_OBSERVATIONS_013_030']

    file_exist = False
    for path_count, path in enumerate(paths):

        if file_exist:
            break

        print(' trying in ' + path)

        if args.monthly:
            path += '/monthly/mooring'
            delta_time = datetime.timedelta(days=32)
            output = args.output + '/monthly'
            if not os.path.exists(output):
                os.makedirs(output)

        else:
            path += '/latest'
            delta_time = datetime.timedelta(days=1)
            output = args.output + '/daily'


        ## change to path directory
        ftp.cwd(path)

        if (not args.strday or not args.endday) and (not args.strmonth or not args.endmonth):
            date_end = datetime.datetime.now()
            date_str = date_end - delta_time
        elif args.strday and args.endday:
            date_str = args.strday
            date_end = args.endday
        elif args.strmonth and args.endmonth:
            date_str = args.strmonth
            date_end = args.endmonth


        ## iterate throw days
        for date in daterange(date_str, date_end, delta=delta_time):
            if args.monthly:
                time_dir = date.strftime("%Y%m")
                time_dir_output = date.strftime("%Y-%m")

                if 'REGION' in station:
                    if station['REGION'] == 'GL TS MO':
                        file_url = 'GL_' + time_dir + '_TS_MO_' + station['DOWNSTA_NAME'] + '.nc'
                    elif station['REGION'] == 'MO TS MO':
                        file_url = 'MO_' + time_dir +'_TS_MO_' + station['DOWNSTA_NAME']  + '.nc'
                    else:
                        print(' New REGION: ' + station['REGION'])
                        sys.exit(1)
                else:
                    file_url = 'IR_' + time_dir + '_TS_MO_' + station['DOWNSTA_NAME'] + '.nc'

            else:
                time_dir = date.strftime("%Y%m%d")

                date_after = date + delta_time
                time_dir_output = date.strftime("%Y-%m-%d") + '_' + date_after.strftime("%Y-%m-%d")

                if 'REGION' in station:
                    if station['REGION'] == 'GL TS MO':
                        file_url = 'GL_LATEST_TS_MO_' + station['DOWNSTA_NAME'] + '_' + time_dir + '.nc'
                    elif station['REGION'] == 'MO TS MO':
                        file_url = 'MO_LATEST_TS_MO_' + station['DOWNSTA_NAME'] + '_' + time_dir + '.nc'
                    else:
                        print(' New REGION: ' + station['REGION'])
                        sys.exit(1)
                else:
                    file_url = 'IR_LATEST_TS_MO_' + station['DOWNSTA_NAME'] + '_' + time_dir + '.nc'



            #print(' process ' + time_dir)


            output2 = output + '/' + time_dir_output
            if not os.path.exists(output2):
                os.makedirs(output2)


            ## check if directory exist
            time_list = ftp.nlst()
            if time_dir in time_list:

                ## change to day_dir
                directory = path + '/' + time_dir
                ftp.cwd(directory)

                files = ftp.nlst()

                ## check if file exist
                if file_url in files:
                    file_exist = True
                    #print(' ' + file + ' exist')
                    try:
                        filename = output2 + '/' + station['STATION_NAME'] + '.nc'
                        ftp.retrbinary('RETR %s' % file_url, open(filename, 'wb').write)
                    except:
                        print(" Error download " + file_url)

                else:
                    #print(' ' + file_url + ' not exist')
                    if path_count == len(paths)-1:
                        print("\n" + file_url + ' not found!')

            else:
                print(' ' + time_dir + ' directory not exist')

            ftp.cwd(path)

    ftp.quit()

def movefiles():
    if not os.path.exists(args.moveto):
                os.makedirs(args.moveto)

    dirs = os.listdir(args.output)
    for dir in dirs:
        shutil.move(args.output + '/'+ dir, args.moveto)


if __name__ == '__main__':

    args = get_parser()

    data = read_stations()

    stations = data['stations']
    tides = data['tide']
    for station in stations:
        print('processing ' + station['STATION_NAME'] + '...')
        download(station)

    for station in tides:
        print('processing ' + station['STATION_NAME'] + '...')
        download(station)

    print("\n\n move files to " + args.moveto)
    movefiles()


