# -*- coding: utf-8 -*-
# Author: Alexandre Correia / MARETEC
# Email: alexandre.c.correia@tecnico.ulisboa.pt
# Last update: 2020-02-07

# python integrated packages
import os
import sys
import subprocess
import logging
from shutil import copy2, move
from datetime import datetime, timedelta
# other python packages
import yaml
# written for GetMeteoPy
import utils


def set_logger():
    global log
    log = logging.getLogger(__name__)
    log.setLevel(logging.INFO)
    formatter = logging.Formatter(fmt='%(asctime)s| %(message)s',
                                                                datefmt='%Y-%m-%d %H:%M:%S')

    # sends logs to stdout
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    log.addHandler(ch)



def open_yaml_file(path):
    log.info('Reading GetMeteoPy.yaml')
    with open(path, 'r') as yml_file:
        return yaml.safe_load(yml_file)


def get_start_and_end(path):
    log.info('Reading GetMeteoPy.dat')
    with open(path, 'r') as f:
        all_lines = f.readlines()
        all_lines = list(map(lambda x: x.replace('\n',''), all_lines))
        all_lines = list(filter(lambda x: len(x)>0, all_lines))
        for line in all_lines:
            if line.find('START') > -1:
                start = line[line.find(':')+1:].strip(' ')
            if line.find('END') > -1:
                end = line[line.find(':')+1:].strip(' ')
    try:
        start = datetime.strptime(start, '%Y %m %d %H %M %S')
        end = datetime.strptime(end, '%Y %m %d %H %M %S')
    except ValueError:
        start = datetime.strptime(start, '%Y %m %d')
        end = datetime.strptime(end, '%Y %m %d')
    log.info('START set to ' + str(start))
    log.info('END set to ' + str(end))
    return start, end


def check_existing_file(yaml, start, end):
    return os.path.isfile('./History/'+yaml['outputPrefix']+'_'+datetime.strftime(start, '%Y-%m-%d')+'_'+datetime.strftime(end, '%Y-%m-%d')+'.hdf5')


def copy_meteo_files(yaml, meteoModel, start, end):
    # copies meteo hdf5 files in the format ModelName_YYYYMMDDHH_YYYYMMDDHH.hdf5
    log.info('Searching for files for model ' + meteoModel)
    if 'meteoRemoveStartupSeconds' in yaml['meteoModels'][meteoModel].keys():
        meteoRemoveStartupSeconds = yaml['meteoModels'][meteoModel]['meteoRemoveStartupSeconds']
        log.info('meteoRemoveStartupSeconds keyword active and set to ' + str(meteoRemoveStartupSeconds) + ' seconds')
    else:
        meteoRemoveStartupSeconds = 0

    files_in_range = []
    meteoFileFormat = yaml['meteoModels'][meteoModel]['meteoFileFormat']
    if meteoFileFormat.count('%Y') == 1:
        for root, dirs, files in os.walk(yaml['meteoModels'][meteoModel]['meteoDirectory']):
            for f in files:
                try:
                    file_date_start = datetime.strptime(f, yaml['meteoModels'][meteoModel]['meteoFileFormat'])
                except ValueError:
                    log.debug('File: ' + f + ' does not fit the FileFormat specified of: ' + meteoFileFormat + ', ignoring.')
                    continue
                file_dates = [file_date_start, file_date_start + timedelta(seconds=yaml['meteoModels'][meteoModel]['meteoFileTotalSeconds'])]
                if file_dates[1] < start or end < file_dates[0]:
                    continue
                else:
                    files_in_range.append([os.path.join(root, f), file_dates[0], file_dates[1]])
    elif meteoFileFormat.count('%Y') == 2:
        codes_found = {}
        file_name = ['', '']
        in_start = True
        index = 0
        for l in meteoFileFormat:
            if l is '%':
                code = '%' + meteoFileFormat[index+1]
                if code in codes_found.keys():
                    codes_found.update({code: codes_found[code] + 1})
                    if in_start:
                        in_start = False
                else:
                    codes_found.update({code: 1})
            if in_start:
                file_name[0] += l
            else:
                file_name[1] += l
            index += 1
        file_name_example = [datetime(2000, 1, 1).strftime(x) for x in file_name]
        file_name_length = [len(x) for x in file_name_example]
        for root, dirs, files in os.walk(yaml['meteoModels'][meteoModel]['meteoDirectory']):
                for f in files:
                    file_split = [f[:file_name_length[0]], f[-file_name_length[1]:]]
                    try:
                        file_dates = [datetime.strptime(file_split[0], file_name[0]), datetime.strptime(file_split[1], file_name[1])]
                    except ValueError:
                        log.debug('File: ' + f + ' does not fit the FileFormat specified of: ' + meteoFileFormat + ', ignoring.')
                        continue
                    if file_dates[1] < start or end < file_dates[0]:
                        continue
                    else:
                        files_in_range.append([os.path.join(root, f), file_dates[0], file_dates[1]])
    files_in_range = sorted(files_in_range)

    if files_in_range == []:
        log.info('\n--- ERROR ---\nNo files with the specified name or date range were found in ' + yaml['meteoModels'][meteoModel]['meteoDirectory'])
        exit(1)

    log.info('Files found with data in the requested time range:')
    for f in files_in_range: log.info('- ' + f[0])

    if meteoRemoveStartupSeconds > 0:
        i = 0
        for _ in files_in_range:
            files_in_range[i][1] = files_in_range[i][1] + timedelta(seconds=meteoRemoveStartupSeconds)
            i += 1

    files_with_everything_inside = []
    for f in files_in_range:
        if (f[1] <= start) and (end <= f[2]):
            files_with_everything_inside.append(f)

    log.info('Copying files:')
    files_copied = []
    file_to_copy = ''
    if len(files_with_everything_inside) == 0:
        for f in files_in_range:
            log.info('- ' + f[0])
            copy2(f[0], os.path.basename(f[0]))
            files_copied.append(os.path.basename(f[0]))
    elif len(files_with_everything_inside) == 1:
        log.info('- ' + files_with_everything_inside[0][0])
        copy2(files_with_everything_inside[0][0], os.path.basename(files_with_everything_inside[0][0]))
        files_copied.append(os.path.basename(files_with_everything_inside[0][0]))
    elif len(files_with_everything_inside) > 1:
        file_to_copy = files_with_everything_inside[0][0]
        files_with_everything_inside.pop(0)
        for f in files_with_everything_inside:
            if os.path.getmtime(f[0]) > os.path.getmtime(file_to_copy):
                file_to_copy = f[0]
        log.info('- ' + file_to_copy)
        copy2(file_to_copy, os.path.basename(file_to_copy))
        files_copied.append(os.path.basename(file_to_copy))

    if meteoRemoveStartupSeconds > 0:
        log.info('Removing requested startup instants for files:')
        for f in files_copied:
            log.info('- ' + f)
            utils.remove_hdf5_startup_instants(f, meteoRemoveStartupSeconds)

    return files_copied


