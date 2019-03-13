import logging

class MOHID:

    def __init__(self,filename,readoption,datacolumn):
        

        try:
            if readoption == 'TimeSeries':

                self.filename=filename
                self.Name=""
                self.Localization_i=0
                self.Localization_j=0
                self.Localization_k=0
                self.SerieInitialData = []
                self.TimeUnits=""
                self.ModelDomain=""
                self.Fields=[]
                self.Values=[]
                self.ValuesX=[]
                self.ValuesX_datenum=[]
                self.ValuesY=[]
                self.residualValues=[]
                self.datacolumn_to_read = datacolumn

                MOHID.__Timeseries(self)
                MOHID.__Properties(self)
               # MOHID.drawplot(self)


            if readoption == 'TimeSeriesValidation':

                self.stdev_obs=None
                self.average_obs=None
                self.bias=None
                self.rmse=None
                self.normalise_rmse=None
                self.unbias_rmse=None
                self.normalise_unbias_rmse=None
                self.rcorr=None
                self.nash_sutcliffe=None
                self.skill=None
                self.rcorr_quad=None
                self.z_fisher=None
                self.alfa=None
                self.beta_1=None
                self.am=None
                self.bm=None

                self.datacolumn_to_read = datacolumn

                MOHID.__Timeseries(self)
                MOHID.__Properties(self)
               # MOHID.drawplot(self)


            elif readoption == 'empty':
                self.Name=None

        except ValueError:
            logging.info(': Could not find the option')


    def __Timeseries(self):

        import re
        import logging

                
        fid = open(self.filename, 'r')

        for line in fid:

            auxString=line

            string=auxString.strip()

            stringSplit=re.split(':',string)

            if stringSplit[0].strip().lower() == 'NAME'.lower():

                self.Name=stringSplit[1].strip()

            elif stringSplit[0].strip().lower() == 'LOCALIZATION_I'.lower():

                self.Localization_i=int(stringSplit[1].strip())

            elif stringSplit[0].strip().lower() == 'LOCALIZATION_J'.lower():

                self.Localization_j=int(stringSplit[1].strip())

            elif stringSplit[0].strip().lower() == 'LOCALIZATION_K'.lower():

                self.Localization_k=int(stringSplit[1].strip())

            elif stringSplit[0].strip().lower() == 'SERIE_INITIAL_DATA'.lower():

                auxSerieInitialData=re.split(' +',stringSplit[1].strip())
                self.SerieInitialData = [int(float(i)) for i in auxSerieInitialData]
                
            elif stringSplit[0].strip().lower() == 'TIME_UNITS'.lower():

                self.TimeUnits=stringSplit[1].strip()

            elif stringSplit[0].strip().lower() == 'MODEL_DOMAIN'.lower():

                self.ModelDomain=stringSplit[1].strip()

            elif re.match('Seconds   YY  MM  DD  hh  mm       ss'.lower(),stringSplit[0].strip().lower()):

                auxFields=re.split(r' +',stringSplit[0].strip())
                self.Fields=[re.sub(r'_',r" ",i) for i in auxFields]
                #print (self.Fields)

            elif stringSplit[0].strip().lower() == '<BeginTimeSerie>'.lower():

                for line in fid:

                    auxString=line

                    string=auxString.strip()

                    if string.strip().lower() == '<EndTimeSerie>'.lower():

                        break

                    else :
                        
                        auxValues=re.split(' +',string.strip())
                        self.Values.append([float(i) for i in auxValues])
                        self.ValuesX=[item[0] for item in self.Values]
                        self.ValuesY=[item[self.datacolumn_to_read-1] for item in self.Values]

            elif stringSplit[0].strip().lower() == '<BeginResidual>'.lower():

                for line in fid:

                    auxString=line

                    string=auxString.strip()

                    if string.strip().lower() == '<EndResidual>'.lower():

                        break

                    else :
                        
                        auxResidualvalues=re.split(' +',string.strip())
                        self.residualValues.append([float(i) for i in auxResidualvalues])  
                        
            elif stringSplit[0].strip().lower() == 'STDEV_OBS'.lower():
                try:
                    self.stdev_obs=float (stringSplit[1].strip())
                    logging.info(': Sucess 001 : 1/16 STDEV_OBS lido ')
                except:
                   logging.info(': Error 001 : STDEV_OBS readed failed ')                                 


            elif stringSplit[0].strip().lower() == 'AVERAGE_OBS'.lower():
                try:
                    self.average_obs=float (stringSplit[1].strip())
                    logging.info(': Sucess 001 : 2/16 AVERAGE_OBS lido ')
                except:
                   logging.info(': Error 001 : AVERAGE_OBS readed failed ')                                 


            elif stringSplit[0].strip().lower() == 'BIAS'.lower():
                try:
                    self.bias=float (stringSplit[1].strip())
                    logging.info(': Sucess 001 : 3/16 BIAS lido ')
                except:
                   logging.info(': Error 001 : BIAS readed failed ')                                 


            elif stringSplit[0].strip().lower() == 'RMSE'.lower():
                try:
                    self.rmse=float (stringSplit[1].strip())
                    logging.info(': Sucess 001 : 4/16 RMSE lido ')
                except:
                   logging.info(': Error 001 : RMSE readed failed ')                                 


            elif stringSplit[0].strip().lower() == 'Normalise RMSE [%]'.lower():
                try:
                    self.normalise_rmse=float (stringSplit[1].strip())
                    logging.info(': Sucess 001 : 5/16 Normalise RMSE [%] lido ')
                except:
                   logging.info(': Error 001 : Normalise RMSE [%] readed failed ')      
      


            elif stringSplit[0].strip().lower() == 'Unbias RMSE'.lower():
                try:
                    self.unbias_rmse=float (stringSplit[1].strip())
                    logging.info(': Sucess 001 : 6/16 Unbias RMSE lido ')
                except:
                   logging.info(': Error 001 : Unbias RMSE readed failed ')           

            elif stringSplit[0].strip().lower() == 'Normalise unbias RMSE[%]'.lower():
                try:
                    self.normalise_unbias_rmse=float (stringSplit[1].strip())
                    logging.info(': Sucess 001 : 7/16 Normalise unbias RMSE[%] lido ')
                except:
                   logging.info(': Error 001 : Normalise unbias RMSE[%] readed failed ')           

            elif stringSplit[0].strip().lower() == 'rcorr'.lower():
                try:
                    self.rcorr=float (stringSplit[1].strip())
                    logging.info(': Sucess 001 : 8/16 rcorr lido ')
                except:
                   logging.info(': Error 001 : rcorr readed failed ')           

            elif stringSplit[0].strip().lower() == 'NASH–SUTCLIFFE'.lower():
                try:
                    self.nash_sutcliffe=float (stringSplit[1].strip())
                    logging.info(': Sucess 001 : 9/16 NASH–SUTCLIFFE lido ')
                except:
                   logging.info(': Error 001 : NASH–SUTCLIFFE readed failed ')           

            elif stringSplit[0].strip().lower() == 'SKILL'.lower():
                try:
                    self.skill=float (stringSplit[1].strip())
                    logging.info(': Sucess 001 : 10/16 SKILL lido ')
                except:
                   logging.info(': Error 001 : SKILL readed failed ')           

            elif stringSplit[0].strip().lower() == 'rcorr_quad'.lower():
                try:
                    self.rcorr_quad=float (stringSplit[1].strip())
                    logging.info(': Sucess 001 : 11/16 rcorr_quad lido ')
                except:
                   logging.info(': Error 001 : rcorr_quad readed failed ')           

            elif stringSplit[0].strip().lower() == 'z_fisher'.lower():
                try:
                    self.z_fisher=float (stringSplit[1].strip())
                    logging.info(': Sucess 001 : 12/16 z_fisher lido ')
                except:
                   logging.info(': Error 001 : z_fisher readed failed ')           

            elif stringSplit[0].strip().lower() == 'alfa'.lower():
                try:
                    self.alfa=float (stringSplit[1].strip())
                    logging.info(': Sucess 001 : 13/16 alfa lido ')
                except:
                   logging.info(': Error 001 : alfa readed failed ')           

            elif stringSplit[0].strip().lower() == 'beta_1'.lower():
                try:
                    self.beta_1=float (stringSplit[1].strip())
                    logging.info(': Sucess 001 : 14/16 beta_1 lido ')
                except:
                   logging.info(': Error 001 : beta_1 readed failed ')           

            elif stringSplit[0].strip().lower() == 'Am'.lower():
                try:
                    self.am=float (stringSplit[1].strip())
                    logging.info(': Sucess 001 : 15/16 Am lido ')
                except:
                   logging.info(': Error 001 : Am readed failed ')           

            elif stringSplit[0].strip().lower() == 'Bm'.lower():
                try:
                    self.bm=float (stringSplit[1].strip())
                    logging.info(': Sucess 001 : 16/16 Bm lido ')
                except:
                   logging.info(': Error 001 : Bm readed failed ')        



        fid.close()

    def __Properties(self):
        import logging
        import numpy as np
        import datetime

        try:
            if self.TimeUnits == 'SECONDS':
                for x in range(0,len(self.ValuesX)):
                    self.ValuesX_datenum.append(datetime.timedelta(seconds=self.ValuesX[x]) + datetime.datetime(self.SerieInitialData[0], self.SerieInitialData[1], self.SerieInitialData[2],self.SerieInitialData[3], self.SerieInitialData[4], self.SerieInitialData[5]))

            elif self.TimeUnits == 'MINUTES':
                for x in range(0,len(self.ValuesX)):
                    self.ValuesX_datenum.append(datetime.timedelta(minutes=self.ValuesX[x]) + datetime.datetime(self.SerieInitialData[0], self.SerieInitialData[1], self.SerieInitialData[2],self.SerieInitialData[3], self.SerieInitialData[4], self.SerieInitialData[5]))

            elif self.TimeUnits == 'HOURS':
                for x in range(0,len(self.ValuesX)):
                    self.ValuesX_datenum.append(datetime.timedelta(hours=self.ValuesX[x]) + datetime.datetime(self.SerieInitialData[0], self.SerieInitialData[1], self.SerieInitialData[2],self.SerieInitialData[3], self.SerieInitialData[4], self.SerieInitialData[5]))

        except Exception as ex:
            logging.info(': Error 008 : Cannot find TimeUnit ' + self.TimeUnits)
            logging.shutdown()
            sys.exit()    


    def readTimeseries(filename,datacolumn):

        if datacolumn == 'empty':
            timeseries = MOHID(filename, "empty",datacolumn)
        else:
           timeseries = MOHID(filename, "TimeSeries",datacolumn)
            
        return timeseries
