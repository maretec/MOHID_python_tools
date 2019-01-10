import os
import logging
import sys
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import pickle
import numpy as np
import ModuloMapsDraw as MMD
import operator
import ModuloMapsFunctions as MI
import ModuloTimeSerieReader as MTSR
import ModuloTimeSeriesDraw as MTSD
import ModuloTimeSeriesFunctions as MTSF
from subprocess import call
import subprocess

class Validation(object):

    def __init__(self,file,options, lonlatcellcenter,timeIndex):
        self.lonC=lonlatcellcenter.lonC
        self.latC=lonlatcellcenter.latC
        self.lon=lonlatcellcenter.lon
        self.lat=lonlatcellcenter.lat


        # Criar o plot e a respectiva grid
        try: 
            if options.Xinches is None:
                fig  = plt.subplots(options.validation_grid[0],options.validation_grid[1],dpi=options.dpi)
            else:
                fig  = plt.subplots(options.validation_grid[0],options.validation_grid[1],dpi=options.dpi,figsize=(options.Xinches,options.Yinches))

            plt.subplots_adjust(left=.05, bottom=.05, right=.95, top=.95, wspace=options.validation_grid_ws, hspace=options.validation_grid_hs)

        except Exception as ex:
            logging.info(': Modulo Maps Validation : Error 001 : Failed to create subplot ' + ex)
            logging.shutdown()
            sys.exit()
            
    def Maps(file,options, lonlatcellcenter,timeIndex):

        try:         
            options.scalar                   = options.sorted_x[options.subplot_index][6].strip() + "_" + str('1').zfill(5)
            options.scalarMin                = float(options.sorted_x[options.subplot_index][2])
            options.scalarMax                = float(options.sorted_x[options.subplot_index][3])
            options.title                    = options.sorted_x[options.subplot_index][5].strip()
            options.colorbarSpacing          = float(options.sorted_x[options.subplot_index][4])
            options.legend                   = options.sorted_x[options.subplot_index][7].strip() 
            options.colormap                 = options.sorted_x[options.subplot_index][8].strip() 

            MMD.drawImage.draw(file, options, lonlatcellcenter,timeIndex)

        except Exception as ex:
            logging.info(': Modulo Maps Validation : Error 002 : Cannot Draw  ' + ex)
            logging.shutdown()
            sys.exit()

    def TimeSeries(file,options):

        try:

            #options.files_list='CompareOut_0'  # Nome igual ao de saida do hdf5valida

            # Lê as séries do filea dar nome.srh 
            try:
                #Timeseries=MTSR.MOHID.readTimeseries(options.files_list[0],'empty')
                # o nome e sempre em funcao da primeira serie que enrta no timeserie, deve ser a primeira da lista do begin_files_list
                Timeseries=['','','','','','','','','','','']
                if options.AQUASAFE is 0:
                    for x in range(0,len(options.timeseries_validation_parameters)):
                        Timeseries[x] = MTSR.MOHID.readTimeseries(options.files_list[x],int(options.timeseries_validation_parameters[x][2]))  
                        try:
                            if int(options.timeseries_validation_parameters[x][2]) is options.files_list_column[x]:
                                print('Good')
                            else:
                                logging.info(': Modulo Maps Validation : Error 002i : A coluna do ficheiro declarada na lista é diferente da do parametro pedido ' + str(options.files_list[x]) +'/'+ str(options.files_list_column[x]) )
                                logging.shutdown()
                                sys.exit()
                        except Exception as ex:
                            logging.info(': Modulo Maps Validation : Error 002i : A coluna do ficheiro declarada na lista é diferente da do parametro pedido ' + str(options.files_list[x]) +'/'+ str(options.files_list_column[x]) + ex)
                            logging.shutdown()
                            sys.exit()
                        logging.info(': Série ' + options.timeseries_validation_parameters[x][0] +'/coluna ' + str(int(options.timeseries_validation_parameters[x][2])) + ' lida com sucesso')
                elif options.AQUASAFE is 1:
                    for x in range(0,len(options.timeseries_validation_parameters)):
                        Timeseries[x] = MTSR.MOHID.readTimeseries(options.files_list[x],int(options.files_list_column[x]))  
                        logging.info(': Série ' + (options.timeseries_validation_parameters[x][0]).strip() +'/coluna ' + str(int(options.timeseries_validation_parameters[x][2])) + ' lida com sucesso')                    
            except Exception as ex:
                logging.info(': Modulo Maps Validation : Error 003 : Falha a ler a Timeserie de validação ' + str(options.files_list) + ex)





            try:
                MTSD.Draw_timeseries.__init__(options.plot_type,Timeseries,options)
            except:
                logging.info(': Modulo Maps Validation : Error 004 : Falha a desenhar')
                logging.shutdown()
                sys.exit()  

            if options.subplot_index == options.validation_grid[0]*options.validation_grid[1]-1:
                fig = plt.gcf()
                logging.info(': Valiation Map : Drawing Step # 1/4 ')

                initime = Timeseries[x].ValuesX_datenum[0]
                endtime = Timeseries[x].ValuesX_datenum[-1]
                fig.suptitle(options.titleOrigianal +
                            str(initime.strftime('%b. %d, %Y %H:%M')) +
                            '   -   ' +
                           str(endtime.strftime('%b. %d, %Y %H:%M UTC%z')), size=options.fontsize+1)

                logging.info(': Valiation Map : Drawing Step # 3/4 ')
                MTSF.TS._savefigTS(options,fig)
                logging.info(': Valiation Map : Drawing Step # 4/4 ')
                MTSF.TS._Image2JPEGTS(options)

        except Exception as ex:
            logging.info(': Modulo Maps Validation : Error 005 : Cannot Draw  ' + ex)
            logging.shutdown()
            sys.exit()

    def GridAspect(file,options, lonlatcellcenter,timeIndex):

        Validation(file,options, lonlatcellcenter,timeIndex)
        sorted_x = sorted(options.maps_validation_parameters,key=lambda x : x[1])
        
                # confirma se a grid e o numero de propriedades de valiçao pedidas esta correcto
        try: 
            if options.validation_grid[0]*options.validation_grid[1] is not len(sorted_x):
                logging.info(': Modulo Validation : Error 001 : Requested grid dimension (' + str(options.validation_grid[0]*options.validation_grid[1]) + ') is diferent than the requested number of validation Charts (' + str(len(sorted_x)) +')' )
                logging.shutdown()
                sys.exit()
        except Exception as ex:
            logging.info(': Modulo Maps Validation : Error 006 : Requested grid dimension (' + str(options.validation_grid[0]*options.validation_grid[1]) + ') is diferent than the requested number of validation Charts (' + str(sorted_x[-1][1]) +')' )

        options.titleOrigianal=options.title                    #guarda o titlo defenido pelo utilizador e usa pr dar nome geral a imagem
        options.sorted_x=sorted_x

        for x in range(len(sorted_x)):

            options.subplot_index=x
            options.title= sorted_x[x][5]
            ax = plt.subplot(str(options.validation_grid[0])+str(options.validation_grid[1])+str(int(options.maps_validation_parameters[options.subplot_index][1])))

            if 'TimeSeries' not in sorted_x[x][0]:
                ax.set_aspect(1.0)
                Validation.Maps(file,options, lonlatcellcenter,timeIndex)

            elif 'TimeSeries' in sorted_x[x][0]:
                options.subplot_index=x
                options.title='Time Evolution'
                plt.title(options.title)
                Validation.TimeSeries(file,options)

        #plt.show()
        #plt.tight_layout()

    def _hdf5valida (self):

        # corrige o Input_file e o Compara_file de modo a estarem de acordo com a lista de ficheiros dada.
        try:
            indices = [i for i, s in enumerate(self.hdf5valida_config) if 'HDF_IN' in s]
            for x in range(len(indices)):
                if x == 0:
                    self.hdf5valida_config[indices[x]] = ('HDF_IN   : ' + self.filePath + '\n')
                else:
                    self.hdf5valida_config[indices[x]] = ('HDF_IN   : ' + self.filePathB + '\n')
        except Exception as ex:
            logging.info(': Modulo Maps Validation : Error 007 : Falha a corrigir o nome dos ficheiros de entrada' +ex)
            logging.shutdown()
            sys.exit()  


            # Cria o Ficheiro para o hdf5 funcionar      
        try:
            f=open('Compare2HDFfiles.dat','w')
            for ele in self.hdf5valida_config:
                f.write(ele)
            f.close()
            logging.info(': Sucess : Ficheiro hdf5valida.dat.dat criado com sucesso')
        except:
            logging.info(': Modulo Maps Validation : Error 008 : Falha a criar o ficheiro hdf5valida.dat')
            logging.shutdown()
            sys.exit()  

            # Corre o TimeSerieAnalyser     
        try:
            #os.system(options.executable_exe)
            p = subprocess.Popen(self.executable_exe + '> Compare2HDFfiles_log.txt', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            for line in p.stdout.readlines():
                print (line),
            retval = p.wait()
            logging.info(': Sucess : O hdf5Valida analyser correu')
        except:
            logging.info(': Modulo Maps Validation : Error 009 : Falha a correr o Executavel' + options.executable_exe)
            logging.shutdown()
            sys.exit()  
        
        indice = [i for i, s in enumerate(self.hdf5valida_config) if 'HDF_OUT ' in s]
        name=str(self.hdf5valida_config[indice[0]])
        name=name.split()
        self.filePath = name[2]

        indice = [i for i, s in enumerate(self.hdf5valida_config) if 'TS_OUT ' in s]
        name=str(self.hdf5valida_config[indice[0]])
        name=name.split()
        self.files_list = name[2]

        return self