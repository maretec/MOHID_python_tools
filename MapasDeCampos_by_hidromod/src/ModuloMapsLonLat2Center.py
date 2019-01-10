import logging
import numpy as np
import ModuloGeneralReadOptions as MGRO

class lonlat2center(object):
    """Get Mohid Cell center, this receives 2d arrays"""

    def __init__(self,lon,lat):
        self.lonC=None
        self.latC=None
        self.lon=lon
        self.lat=lat
        
        lonlat2center.calculo(self,lon,lat)
       
    def calculo(self,lon,lat):
        
        try:
            nLines = lon.shape[0]
            nColumns = lon.shape[1]

            self.lonC = np.zeros((nLines-1, nColumns-1))
            self.latC = np.zeros((nLines-1, nColumns-1))

            for i in range(0,nLines-1):
                loni = lon[i];
                lati = lat[i];
                loni1 = lon[i+1];
                lati1 = lat[i+1];
                for j in range(0,nColumns-1):

                    XSW = loni[j];
                    YSW = lati[j];
                    XSE = loni[j+1];
                    YSE = lati[j+1];
                    XNE = loni1[j+1];
                    YNE = lati1[j+1];
                    XNW = loni1[j];
                    YNW = lati1[j];

                    self.lonC[i][j] = (XSW + XSE + XNE + XNW) / 4.;
                    self.latC[i][j]= (YSW + YSE + YNE + YNW) / 4.;

        except Exception as ex:
            logging.info(': Modulo Maps Lon2Lat2Center : Error 001 : Cannot calculate Lon Lat cell center ' + ex)
            logging.shutdown()
            sys.exit()

    def lonlatToCellCenter(lon,lat):

        logging.info(': Converting Lon and Lat faces to Lon Lat cell center')
        llcc = lonlat2center(lon,lat)
        
        logging.info(': Finished Converting Lon and Lat faces to Lon Lat cell center')
            
        return llcc