# -*- coding: utf-8 -*-
"""
Created on Fri Jan 11 11:57:37 2019

@author: Angie
"""
import os
import sys
import argparse

import numpy as np
import netCDF4
import pandas as pd
#import datetime
#import matplotlib.pyplot as plt
#import xarray as xr

def get_contained_files(a_dir,extension):
    return [file for file in os.listdir(a_dir)
            if file.endswith(extension)]

def get_parser():

    """ Get parser object """
    parser=argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, description='')

    parser.add_argument('-i', dest='dir',
                        help='dir for netcdf time series',
                        action='store', required=True)


    ## Assign args to variables
    args=parser.parse_args()


    return args

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


#########IMPUT VALUES############################     

args = get_parser()

#ncfile= '6202403_Lajes_das_Flores_Buoy.nc'
WorkingFolder = args.dir #'\\\\davinci\\DataCenter\\DadosBase\\Oceanografia\\Fixed_Stations\\Monthly\\2018-05'
ncfilesfiles = get_contained_files(WorkingFolder,'.nc')
# this function converts one file only


#########STARTING Code############################     
for ncfile in ncfilesfiles:
    nc = netCDF4.Dataset(os.path.join(WorkingFolder, ncfile))
    print(ncfile)
    # get location of the bouy
    lat = nc.variables['LATITUDE'][0]
    lon = nc.variables['LONGITUDE'][0]
    try:
      depth_id = nc.variables['DEPH'][1,:]
      depth_var = nc.variables['DEPH'][:]
    except:
      depth_id=[0.0]
       #pass
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
    #print(LIST)

    for l in a:
        # create a pandas dataframe
        df = pd.DataFrame(dtime, columns=['date'])
        df['Seconds']=diff
        extract_date(df, 'date')
        #adding the variables
        for x in LIST:
            try: 
                varid= nc.variables[x].standard_name
                #print('Writing Standar Name ' + varid)  
                df[varid]= nc.variables[x][:,l]
            except:
               varid= nc.variables[x].long_name
               #print('Writing Long Name ' + varid)
               df[varid]= nc.variables[x][:,l]
            
            
        df=df.drop(columns=['date'])
        # create a list of header variables
        hd = list(df.columns)

        # Writing Mohid Format for all depths 

        depth2str=str(depth_id[l])
        depth2str_label = depth2str.replace(".", "p", 1)
        base_filename = ncfile.replace(".nc","")
        base_filename_out= base_filename.strip() + '_D_' + depth2str_label + '.ets'
        print('Writing MOHID format ' + base_filename_out)
        writedata2mohid_format(WorkingFolder,base_filename_out,df,depth2str)

###################################


# Create Pandas time series object
#ts = pd.Series(var[:,1],index=dtime,name=vname)

# Use Pandas time series plot method
#ts.plot(
#   title='Location: Lon=%.2f, Lat=%.2f' % ( lon, lat),legend=True)
#plt.ylabel(var.units);

