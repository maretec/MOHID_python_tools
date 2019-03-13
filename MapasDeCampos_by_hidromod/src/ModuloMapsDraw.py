import timeit
import ModuloMapsBasemaps as MMB
import sys
import datetime
import logging
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable, axes_size
from scipy.misc import imread
import matplotlib.cbook as cbook
import ModuloMapsFunctions as MI
import ModuloTimeSeriesFunctions as MTSF
import ModuloGeneralReadOptions as MGRO

class drawImage(object):
    """Get Mohid Cell center, this receives 2d arrays"""

    # The class "constructor" - It's actually an initializer
    def __init__(self,file, options, lonlatcellcenter,timeIndex):
        
        import logging

        try:
            if options.scalar is not None:
                try:
                    logging.info(': Reading ' + options.scalar+timeIndex)
                    if options.drawBathymetry == 1:
                        dsaux=file[options.scalar]
                    elif options.plot_image_type == 'maps' and options.plot_type == 2:
                        dsaux=file[options.scalar]
                    else:
                        dsaux=file[options.scalar+timeIndex]

                    dim = np.ndim(dsaux)
                    if dim is 2:
                        aux = dsaux[0:lonlatcellcenter.lonC.shape[0], 0:lonlatcellcenter.lonC.shape[1]]
                    elif dim is 3:
                        if options.layerDepth == 'surface':
                            aux = dsaux[dsaux.shape[0]-1,0:lonlatcellcenter.lonC.shape[0], 0:lonlatcellcenter.lonC.shape[1]]
                        else:
                            aux = dsaux[options.layerDepth,0:lonlatcellcenter.lonC.shape[0], 0:lonlatcellcenter.lonC.shape[1]]

                    if options.fillValue is not None:
                        for i in range(0,len(options.fillValue)):
                            aa = float(options.fillValue[i])
                            aux[aux == aa] = None
                            del aa
                        del i
                        
                    if options.conversionfactor is None:
                        self.dsScalar = aux
                    else:
                        self.dsScalar = aux*options.conversionfactor


                    
                    del aux, dsaux

                except Exception as ex:
                    logging.info(': Modulo Maps Draws : Error 001 : Cannot process scalar ' + options.scalar+timeIndex)
                    logging.shutdown()
                    sys.exit()
            else:
                raise Exception ('No scalar field defined!')
        except Exception as ex:
            logging.info(': Modulo Maps Draws : Error 002 : No scalar field defined!')
            logging.shutdown()
            sys.exit()

        if options.vectorX is not None and options.vectorY is not None:
            try:
                logging.info(': Reading ' + options.vectorX+timeIndex)
                dsaux =file[options.vectorX+timeIndex]

                dim = np.ndim(dsaux)
                if dim is 2:
                    aux = dsaux[0:lonlatcellcenter.lonC.shape[0], 0:lonlatcellcenter.lonC.shape[1]]
                elif dim is 3:
                    if options.layerDepth == 'surface':
                        aux = dsaux[dsaux.shape[0]-1,0:lonlatcellcenter.lonC.shape[0], 0:lonlatcellcenter.lonC.shape[1]]
                    else:
                        aux = dsaux[options.layerDepth,0:lonlatcellcenter.lonC.shape[0], 0:lonlatcellcenter.lonC.shape[1]]

                aux[np.isnan(self.dsScalar)] = np.nan
                self.dsVectorx=aux
                del aux, dsaux
            except Exception as ex:
                logging.info(': Modulo Maps Draws : Error 003: Cannot process vectorX ' + options.vectorX+timeIndex)
                logging.shutdown()
                sys.exit()

            try:
                logging.info(': Reading ' + options.vectorY+timeIndex)
                dsaux =file[options.vectorY+timeIndex]

                dim = np.ndim(dsaux)
                if dim is 2:
                    aux = dsaux[0:lonlatcellcenter.lonC.shape[0], 0:lonlatcellcenter.lonC.shape[1]]
                elif dim is 3:
                    if options.layerDepth == 'surface':
                        aux = dsaux[dsaux.shape[0]-1,0:lonlatcellcenter.lonC.shape[0], 0:lonlatcellcenter.lonC.shape[1]]
                    else:
                        aux = dsaux[options.layerDepth,0:lonlatcellcenter.lonC.shape[0], 0:lonlatcellcenter.lonC.shape[1]]

                aux[np.isnan(self.dsScalar)] = np.nan     
                self.dsVectory=aux
                del aux, dsaux 
            except Exception as ex:
                logging.info(': Modulo Maps Draws : Error 004 : Cannot process vectorY ' + options.vectorY+timeIndex)
                logging.shutdown()
                sys.exit() 

        if options.streamX is not None and options.streamY is not None:
            try:
                logging.info(': Reading ' + options.streamX+timeIndex)
                dsaux =file[options.streamX+timeIndex]

                dim = np.ndim(dsaux)
                if dim is 2:
                    aux = dsaux[0:lonlatcellcenter.lonC.shape[0], 0:lonlatcellcenter.lonC.shape[1]]
                elif dim is 3:
                    if options.layerDepth == 'surface':
                        aux = dsaux[dsaux.shape[0]-1,0:lonlatcellcenter.lonC.shape[0], 0:lonlatcellcenter.lonC.shape[1]]
                    else:
                        aux = dsaux[options.layerDepth,0:lonlatcellcenter.lonC.shape[0], 0:lonlatcellcenter.lonC.shape[1]]

                aux[np.isnan(self.dsScalar)] = np.nan
                self.dsstreamx=aux
                del aux, dsaux
            except Exception as ex:
                logging.info(': Modulo Maps Draws : Error 003: Cannot process streamX ' + options.streamX+timeIndex)
                logging.shutdown()
                sys.exit()

            try:
                logging.info(': Reading ' + options.streamY+timeIndex)
                dsaux =file[options.streamY+timeIndex]

                dim = np.ndim(dsaux)
                if dim is 2:
                    aux = dsaux[0:lonlatcellcenter.lonC.shape[0], 0:lonlatcellcenter.lonC.shape[1]]
                elif dim is 3:
                    if options.layerDepth == 'surface':
                        aux = dsaux[dsaux.shape[0]-1,0:lonlatcellcenter.lonC.shape[0], 0:lonlatcellcenter.lonC.shape[1]]
                    else:
                        aux = dsaux[options.layerDepth,0:lonlatcellcenter.lonC.shape[0], 0:lonlatcellcenter.lonC.shape[1]]

                aux[np.isnan(self.dsScalar)] = np.nan     
                self.dsstreamy=aux
                del aux, dsaux 
            except Exception as ex:
                logging.info(': Modulo Maps Draws : Error 004 : Cannot process streamY ' + options.streamY+timeIndex)
                logging.shutdown()
                sys.exit() 


        try:
            logging.info(': Reading ' + '/Time/Time'+timeIndex)
            self.time = file['/Time/Time'+timeIndex]
            self.time_end = file['/Time/Time'+options.timeIndex_end]
        except Exception as ex:
            logging.info(': Modulo Maps Draws : Error 006 : Cannot process time ' + '/Time/Time'+timeIndex)
            logging.shutdown()
            sys.exit() 
        
        if options.Xmin is None:     
            options.Xmin  = np.nanmin(np.nanmin(lonlatcellcenter.lonC, axis=1), axis=0)

        if options.Xmax is None:
            options.Xmax  = np.nanmax(np.nanmax(lonlatcellcenter.lonC, axis=1), axis=0)

        if options.Ymin is None:
            options.Ymin = np.nanmin(np.nanmin(lonlatcellcenter.latC, axis=1), axis=0)  

        if options.Ymax is None:
            options.Ymax  = np.nanmax(np.nanmax(lonlatcellcenter.latC, axis=1), axis=0)

        self.lon_minf = np.floor(options.Xmin)
        self.lon_maxf = np.ceil(options.Xmax)
        self.lat_minf = np.floor(options.Ymin)
        self.lat_maxf = np.ceil(options.Ymax)

        self.options = options
        self.lonlatcellcenter = lonlatcellcenter
        self.timeIndex = timeIndex

        if options.plot_type ==1:
            tic = timeit.default_timer()
            drawImage.__saveImage(self)
            toc = timeit.default_timer()
            logging.info(': Image Created in ' + str(round(toc-tic,2)) + ' seconds')

        elif options.plot_type ==2:
            tic = timeit.default_timer()
            drawImage.__saveImage(self)
            toc = timeit.default_timer()
            logging.info(': Image Created in ' + str(round(toc-tic,2)) + ' seconds')

    def __saveImage(self):

        from PIL import Image
        from mpl_toolkits.basemap import Basemap
        import datetime
        import numpy as np
        import gc
        import logging
        import re
        from matplotlib.patches import Polygon
        from matplotlib.collections import PatchCollection
        from matplotlib.colors import LogNorm
        import pickle
        import time
        logging.info(': Creating figure... ')

        

        if self.options.plot_type == 1:
            try:
                logging.info(': Starting to Generate Figure ')
                plt.clf()

                logging.info(': Drawing Basemap ')
                if self.options.worldImage == 1 and self.options.gssh == 0:
                    try:
                        MMB.Basemaps.get_ESRIBasemap(self.options.Xmin,self.options.Xmax,self.options.Ymin,self.options.Ymax,self)

                        m_name= 'm.pickle'
                        fig_name = 'fig.pickle'

                        f=open(m_name, 'rb')
                        m = pickle.load(f)
                        f.close()

                        f=open(fig_name, 'rb')
                        fig = pickle.load(f)
                        f.close()
                    except Exception as ex:
                        logging.info(': Modulo Maps Draws : Error 007 : Cannot acess wms WorldImage')
                        logging.shutdown()
                        sys.exit()

                elif self.options.gssh == 1 and self.options.worldImage == 0:
                    try:
                        logging.info(': Accessing WMS World GSSH CoastLines...')
                        fig=plt.figure()
                        MMB.Basemaps.get_GSSH(self)

                    except Exception as ex:
                        logging.info(': Modulo Maps Draws : Error 008 : Cannot acess wms GSSH')
                        logging.shutdown()
                        sys.exit()  
                        
                elif self.options.gssh == 0 and self.options.worldImage == 0 and self.options.coastline == 1  :
                    try:
                        fig=plt.figure()
                        m = Basemap(llcrnrlon=self.options.Xmin,llcrnrlat=self.options.Ymin,urcrnrlon=self.options.Xmax,urcrnrlat=self.options.Ymax)
                        #devia passar para uma função todo o bloco de geraçao de imagens a partir de .dat de linha de costa JGRR - 2017 11 28
                        lala='%.0f'
                        if self.options.dx >=.1 and self.options.dx <1:
                            lala = '%.1f'
                        elif self.options.dx >=.01 and self.options.dx <.1:
                            lala = '%.2f'
                        m.plot(self.options.X,self.options.Y,linewidth=0.4, color='k')      
                        plt.xticks(np.arange(self.options.Xmin, self.options.Xmax, self.options.dx))
                        plt.yticks(np.arange(self.options.Ymin, self.options.Ymax, self.options.dy))

                    except Exception as ex:
                        logging.info(': Modulo Maps Draws : Error 009 : Basemap error')
                        logging.shutdown()
                        sys.exit() 

                logging.info(': Drawing Parales and Meridians ')
                if self.options.dx == None: 
                    try:
                        d1 = np.ceil(np.mean([self.options.Ymax-self.options.Ymin,self.options.Xmax-self.options.Xmin])*100)/100;

                        if d1<1:
                            self.options.dx =  np.ceil((d1/10)*100)/100
                        else:
                            self.options.dx = np.ceil(d1/10)
                    except Exception as ex:
                        logging.info(': Modulo Maps Draws : Error 008 : Draw parallels and meridians')
                        logging.shutdown()
                        sys.exit()
                if self.options.dy == None:
                        self.options.dy = self.options.dx

                logging.info(': Fixing from UTC Timezone ')
                MI.Maps._Datetime(self)
                date_object = drawImage.__utcToTimeZone(datetime.datetime(int(self.Y), int(self.M), int(self.D), int(self.h), int(self.m), int(self.s)), self.options.timeZone)

                logging.info(': Ploting Title ')
                if self.options.title is not '':
                    plt.title(self.options.title+' \n %s ' % date_object.strftime('%b. %d, %Y %H:%M UTC%z'),size=9)
                #else:
                #    plt.title(' \n %s ' % date_object.strftime('%b. %d, %Y %H:%M UTC%z'),size=9)

                MI.Maps._colormap(self)
                MI.Maps._ColormapLimit(self)
                MI.Maps._Contour(self)
                MI.Maps._Pcolor(self)
                MI.Maps._DrawQuiver(self)
                MI.Maps._Polygon(self)
                MI.Maps._StreamLines(self)
                plt.axes().set_aspect(1);      
                MI.Maps._AxisLabels(self)
                MI.Maps._PointsLabel(self)
                MI.Maps._HidroLogo(self)
                MI.Maps._ColorBar(self)
                MI.Maps._FigureOutName(self,date_object)
                MI.Maps._Transparency(self)
                MI.Maps._ImageSize(self,fig)
                MI.Maps._SaveImage(self,fig)
                MI.Maps._Image2JPEG(self)

                logging.info(': Cleaning... ')
                gc.collect()
                # este ciclo percorre a lista de imagens e fecha a ultima primeiro, caso se faça close all nao funciona, pois tem de ser por estar ordem
                for i in reversed(plt.get_fignums()):              
                    plt.close(i)
            except Exception as ex:
                logging.info(': Modulo Maps Draws : Error 010 : FAIL to generate map with Option 1' + ex)
                logging.shutdown()
                sys.exit()

        elif self.options.plot_type == 2:
            try:
                logging.info(': Starting to Generate Figure ')
                
                logging.info(': Drawing Step #1 ')
                
                if self.options.worldImage==1:
                    MMB.Basemaps.get_ESRIBasemap_Validation(self)
                elif self.options.gssh==1:
                    MMB.Basemaps.get_GSSH(self)
                
                logging.info(': Drawing Step #2 ')                
                if self.options.dx == None:
                    try:
                        d1 = np.ceil(np.mean([self.options.Ymax-self.options.Ymin,self.options.Xmax-self.options.Xmin])*100)/100;

                        if d1<1:
                            self.options.dx =  np.ceil((d1/10)*100)/100
                        else:
                            self.options.dx = np.ceil(d1/10)
                    except Exception as ex:
                        logging.info(': Modulo Maps Draws : Error 011 : Draw parallels and meridians')
                        logging.shutdown()
                        sys.exit()
                if self.options.dy == None:
                        self.options.dy = self.options.dx

                logging.info(': Drawing Step #3 ')
                MI.Maps._Datetime(self)
                date_object = drawImage.__utcToTimeZone(datetime.datetime(int(self.Y), 
                                                                          int(self.M), 
                                                                          int(self.D), 
                                                                          int(self.h), 
                                                                          int(self.m), 
                                                                          int(self.s)), 
                                                        self.options.timeZone)
                self.date_object_end = drawImage.__utcToTimeZone(datetime.datetime(int(self.Y_end), 
                                                                              int(self.M_end), 
                                                                              int(self.D_end), 
                                                                              int(self.h_end), 
                                                                              int(self.m_end), 
                                                                              int(self.s_end)), 
                                                            self.options.timeZone)

                logging.info(': Drawing Step #4 ')
                if self.options.title is not None:
                    plt.title(self.options.title)
                #else:
                #    plt.title(' \n %s ' % date_object.strftime('%b. %d, %Y %H:%M UTC%z'),size=9)

                logging.info(': Drawing Step #5 ')
                MI.Maps._colormap(self)
                logging.info(': Drawing Step #6 ')
                MI.Maps._ColormapLimit(self)
                logging.info(': Drawing Step #7 ')
                MI.Maps._Contour(self)
                logging.info(': Drawing Step #8 ')
                MI.Maps._Pcolor(self)
                logging.info(': Drawing Step #9 ')
                MI.Maps._DrawQuiver(self)
                logging.info(': Drawing Step #10 ')
                MI.Maps._Polygon(self)
                logging.info(': Drawing Step #11 ')
                MI.Maps._StreamLines(self)
                logging.info(': Drawing Step #12 ')
                MI.Maps._AxisLabels(self)
                logging.info(': Drawing Step #13 ')
                MI.Maps._PointsLabel(self)
                logging.info(': Drawing Step #14 ')
                #MI.Maps._HidroLogo(self)
                logging.info(': Drawing Step #15 ')
                MI.Maps._ColorBar(self)
                logging.info(': Drawing Step #16 ')
                MI.Maps._FigureOutName(self,date_object)
                logging.info(': Drawing Step #17 ')
                MI.Maps._Transparency(self)

                if self.options.subplot_index == self.options.validation_grid[0]*self.options.validation_grid[1]-1:
                    fig = plt.gcf()
                    logging.info(': Valiation Map : Drawing Step # 1/4 ')
                    MI.Maps._ImageSize(self,fig)
                    logging.info(': Valiation Map : Drawing Step # 2/4 ')
                    fig.suptitle(self.options.titleOrigianal, size=self.options.fontsize+4)     
                    #plt.tight_layout(pad=1, w_pad=1, h_pad=1.0)
                    logging.info(': Valiation Map : Drawing Step # 3/4 ')
                    MI.Maps._SaveImage(self,fig)
                    logging.info(': Valiation Map : Drawing Step # 4/4 ')
                    MI.Maps._Image2JPEG(self)
            except Exception as ex:
                logging.info(': Modulo Maps Draws : Error 012 : FAIL to generate map with Option 2' + ex)
                logging.shutdown()
                sys.exit()       
                

    def __utcToTimeZone(date, timezone):

        import pytz
        import logging

        try:
            # Time Reference
            win_tz = {'AUS Central Standard Time': 'Australia/Darwin',
             'AUS Eastern Standard Time': 'Australia/Sydney',
             'Afghanistan Standard Time': 'Asia/Kabul',
             'Alaskan Standard Time': 'America/Anchorage',
             'Arab Standard Time': 'Asia/Riyadh',
             'Arabian Standard Time': 'Asia/Dubai',
             'Arabic Standard Time': 'Asia/Baghdad',
             'Argentina Standard Time': 'America/Buenos_Aires',
             'Atlantic Standard Time': 'America/Halifax',
             'Azerbaijan Standard Time': 'Asia/Baku',
             'Azores Standard Time': 'Atlantic/Azores',
             'Bahia Standard Time': 'America/Bahia',
             'Bangladesh Standard Time': 'Asia/Dhaka',
             'Belarus Standard Time': 'Europe/Minsk',
             'Canada Central Standard Time': 'America/Regina',
             'Cape Verde Standard Time': 'Atlantic/Cape_Verde',
             'Caucasus Standard Time': 'Asia/Yerevan',
             'Cen. Australia Standard Time': 'Australia/Adelaide',
             'Central America Standard Time': 'America/Guatemala',
             'Central Asia Standard Time': 'Asia/Almaty',
             'Central Brazilian Standard Time': 'America/Cuiaba',
             'Central Europe Standard Time': 'Europe/Budapest',
             'Central European Standard Time': 'Europe/Warsaw',
             'Central Pacific Standard Time': 'Pacific/Guadalcanal',
             'Central Standard Time': 'America/Chicago',
             'Central Standard Time (Mexico)': 'America/Mexico_City',
             'China Standard Time': 'Asia/Shanghai',
             'Dateline Standard Time': 'Etc/GMT+12',
             'E. Africa Standard Time': 'Africa/Nairobi',
             'E. Australia Standard Time': 'Australia/Brisbane',
             'E. South America Standard Time': 'America/Sao_Paulo',
             'Eastern Standard Time': 'America/New_York',
             'Eastern Standard Time (Mexico)': 'America/Cancun',
             'Egypt Standard Time': 'Africa/Cairo',
             'Ekaterinburg Standard Time': 'Asia/Yekaterinburg',
             'FLE Standard Time': 'Europe/Kiev',
             'Fiji Standard Time': 'Pacific/Fiji',
             'GMT Standard Time': 'Europe/London',
             'GTB Standard Time': 'Europe/Bucharest',
             'Georgian Standard Time': 'Asia/Tbilisi',
             'Greenland Standard Time': 'America/Godthab',
             'Greenwich Standard Time': 'Atlantic/Reykjavik',
             'Hawaiian Standard Time': 'Pacific/Honolulu',
             'India Standard Time': 'Asia/Calcutta',
             'Iran Standard Time': 'Asia/Tehran',
             'Israel Standard Time': 'Asia/Jerusalem',
             'Jordan Standard Time': 'Asia/Amman',
             'Kaliningrad Standard Time': 'Europe/Kaliningrad',
             'Korea Standard Time': 'Asia/Seoul',
             'Libya Standard Time': 'Africa/Tripoli',
             'Line Islands Standard Time': 'Pacific/Kiritimati',
             'Magadan Standard Time': 'Asia/Magadan',
             'Mauritius Standard Time': 'Indian/Mauritius',
             'Middle East Standard Time': 'Asia/Beirut',
             'Montevideo Standard Time': 'America/Montevideo',
             'Morocco Standard Time': 'Africa/Casablanca',
             'Mountain Standard Time': 'America/Denver',
             'Mountain Standard Time (Mexico)': 'America/Chihuahua',
             'Myanmar Standard Time': 'Asia/Rangoon',
             'N. Central Asia Standard Time': 'Asia/Novosibirsk',
             'Namibia Standard Time': 'Africa/Windhoek',
             'Nepal Standard Time': 'Asia/Katmandu',
             'New Zealand Standard Time': 'Pacific/Auckland',
             'Newfoundland Standard Time': 'America/St_Johns',
             'North Asia East Standard Time': 'Asia/Irkutsk',
             'North Asia Standard Time': 'Asia/Krasnoyarsk',
             'Pacific SA Standard Time': 'America/Santiago',
             'Pacific Standard Time': 'America/Los_Angeles',
             'Pacific Standard Time (Mexico)': 'America/Santa_Isabel',
             'Pakistan Standard Time': 'Asia/Karachi',
             'Paraguay Standard Time': 'America/Asuncion',
             'Romance Standard Time': 'Europe/Paris',
             'Russia Time Zone 10': 'Asia/Srednekolymsk',
             'Russia Time Zone 11': 'Asia/Kamchatka',
             'Russia Time Zone 3': 'Europe/Samara',
             'Russian Standard Time': 'Europe/Moscow',
             'SA Eastern Standard Time': 'America/Cayenne',
             'SA Pacific Standard Time': 'America/Bogota',
             'SA Western Standard Time': 'America/La_Paz',
             'SE Asia Standard Time': 'Asia/Bangkok',
             'Samoa Standard Time': 'Pacific/Apia',
             'Singapore Standard Time': 'Asia/Singapore',
             'South Africa Standard Time': 'Africa/Johannesburg',
             'Sri Lanka Standard Time': 'Asia/Colombo',
             'Syria Standard Time': 'Asia/Damascus',
             'Taipei Standard Time': 'Asia/Taipei',
             'Tasmania Standard Time': 'Australia/Hobart',
             'Tokyo Standard Time': 'Asia/Tokyo',
             'Tonga Standard Time': 'Pacific/Tongatapu',
             'Turkey Standard Time': 'Europe/Istanbul',
             'US Eastern Standard Time': 'America/Indianapolis',
             'US Mountain Standard Time': 'America/Phoenix',
             'UTC': 'Etc/GMT',
             'UTC+12': 'Etc/GMT-12',
             'UTC+01': 'Etc/GMT-1',
             'UTC-02': 'Etc/GMT+2',
             'UTC-11': 'Etc/GMT+11',
             'Ulaanbaatar Standard Time': 'Asia/Ulaanbaatar',
             'Venezuela Standard Time': 'America/Caracas',
             'Vladivostok Standard Time': 'Asia/Vladivostok',
             'W. Australia Standard Time': 'Australia/Perth',
             'W. Central Africa Standard Time': 'Africa/Lagos',
             'W. Europe Standard Time': 'Europe/Berlin',
             'West Asia Standard Time': 'Asia/Tashkent',
             'West Pacific Standard Time': 'Pacific/Port_Moresby',
             'Yakutsk Standard Time': 'Asia/Yakutsk'} 
        
            from_zone = pytz.timezone("Etc/GMT")#UTC
            to_zone = pytz.timezone(win_tz[timezone])

            date = from_zone.normalize(from_zone.localize(date))
            demandedDate = date.astimezone(to_zone)
 
            return demandedDate
        except Exception as ex:
                logging.info(': Modulo Maps Draws : Error 013 : Get datetime zone')
                logging.shutdown()
                sys.exit()

    def draw(file, options, lonlatcellcenter,timeIndex):

        drawImage(file, options, lonlatcellcenter,timeIndex)

