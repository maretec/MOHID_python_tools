# -*- coding: utf-8 -*-
"""
Created on Fri Feb  1 10:58:12 2019

@author: Angie

code to merge netcdf using xarray

"""
import os
import xarray
import glob
import pandas as pd

###############################################################################
def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]
    
def get_contained_files(a_dir,extension):
    return [file for file in os.listdir(a_dir)
            if file.endswith(extension)]     

def extract_date(df, column):
    df["YY"]=df[column].apply(lambda x: x.year)
    df["MM"]=df[column].apply(lambda x: x.month)
    df["DD"]=df[column].apply(lambda x: x.day)
    df["HH"]=df[column].apply(lambda x: x.hour)
    df["mm"]=df[column].apply(lambda x: x.minute)
    df["ss"]=df[column].apply(lambda x: x.second )

###############################################################################
    



Label= '_gridV.nc'

PATH= '\\\\francisco\\data\\'

filenames = glob.glob("\\\\francisco\\data\\*\\*gridU.nc")
dsmerged = xarray.open_mfdataset(filenames)
station=list(range(24))

fpath = 'river_nameU.csv'
with open(fpath, "r") as f: lst = [line.rstrip('\n \t') for line in f]
#df = dsmerged.to_dataframe()

for st in station:
    print(st)
    time_id    = dsmerged.time_counter[:]
    statio_idn =dsmerged.nbidta[:,:,st]
    statio_jdn =dsmerged.nbjdta[:,:,st]
    statio_ddn =dsmerged.nbrdta[:,:,st]
    #statio_vome =dsmerged.vomecrty[:,:,st]
    statio_vome =dsmerged.vozocrtx[:,:,st]

    df_id = statio_idn.to_dataframe()
    df_jd = statio_jdn.to_dataframe()
    df_ddn = statio_ddn.to_dataframe()
    df_vome=statio_vome.to_dataframe()

    frames = [df_id,df_jd,df_ddn,df_vome ]
    result = pd.concat(frames,axis=1, sort=False)
    print("gridU_"+ lst[st] +".csv")
    result.to_csv("gridU_"+lst[st] +".csv", index=True, header=True)


