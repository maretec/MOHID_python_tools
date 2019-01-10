import h5py
import sys
import logging
import ModuloGeneralReadOptions as MGRO
import ModuloMapsLonLat2Center
import ModuloMapsDraw
import ModuloMapsValidation
import os
from subprocess import call
import subprocess
import ModuloMaps as MM
import ModuloTimeSeriesPlot as MT
import inspect

try:
    configFile = 'PythonFigures.dat'

    name=sys.argv[0]
    filename_zip = inspect.getframeinfo(inspect.currentframe()).filename

    logging.FileHandler(filename=filename_zip.split('\\')[-2][:-4] + '.log', mode='w')
    logging.basicConfig(filename=filename_zip.split('\\')[-2][:-4] + '.log',level=logging.INFO,format='%(asctime)s %(message)s',datefmt='%Y/%m/%d %H:%M:%S')

    logging.info(': Started')


    options = MGRO.readOptions.readoptions (configFile)

    del configFile

    if options.plot_image_type == 'maps':
        MM.ModuloMapaDeCampos.Maps(options)
    elif options.plot_image_type == 'timeseries':
        MT.ModuloTimeSeriesPlot.TimeSeries(options)
    else:
        logging.info(': Error 001 : Only Available options for PLOT_IMAGE_TYPE are: MAPS or TIMESERIES.')
        logging.shutdown()
        sys.exit()


    logging.info(': Python Image Generator successfully terminated')
    logging.shutdown()

except Exception as ex:
    logging.error(': Description major error: ' + str(ex))
    logging.info(': Error 000 : Major error!!!')
    logging.shutdown()
    print ('BOOOOOMMMMMMMMM')

sys.exit()