def write_ConvertToHDF5Action_glue(yaml, meteoModel, start, end, files_to_glue):
    log.info('Writing ConvertToHDF5Action.dat for GLUES HDF5 FILES action')
    with open('./ConvertToHDF5Action.dat', 'w') as f:
        f.write('<begin_file>\n')
        f.write('\n')
        f.write('! Written by GetMeteoPy\n')
        f.write('{0:30}{1}'.format('ACTION', ': ' + 'GLUES HDF5 FILES' + '\n'))
        f.write('{0:30}{1}'.format('OUTPUTFILENAME', ': ' + meteoModel + '.hdf5' + '\n'))
        f.write('\n')
        f.write('{0:30}{1}'.format('START', ': ' + datetime.strftime(start, '%Y %m %d %H %M %S') + '\n'))
        f.write('{0:30}{1}'.format('END', ': ' + datetime.strftime(end, '%Y %m %d %H %M %S') + '\n'))
        f.write('\n')
        f.write('<<begin_list>>\n')
        for hdf5_file in files_to_glue:
            f.write(hdf5_file+'\n')
        f.write('<<end_list>>\n')
        f.write('\n')
        if ('mohidKeywords' in yaml.keys()) and ('GLUES HDF5 FILES' in yaml['mohidKeywords'].keys()):
            f.write('! Additional keywords\n')
            for keyword in yaml['mohidKeywords']['GLUES HDF5 FILES'].keys():
                try: f.write('{0:30}{1}'.format(keyword, ': ' + yaml['mohidKeywords']['GLUES HDF5 FILES'][keyword] + '\n'))
                except TypeError: f.write('{0:30}{1}'.format(keyword, ': ' + str(yaml['GLUES HDF5 FILES']['mohidKeywords'][keyword]) + '\n'))
            f.write('\n')
        f.write('<end_file>\n')
    copy2('./ConvertToHDF5Action.dat', './ConvertToHDF5Action-GLUES_HDF5_FILES.dat')


