import timeit
import ModuloMapsBasemaps
import sys
import datetime
import logging
from PIL import Image
import numpy as np

class TS(object):
      
    def __init__(self,options):
        self.oi=oi;

    def _savefigTS(self,fig):
        try:
            if self.plot_type is not 0:
                fig.savefig(self.figure_out, 
                            facecolor=self.figurecolor, 
                            edgecolor=self.figurecolor,
                            orientation='portrait', 
                            papertype=None, 
                            format=None,
                            transparent=self.figuretransparent, 
                            pad_inches=0.1,
                            dpi=self.dpi)
        except Exception as ex:
            logging.info(': Modulo TimeSeries Functions : Error 001 : Saving figure '  + ex)
            logging.shutdown()
            sys.exit()

    def _Image2JPEGTS(self):
        
        try:
            if self.plot_type is not 0:
                if self.CompressImage == 1 and self.figurequality is not None and self.figuretransparent is False:  
                    logging.info(': CompressImage figure... ')
                    Image.open(self.figure_out).save(self.figure_out, "JPEG", quality=self.figurequality, optimize=True)
        except Exception as ex:
            logging.info(': Modulo TimeSeries Functions : Error 002 : To compress image to JPEG '  + ex)
            logging.shutdown()
            sys.exit()

    def _Dynamic_plot_limit(Timeseries, ax, options, x):
        try:
            if  'RMSE' in options.timeseries_validation_parameters[x][0].split() and options.dynamic_limits == 1:  # se for pr observations e modelo escala é igual
                aux_1 = [np.floor(min(Timeseries[x].ValuesY)),np.ceil(max(Timeseries[x].ValuesY))]
                value=max(min(aux_1), max(aux_1), key=abs)
                ax.set(ylim=[abs(value)*-1,abs(value)])
            elif  'R' in options.timeseries_validation_parameters[x][0].split() and options.dynamic_limits == 1:  # se for pr observations e modelo escala é igual
                ax.set(ylim=[0,1])
        except Exception as ex:
            logging.info(': Modulo TimeSeries Functions : Error 003 : force Module values in colorbar for RMSE' + ex)
            logging.shutdown()
            sys.exit()
        