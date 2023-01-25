import pandas as pd
from datetime import datetime
from pprint import pprint
import os
import numpy as np


def get_mohid_timeseries_1_file(file, remove_time_0=True):
    f = open(file)
    prev_l = ''
    while True:
        l = f.readline()
        if l == '':
            break
        if l.find('<BeginTimeSerie>') != -1:
            header = prev_l
            break
        prev_l = l
    data = []
    while True:
        l = f.readline()
        if l == '':
            break
        if l.find('<EndTimeSerie>') != -1:
            break
        data.append(l)
    f.close()

    header = header.strip(' \n')
    header = header.split(' ')
    header = list(filter(None, header))
    header = ['date'] + header[7:]
    data = [x.strip(' \n') for x in data]
    if remove_time_0:
        data.pop(0)
    data = [x.split(' ') for x in data]
    data = [list(filter(None, x)) for x in data]
    data = [[float(x) for x in y] for y in data]
    data = [[datetime(int(x[1]), int(x[2]), int(x[3]), int(x[4]), int(x[5]), int(float(x[6])))] + x[7:] for x in data]
    df = pd.DataFrame.from_records(data, columns=header, index=header[0])

    return df


def get_mohid_timeseries(start, end, results_dir, filename, remove_time_0=True):
    dirs = list(os.walk(results_dir))[0][1]
    valid_dirs = []
    for d in dirs:
        d_check = d.split('_')
        d_check_start = datetime.strptime(d_check[0], '%Y-%m-%d')
        d_check_end = datetime.strptime(d_check[1], '%Y-%m-%d')
        if start <= d_check_start <= end or start <= d_check_end <= end:
            valid_dirs.append(results_dir + d)
    valid_files = []
    for d in valid_dirs:
        files = list(os.walk(d))[0][2]
        for f in files:
            if f == filename:
                valid_files.append(d + '/' + f)
    valid_files = sorted(valid_files)
    for f in valid_files:
        df = get_mohid_timeseries_1_file(f)
        if 'df_final' in locals():
            df_final = pd.concat([df_final, df])
        else:
            df_final = df
    for i in df_final.index.values:
        i_datetime = pd.Timestamp(i).to_pydatetime()
        if i_datetime < start or i_datetime > end:
            df_final = df_final.drop(i)
    return df_final


if __name__ == '__main__':
    print('Working...')
    results_dir = './Results_TimeSeries/'
    filename = 'StNazaireTG.srh'
    start = datetime(2019, 11, 15, 0, 0, 0)
    end = datetime(2019, 11, 18, 0, 0, 0)
    df = get_mohid_timeseries(start, end, results_dir, filename, remove_time_0=True)
    print('Finished.')
