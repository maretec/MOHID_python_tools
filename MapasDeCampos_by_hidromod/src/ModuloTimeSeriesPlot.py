import os
from subprocess import call
from subprocess import PIPE, Popen
import logging
import ModuloTimeSerieReader as MTSR
import ModuloMapsDraw as MMD
import ModuloTimeSeriesDraw as MTSD
import time


class ModuloTimeSeriesPlot(object):

    def __init__(self,options):

        if options.plot_type == 1:
            logging.info(': Plot Type 1')
            logging.info(': plot type 1 not set')

        elif options.plot_type == 2:
            logging.info(': Plot Type 2')

            Timeseries=['','','','','','','','','','','','','','','','','','','','','']
            try:
                for x in range(0,len(options.files_list)):
                    Timeseries[x] = MTSR.MOHID.readTimeseries(options.files_list[x],int(options.files_list_column[x]))  
                    logging.info(': Série ' + (options.files_list[x]) +'/coluna ' + str(int(options.files_list_column[x])) + ' lida com sucesso')                    
            except Exception as ex:
                logging.info(': Modulo TimeSeries Plot : Error 001 : Failed to load Timeseries ' + ex)
                logging.shutdown()
                sys.exit()  

            logging.info(': Começar a Desenhar')
            MTSD.Draw_timeseries.__init__(options.plot_type,Timeseries,options)

        elif options.plot_type == 3:
            logging.info(': plot type 3 not set')

        elif options.plot_type == 4:
            logging.info(': plot type 4 not set')

        elif options.plot_type == 5:
            logging.info(': Plot Type 5 - TimeSerie Validation')

            # corrige o Input_file e o Compara_file de modo a estarem de acordo com a lista de ficheiros dada.
            try:
                indices = [i for i, s in enumerate(options.timeserieanalyser_config) if 'INPUT_FILE' in s]
                options.timeserieanalyser_config[indices[0]] = ('INPUT_FILE   : ' + options.files_list[0] + '\n')

                indices = [i for i, s in enumerate(options.timeserieanalyser_config) if 'COMPARE_FILE' in s]
                options.timeserieanalyser_config[indices[0]] = ('COMPARE_FILE   : ' + options.files_list[1] + '\n')
            except:
                logging.info(': Falha a corrigir o nome dos ficheiros de entrada')
                logging.shutdown()
                sys.exit()  

            # corrige o Input_file e o Compara_file de modo as colun as estarem de acordo com AS.
            try:
                indices = [i for i, s in enumerate(options.timeserieanalyser_config) if 'DATA_COLUMN' in s]
                options.timeserieanalyser_config[indices[0]] = ('DATA_COLUMN   : ' + str(options.files_list_column[0]) + '\n')

                indices = [i for i, s in enumerate(options.timeserieanalyser_config) if 'COMPARE_COLUMN' in s]
                options.timeserieanalyser_config[indices[0]] = ('COMPARE_COLUMN   : ' + str(options.files_list_column[1]) + '\n')
            except:
                logging.info(': Falha a corrigir a coluna de dados dos ficheiros de entrada')
                logging.shutdown()
                sys.exit()  

             # imprime no log o ficheiro de configuração
            try:
                logging.info(': TimeSerie Analyser configurations used')

                for i in options.timeserieanalyser_config:
                    try:
                        logging.info( i)
                    except:
                        logging.info('problemass' + i)
            except:
                logging.info(': Falha a dar a lista de configurações do TimeSerie Analyser' + i)
                logging.shutdown()
                sys.exit()  
             # Cria o Ficheiro para o Timeserieanalyser funcionar      
            try:
                f=open('TimeSeriesAnalyser.dat','w')
                for ele in options.timeserieanalyser_config:
                    f.write(ele)
                f.close()
                logging.info(': Sucess : Ficheiro TimeSeriesAnalyser.dat criado com sucesso')
            except:
                logging.info(': Error 000 : Falha a criar o ficheiro TimeSerieAnalyser.dat')
                logging.shutdown()
                sys.exit()  

             # Corre o TimeSerieAnalyser     
            try:
                #os.system(options.executable_exe)
                x=0
                while 'CompareOut_'+ options.files_list[0].split('\\')[-1] not in os.listdir() and x<= 5:
                    p = Popen(options.executable_exe + '> TimeSerieAnalyser_log.txt', stdin=PIPE, stdout=PIPE, bufsize=1, shell=True)
                    out, err = p.communicate()
                    x+=1
                logging.info(': Sucess : O timeSerie analyser correu')

                time.sleep(10)

            except:
                logging.info(': Error 000 : Falha a correr o Executavel' + options.executable_exe)
                logging.shutdown()
                sys.exit()   

             # Lê as séries do CompareOut_MOHID.srh 
            try:
                Timeseries=MTSR.MOHID.readTimeseries(options.files_list[0],'empty')
                # o nome e sempre em funcao da primeira serie que enrta no timeserie, deve ser a primeira da lista do begin_files_list
                Timeseries.Serie1=MTSR.MOHID.readTimeseries(('CompareOut_' + options.files_list[0]),2)  
                logging.info(': Série observada (Coluna 2) lida com sucesso')
                Timeseries.Serie2=MTSR.MOHID.readTimeseries(('CompareOut_' + options.files_list[0]),3)                 
                logging.info(': Série modelada (Coluna 3) lida com sucesso')
                logging.info(': SUCESSO : Ficheiro de validaçao lido com sucesso (CompareOut_' + options.files_list[0])
            except:
                logging.info(': Error 000 : Falha a ler o ficheiro com validação (CompareOut_' + options.files_list[0])
                logging.shutdown()
                sys.exit()  
              
            try:
                logging.info(': Começar a Desenhar')
                MTSD.Draw_timeseries.__init__(options.plot_type,Timeseries,options)
                logging.info(': SUCESSO : Plot produzido com sucesso')
            except:
                logging.info(': Error 000 : Falha a desenhar')
                logging.shutdown()
                sys.exit()  

    def TimeSeries(options):
        
        ModuloTimeSeriesPlot(options)

