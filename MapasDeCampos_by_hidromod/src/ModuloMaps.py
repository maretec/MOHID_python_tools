import h5py
import sys
import logging
import ModuloGeneralReadOptions
import ModuloMapsLonLat2Center as MML2C
import ModuloMapsDraw as MMD
import ModuloMapsValidation as MMV
import time 

class ModuloMapaDeCampos(object):

    def __init__(self,options):
    
        try:
            file = h5py.File(options.filePath,  "r")
            logging.info(': Opening ' + options.filePath)
        except Exception as ex:
            logging.info(': Modulo Maps : Error 001 : Cannot open HDF5 file.')
            logging.shutdown()
            sys.exit()

        # Read Longitude, Latitude and Time
        try:
            lat=file['/Grid/Latitude']
        except Exception as ex:
            logging.info(': Modulo Maps : Error 002 : Cannot read /Grid/Latitude from file ' + options.filePath)
            logging.shutdown()
            sys.exit()

        try:
            lon=file['/Grid/Longitude']
        except Exception as ex:
            logging.info(': Modulo Maps : Error 003 : Cannot read /Grid/Longitude from file ' + options.filePath)
            logging.shutdown()
            sys.exit()

            
        try:
            times = file['/Time']
        except Exception as ex:
            logging.info(': Modulo Maps : Error 004 : Cannot read /Time from file ' + options.filePath)
            logging.shutdown()
            sys.exit()


        lonlatcellcenter = MML2C.lonlat2center.lonlatToCellCenter(lon[0:lon.shape[0],0:lon.shape[1]],lat[0:lon.shape[0],0:lon.shape[1]])

        logging.info(': Drawing Image... ')


        if options.plot_type==1:
            try :
                for x in progressbar((range(1,len(times)+1,options.dt)), "Python Image Generated: ", 40):
                    options.drawmoment=x                                                    #used to keep track of the draw image number

                    timeIndex = "_"+str(x).zfill(5)
                    options.timeIndex_end = timeIndex


                    #calcula a % do ciclo para aparesentar no AquaSafe
                    time.sleep(0.1) # any calculation you need


                    if options.drawBathymetry==1:
                        MMD.drawImage.draw(file, options, lonlatcellcenter,timeIndex)
                        break
                    else:
                        MMD.drawImage.draw(file, options, lonlatcellcenter,timeIndex)
            except Exception as ex:
                logging.info(': Error 005 : Failed to Perform Draw # ' + x + options.filePath)
                logging.shutdown()
                sys.exit()            

        elif options.plot_type==2:
            try :
                    options.lastmoment=len(times)+1

                    timeIndex = "_"+str('1').zfill(5)
                    options.timeIndex_end = "_"+str(len(times)).zfill(5)

                    MMV.Validation.GridAspect(file,options,lonlatcellcenter,timeIndex)
            except Exception as ex:
                logging.info(': Modulo Maps : Error 005 : Failed to Draw Image ' + options.filePath)
                logging.shutdown()
                sys.exit()

        else:             
            try:
                logging.info(': Modulo Maps : Error 006 : Available options 1 - Field Maps, 2 - Validation Maps.')
                logging.info(': Modulo Maps : Error 006 : Please choose the one you need.')
                logging.shutdown()
                sys.exit()
            except Exception as ex:
                logging.shutdown()
                sys.exit()

    
        logging.info(': Finished Drawing Image ')

        logging.info(': Closing ' + options.filePath)
        file.close()
        #getMemory()

    def Maps(options):
        
        #antiga chamada ao executavel que fazia a validaçao de hdf5
        #if options.plot_type==2:
        #    MMV.Validation._hdf5valida(options)
        

        ModuloMapaDeCampos(options)


def progressbar(it, prefix="", size=60):
    count = len(it)
    def _show(_i):
        x = int(size*_i/count)
        sys.stdout.write("%s[%s%s] %i/%i\r" % (prefix, "#"*x, "."*(size-x), _i, count))
        sys.stdout.flush()

    _show(0)
    for i, item in enumerate(it):
        yield item
        _show(i+1)
    sys.stdout.write("\n")
    sys.stdout.flush()