def write_ConvertToHDF5Action_interpolate(yaml, start, end):
    log.info('Writing ConvertToHDF5Action.dat for INTERPOLATE GRIDS action')
    with open('./ConvertToHDF5Action.dat', 'w') as f:
        f.write('<begin_file>\n')
        f.write('\n')
        f.write('! Written by GetMeteoPy\n')
        f.write('{0:30}{1}'.format('ACTION', ': ' + 'INTERPOLATE GRIDS' + '\n'))
        f.write('{0:30}{1}'.format('TYPE_OF_INTERPOLATION', ': ' + str(yaml['typeOfInterpolation']) + '\n'))
        f.write('\n')
        f.write('{0:30}{1}'.format('START', ': ' + datetime.strftime(start, '%Y %m %d %H %M %S') + '\n'))
        f.write('{0:30}{1}'.format('END', ': ' + datetime.strftime(end, '%Y %m %d %H %M %S') + '\n'))
        f.write('\n')
        f.write('{0:30}{1}'.format('OUTPUTFILENAME', ': ' +
                yaml['outputPrefix']+'_'+datetime.strftime(start, '%Y-%m-%d')+'_'+datetime.strftime(end, '%Y-%m-%d')+'.hdf5' + '\n'))
        f.write('{0:30}{1}'.format('NEW_GRID_FILENAME', ': ' + yaml['bathymetry'] + '\n'))
        f.write('\n')
        for meteoModel in yaml['meteoModels'].keys():
            f.write('{0:30}{1}'.format('FATHER_FILENAME', ': ' + meteoModel + '.hdf5' + '\n'))
            f.write('{0:30}{1}'.format('FATHER_GRID_FILENAME', ': ' + yaml['meteoModels'][meteoModel]['meteoDatFile'] + '\n'))
        f.write('\n')
        if 'propertiesToInterpolate' in yaml.keys():
            f.write('<<BeginFields>>\n')
            for p in yaml['propertiesToInterpolate']:
                f.write(p+'\n')
            f.write('<<EndFields>>\n')
            f.write('\n')
        if ('mohidKeywords' in yaml.keys()) and ('INTERPOLATE GRIDS' in yaml['mohidKeywords'].keys()):
            f.write('! Additional keywords\n')
            for keyword in yaml['mohidKeywords']['INTERPOLATE GRIDS'].keys():
                try: f.write('{0:30}{1}'.format(keyword, ': ' + yaml['mohidKeywords']['INTERPOLATE GRIDS'][keyword] + '\n'))
                except TypeError: f.write('{0:30}{1}'.format(keyword, ': ' + str(yaml['mohidKeywords']['INTERPOLATE GRIDS'][keyword]) + '\n'))
            f.write('\n')
        f.write('<end_file>\n')
    copy2('./ConvertToHDF5Action.dat', './ConvertToHDF5Action-INTERPOLATE_GRIDS.dat')


def write_ConvertToHDF5Action_patch(yaml, start, end):
    log.info('Writing ConvertToHDF5Action.dat for PATCH HDF5 FILES action')
    with open('./ConvertToHDF5Action.dat', 'w') as f:
        f.write('<begin_file>\n')
        f.write('\n')
        f.write('! Written by GetMeteoPy\n')
        f.write('{0:30}{1}'.format('ACTION', ': ' + 'PATCH HDF5 FILES' + '\n'))
        f.write('{0:30}{1}'.format('TYPE_OF_INTERPOLATION', ': ' + str(yaml['typeOfInterpolation']) + '\n'))
        f.write('\n')
        f.write('{0:30}{1}'.format('START', ': ' + datetime.strftime(start, '%Y %m %d %H %M %S') + '\n'))
        f.write('{0:30}{1}'.format('END', ': ' + datetime.strftime(end, '%Y %m %d %H %M %S') + '\n'))
        f.write('\n')
        f.write('{0:30}{1}'.format('OUTPUTFILENAME', ': ' +
                yaml['outputPrefix']+'_'+datetime.strftime(start, '%Y-%m-%d')+'_'+datetime.strftime(end, '%Y-%m-%d')+'.hdf5' + '\n'))
        f.write('{0:30}{1}'.format('NEW_GRID_FILENAME', ': ' + yaml['bathymetry'] + '\n'))
        f.write('\n')
        for meteoModel in yaml['meteoModels'].keys():
            f.write('<<begin_father>>\n')
            f.write('{0:30}{1}'.format('FATHER_FILENAME', ': ' + meteoModel + '.hdf5' + '\n'))
            f.write('{0:30}{1}'.format('FATHER_GRID_FILENAME', ': ' + yaml['meteoModels'][meteoModel]['meteoDatFile'] + '\n'))
            f.write('{0:30}{1}'.format('LEVEL', ': ' + str(yaml['meteoModels'][meteoModel]['level']) + '\n'))
            f.write('<<end_father>>\n\n')
        if 'propertiesToInterpolate' in yaml.keys():
            f.write('<<BeginFields>>\n')
            for p in yaml['propertiesToInterpolate']:
                f.write(p+'\n')
            f.write('<<EndFields>>\n')
            f.write('\n')
        if ('mohidKeywords' in yaml.keys()) and ('PATCH HDF5 FILES' in yaml['mohidKeywords'].keys()):
            f.write('! Additional keywords\n')
            for keyword in yaml['mohidKeywords']['PATCH HDF5 FILES'].keys():
                try: f.write('{0:30}{1}'.format(keyword, ': ' + yaml['mohidKeywords']['PATCH HDF5 FILES'][keyword] + '\n'))
                except TypeError: f.write('{0:30}{1}'.format(keyword, ': ' + str(yaml['mohidKeywords']['PATCH HDF5 FILES'][keyword]) + '\n'))
            f.write('\n')
        f.write('<end_file>\n')
    copy2('./ConvertToHDF5Action.dat', './ConvertToHDF5Action-PATCH_HDF5_FILES.dat')


