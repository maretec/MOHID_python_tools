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
import netCDF4
import numpy as np
import json
from ftplib import FTP
import shutil
import pandas as pd

date_base = None

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
                        help='directory where output are download',
                        default=os.path.dirname(os.path.abspath(__file__)) + '/dowload',
                        action='store', required=False)

    parser.add_argument('-u', dest='username',
                        help='Username to access FTP server',
                        default='fcampuzano',
                        action='store', required=False)

    parser.add_argument('-p', dest='password',
                        help='Password to access FTP server',
                        default='RAkopeci',
                        action='store', required=False)


    #parser.add_argument('-mv', '--moveto', help="move from download to archive dir",
    #                    default='archive',
    #                    action="store", required=False)
    parser.add_argument('-t', '--convert', help="Convert netcdf to mohid time series", action="store_true")

    #parser.add_argument('-t', '--convert', help="Convert netcdf to mohid time series", action="store", required=False)

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
            output = args.output + '/Monthly'
            if not os.path.exists(output):
                os.makedirs(output)
        else:
            path += '/latest'
            delta_time = datetime.timedelta(days=1)
            output = args.output + '/Daily'


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
                    elif station['REGION'] == 'IR TS MO':
                        file_url = 'IR_' + time_dir +'_TS_MO_' + station['DOWNSTA_NAME']  + '.nc'
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
                    elif station['REGION'] == 'IR TS MO':
                        file_url = 'IR_LATEST_TS_MO_' + station['DOWNSTA_NAME'] + '_' + time_dir + '.nc'
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

def get_contained_files(a_dir,extension):
    return [file for file in os.listdir(a_dir)
            if file.endswith(extension)]


def diff_dates(datetime):
    diffdt =  datetime - date_base
    return int(diffdt.total_seconds())
     
def extract_date(df, column):
    df["YY"]=df[column].apply(lambda x: x.year)
    df["MM"]=df[column].apply(lambda x: x.month)
    df["DD"]=df[column].apply(lambda x: x.day)
    df["HH"]=df[column].apply(lambda x: x.hour)
    df["mm"]=df[column].apply(lambda x: x.minute)
    df["ss"]=df[column].apply(lambda x: x.second )
    
def add_variable(ID,i):   
    df[ID]= nc.variables[ID][:,i]

def writedata2mohid_format(WorkingFolder,base_filename,df,depth_val):   
    with open(os.path.join(WorkingFolder, base_filename),'w') as outfile:
        outfile.writelines([ 'Time Serie Results File coming from MyOcean Netcdf files','\n'])
        outfile.writelines([ 'NAME                    : ',ncfile ,'\n'])
        outfile.writelines([ 'LOCALIZATION_I          :  -9999','\n'])
        outfile.writelines([ 'LOCALIZATION_J          :  -9999','\n'])
        outfile.writelines([ 'LOCALIZATION_K          :  -9999','\n'])
        outfile.writelines([ 'SERIE_INITIAL_DATA      :  ',str(df['YY'][0]),'. ',str(df['MM'][0]),'. ',str(df['DD'][0]),'. ',str(df['HH'][0]),'. ',str(df['mm'][0]),'. ',str(df['ss'][0]),'. ' ,'\n'])
        outfile.writelines([ 'COORD_X                 :  ',str(lon) ,'\n'])
        outfile.writelines([ 'COORD_Y                 :  ',str(lat) ,'\n'])
        outfile.writelines([ 'DEPTH                   :  ',depth_val ,'\n'])
        outfile.writelines([ 'TIME_UNITS              :  SECONDS' ,'\n'])
        
            #Priting Variables ColumnNames
        for item in hd:
                outfile.write("%s  " % item)
            
        outfile.writelines([  '\n']) 
        outfile.writelines([  '<BeginTimeSerie>' ,'\n'])
        df.to_string(outfile,header=False,index=False)
        outfile.writelines([  '\n'])
        outfile.writelines([  '<EndTimeSerie>' ,'\n'])
        
def convert_nc2mohidts():
    global date_base
    global ncfile
    global lon
    global lat
    global depth_val
    global hd
    
    if args.monthly:
        delta_time = datetime.timedelta(days=32)
        output = args.output + '/Monthly'
    else:
        delta_time = datetime.timedelta(days=1)
        output = args.output + '/Daily'

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
        else:
            time_dir = date.strftime("%Y%m%d")
            date_after = date + delta_time
            time_dir_output = date.strftime("%Y-%m-%d") + '_' + date_after.strftime("%Y-%m-%d")
        
            
        output2 = output + '/' + time_dir_output
        if os.path.exists(output2):
            print(output2)
            ncfilesfiles = get_contained_files(output2,'.nc')
            # this function converts one file only

            #########STARTING Code############################     
            for ncfile in ncfilesfiles:
                nc = netCDF4.Dataset(os.path.join(output2, ncfile))
                print(os.path.join(output2, ncfile))
                # get location of the bouy
                lat = nc.variables['LATITUDE'][0]
                lon = nc.variables['LONGITUDE'][0]
                try:
                   depth_id = nc.variables['DEPH'][1,:]
                   depth_var = nc.variables['DEPH'][:]
                except:
                   pass
                n=len(depth_id)
                a = np.arange(0, n, 1)
                #get time
                time_var = nc.variables['TIME']
                dtime = netCDF4.num2date(time_var[:],time_var.units)
                date_base = dtime[0]
                diff = list(map(diff_dates, dtime))

                #Get Variables
                # List of knowing variables name
                KEYS=list(nc.variables.keys())
                # Remove QC_Variables
                matching_QC = [s for s in KEYS if "_QC" in s];
                # Remove DM_Variables
                matching_DM = [s for s in KEYS if "_DM" in s];
                # add all list together
                stopwords = ['TIME','LATITUDE','LONGITUDE','DEPH','POSITIONING_SYSTEM','DC_REFERENCE','VPSP','FLU3'] +  matching_QC + matching_DM
                # add all list together will get all variables that are not QC variables
                LIST = [word for word in KEYS if word not in stopwords ]
                print(LIST)

                for l in a:
                    # create a pandas dataframe
                    df = pd.DataFrame(dtime, columns=['date'])
                    df['Seconds']=diff
                    extract_date(df, 'date')
                    #adding the variables
                    for x in LIST:
                        varid= nc.variables[x].standard_name
                        #try:
                        df[varid]= nc.variables[x][:,l]
                        #except:
                         #  pass
                    df=df.drop(columns=['date'])
                    # create a list of header variables
                    hd = list(df.columns)

                    # Writing Mohid Format for all depths 

                    depth2str=str(depth_id[l])
                    depth2str_label = depth2str.replace(".", "p", 1)
                    base_filename = ncfile.replace(".nc","")
                    base_filename_out= base_filename.strip() + '_D_' + depth2str_label + '.ets'
                    writedata2mohid_format(output2,base_filename_out,df,depth2str)

if __name__ == '__main__':

    args = get_parser()
    

    data = read_stations()

    if 'stations' in data:
        stations = data['stations']
        for station in stations:
            print('processing ' + station['STATION_NAME'] + '...')
            download(station)
    
    if 'tide' in data:
        tides = data['tide']
        for station in tides:
            print('processing ' + station['STATION_NAME'] + '...')
            download(station)

    #print("\n\n move files to " + args.moveto)
    #movefiles()

    if args.convert:
        convert_nc2mohidts()


