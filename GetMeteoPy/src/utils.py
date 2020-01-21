import h5py
import os
from datetime import datetime, timedelta


def remove_hdf5_startup_instants(file_path, seconds_to_remove):
    f = h5py.File(file_path, 'r+')

    time_strings = list(f['Time'].keys())
    time_datetimes = []
    for k in f['Time']:
        time_datetimes.append([int(x) for x in list(f['Time'][k])])
    time_datetimes = [datetime(x[0], x[1], x[2], x[3], x[4], x[5]) for x in time_datetimes]

    last_time_to_keep = time_datetimes[0] + timedelta(seconds=seconds_to_remove)

    indexes_to_delete = []
    for time_str, time_date in zip(time_strings, time_datetimes):
        if time_date < last_time_to_keep:
            indexes_to_delete.append(time_str.replace('Time_',''))

    for i in indexes_to_delete:
        del f['Time']['Time_'+i]

    for k in f['Results'].keys():
        for i in indexes_to_delete:
            del f['Results'][k][k+'_'+i]

    i = 1
    for k in list(f['Time'].keys()):
        f['Time']['Time_'+str(i).zfill(5)] = f['Time'][k]
        del f['Time'][k]
        i += 1

    for k1 in list(f['Results'].keys()):
        i = 1
        for k2 in list(f['Results'][k1].keys()):
            f['Results'][k1][k1+'_'+str(i).zfill(5)] = f['Results'][k1][k2]
            del f['Results'][k1][k2]
            i += 1

    f.close()