def check_ConvertToHDF5Action_sucess(filename):
    with open(filename, 'r') as f:
        last_lines = f.readlines()[-40:]

    for l in last_lines:
        if l.find('ConvertToHDF5 successfully terminated') != -1:
            return
    log.info('\n--- ERROR ---\nConvertToHDF5.exe was not sucessfull\nCheck ' + filename + ' for more information')
    exit(1)


def move_interpolated_hdf5_to_History_folder(yaml, start, end):
    move(yaml['outputPrefix']+'_'+datetime.strftime(start, '%Y-%m-%d')+'_'+datetime.strftime(end, '%Y-%m-%d')+'.hdf5',
        yaml['outputDirectory']+yaml['outputPrefix']+'_'+datetime.strftime(start, '%Y-%m-%d')+'_'+datetime.strftime(end, '%Y-%m-%d')+'.hdf5')


def delete_copied_and_created_files(yaml, hdf5_files_to_delete):
    for meteoModel in yaml['meteoModels'].keys():
        try:
            os.remove(meteoModel + '.hdf5')
        except FileNotFoundError:
            pass
    os.remove('ConvertToHDF5Action.dat')
    for f in hdf5_files_to_delete:
        try:
            os.remove(f)
        except FileNotFoundError:
            pass


def main():
    set_logger()

    log.info('Starting')
    
    yaml = open_yaml_file('GetMeteoPy.yaml')
    start, end = get_start_and_end('./GetMeteoPy.dat')
    
    if os.path.isdir('./History') is False:
        os.mkdir('./History')

    hdf5_files_to_delete = []
    # copy and glue
    for meteoModel in yaml['meteoModels'].keys():
        hdf5_files_copied = copy_meteo_files(yaml, meteoModel, start, end)
        hdf5_files_to_delete += hdf5_files_copied
        if len(hdf5_files_copied) == 1:
            move(hdf5_files_copied[0], meteoModel + '.hdf5')
        elif len(hdf5_files_copied) >1:
            write_ConvertToHDF5Action_glue(yaml, meteoModel, start, end, hdf5_files_copied)
            with open('ConvertToHDF5Action-GLUES_HDF5_FILES.log', 'w') as logfile:
                log.info('Running ConvertToHDF5.exe')
                p = subprocess.Popen(yaml['convertToHDF5exe'], stdout=logfile, stderr=logfile)
                p.wait()
            check_ConvertToHDF5Action_sucess('ConvertToHDF5Action-GLUES_HDF5_FILES.log')
    
    # interpolate
    if len(yaml['meteoModels'].keys()) == 1:
        write_ConvertToHDF5Action_interpolate(yaml, start, end)
        with open('ConvertToHDF5Action-INTERPOLATE_GRIDS.log', 'w') as logfile:
            log.info('Running ConvertToHDF5.exe')
            p = subprocess.Popen(yaml['convertToHDF5exe'], stdout=logfile, stderr=logfile)
            p.wait()
        check_ConvertToHDF5Action_sucess('ConvertToHDF5Action-INTERPOLATE_GRIDS.log')
        log.info('Moving file to output directory')
        move_interpolated_hdf5_to_History_folder(yaml, start, end)
    # patch
    elif len(yaml['meteoModels'].keys()) > 1:
        write_ConvertToHDF5Action_patch(yaml, start, end)
        with open('ConvertToHDF5Action-PATCH_HF5_FILES.log', 'w') as logfile:
            log.info('Running ConvertToHDF5.exe')
            p = subprocess.Popen(yaml['convertToHDF5exe'], stdout=logfile, stderr=logfile)
            p.wait()
        check_ConvertToHDF5Action_sucess('ConvertToHDF5Action-PATCH_HF5_FILES.log')
        log.info('Moving file to output directory')
        move_interpolated_hdf5_to_History_folder(yaml, start, end)
    # cleanup
    log.info('Deleting copied files')
    delete_copied_and_created_files(yaml, hdf5_files_to_delete)
    log.info('Finished')


if __name__ == '__main__':
    main()
