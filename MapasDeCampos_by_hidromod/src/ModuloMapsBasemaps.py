import os
import logging
import sys
import matplotlib.pyplot as plt
#os.environ['PROJ_LIB'] = r'C:\ProgramData\Anaconda3\pkgs\proj4-5.2.0-hfa6e2cd_1001\Library\share'
from mpl_toolkits.basemap import Basemap
import pickle
import numpy as np
import ModuloGeneralReadOptions as MGRO


class Basemaps(object):

    def get_ESRIBasemap(lon_min,lon_max,lat_min,lat_max,self):
        _m   = 'm.pickle'
        _fig = 'fig.pickle'

        try:
            if os.path.isfile(_m) and os.path.isfile(_fig) :
                try:
                    logging.info(': Looks like that i already have BasemapConfig. Using old configuration.')

                except Exception as ex:
                    logging.info(': Modulo Maps Basemaps : Error 001 : Failed to load old configuration')
                    logging.shutdown()
                    sys.exit()
            else:
                fig=plt.figure()

                logging.info(': Accessing WMS World Image for the first time')
                m = Basemap(
                        ellps='WGS84',
                        llcrnrlat=lat_min,
                        llcrnrlon=lon_min,
                        urcrnrlat=lat_max,
                        urcrnrlon=lon_max,
                        resolution=None)

                attempts=0
                success=False
                
                while attempts < 3 and not success:
                    try:
                        logging.info(': Modulo Basemaps : wms WorldImage access try #' + str(attempts+1))
                        m.arcgisimage(server='http://server.arcgisonline.com/ArcGIS', service=self.options.worldImage_esri, xpixels=1920, ypixels=None, dpi=96, verbose=False)
                        success = True
                        m.drawparallels(np.arange(self.lat_minf,self.lat_maxf,self.options.dy),
                                        labels=[1,0,0,1],
                                        labelstyle='+/-',
                                        color='None',
                                        fontsize=self.options.fontsize-1)

                        m.drawmeridians(np.arange(self.lon_minf,self.lon_maxf,self.options.dx),
                                        labels=[1,0,0,1],
                                        labelstyle='+/-',
                                        color='None',
                                        fontsize=self.options.fontsize-1)

                        with open(_m, 'wb') as fin:
                            m = pickle.dump(m,fin)
                        with open(_fig, 'wb') as fin1:
                            fig = pickle.dump(fig,fin1)

                    except Exception as ex:
                        logging.info(': Modulo Maps Basemaps : Error 002 : wms WorldImage access try #'+ 
                                     str(attempts+1) + ' failed. Trying again in 60s. ')
                        time.sleep(60)   
                        # after fail will w8 for 60 seconds before retry to connect with wms
                        attempts += 1
                return m
            del _m, _fig
        except Exception as ex:
            logging.info(': Modulo Maps Basemaps : Error 003 : Fail to generate')
            logging.shutdown()
            sys.exit()

    def get_ESRIBasemap_Validation(self):
        try:
            m= Basemap(
                    ellps='WGS84',
                    llcrnrlat=self.options.Ymin,
                    llcrnrlon=self.options.Xmin,
                    urcrnrlat=self.options.Ymax,
                    urcrnrlon=self.options.Xmax,
                    resolution=None)
            attempts=0
            success=False
                
            while attempts < 3 and not success:
                try:
                    logging.info(': Modulo Maps Basemaps : wms WorldImage access try #' + str(attempts+1))
                    m.arcgisimage(server='http://server.arcgisonline.com/ArcGIS', service=self.options.worldImage_esri, xpixels=1920, ypixels=None, dpi=96, verbose=False)
                    success = True

                    lala='%.0f'
                    if self.options.dx >=.1 and self.options.dx <1:
                        lala = '%.1f'
                    elif self.options.dx >=.01 and self.options.dx <.1:
                        lala = '%.2f'


                    paralels = m.drawparallels(np.arange(self.lat_minf,self.lat_maxf,self.options.dy),labels=[1,0,0,1],
                                               labelstyle='+/-',
                                               color='None',
                                               fontsize=self.options.fontsize-1, 
                                               fmt=lala)
                    meridians  = m.drawmeridians(np.arange(self.lon_minf,self.lon_maxf,self.options.dx),
                                                 labels=[1,0,0,1],
                                                 labelstyle='+/-',
                                                 color='None',
                                                 fontsize=self.options.fontsize-1,
                                                 fmt=lala)

                except Exception as ex:
                    logging.info(': Modulo Maps Basemaps : Error 004 : wms WorldImage access try #'+ 
                                    str(attempts+1) + ' failed. Trying again in 60s. ')
                    time.sleep(60)   
                    # after fail will w8 for 60 seconds before retry to connect with wms
                    attempts += 1                
        except Exception as ex:
            logging.info(': Modulo Maps Basemaps : Error 005 : Failed to get ESRImaps data ')
            logging.shutdown()
            sys.exit()             

    def get_GSSH(self):
        try:
            logging.info(': Modulo Maps Basemaps : Accessing GSSH coastline')

            lala='%.0f'
            if self.options.dx >=.1 and self.options.dx <1:
                lala = '%.1f'
            elif self.options.dx >=.01 and self.options.dx <.1:
                lala = '%.2f'
            elif self.options.dx >=.001 and self.options.dx <.01:
                lala = '%.3f'
            elif self.options.dx >=.0001 and self.options.dx <.001:
                lala = '%.4f'      
                
            m = Basemap(llcrnrlon=self.options.Xmin,llcrnrlat=self.options.Ymin,urcrnrlon=self.options.Xmax,urcrnrlat=self.options.Ymax,resolution=self.options.resolution)
            m.drawcoastlines(linewidth=0.4, linestyle='solid', color='k')
            m.drawcountries(linewidth=0.2, linestyle='solid', color='k')
            if self.options.fillContinents == 1:
                m.fillcontinents(color='white')
                if self.options.fillContinents_color is not 'white':
                    m.fillcontinents(color=self.options.fillContinents_color)
            paralels = m.drawparallels(np.arange(self.lat_minf,self.lat_maxf,self.options.dy),labels=[1,0,0,1],
                                        labelstyle='+/-',
                                        color='None',
                                        fontsize=self.options.fontsize-1, 
                                        fmt=lala)
            meridians  = m.drawmeridians(np.arange(self.lon_minf,self.lon_maxf,self.options.dx),
                                            labels=[1,0,0,1],
                                            labelstyle='+/-',
                                            color='None',
                                            fontsize=self.options.fontsize-1,
                                            fmt=lala)             
        except Exception as ex:
            logging.info(': Modulo Maps Basemaps : Error 006 : Failed to get Coastline data ')
            logging.shutdown()
            sys.exit()             