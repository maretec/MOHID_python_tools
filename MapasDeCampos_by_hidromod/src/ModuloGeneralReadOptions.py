import logging

class readOptions(object):

    # The class "constructor" - It's actually an initializer 
    def __init__(self, filename):

        #Gerais
        self.plot_image_type   = 'maps'
        self.plot_type         = 1
        self.title             = ''
        self.CompressImage     = None
        self.Xmin              = None
        self.Ymin              = None
        self.Xmax              = None
        self.Ymax              = None
        self.fontsize          = 6
        self.logopath          = None
        self.dpi               = 200
        self.figureOutName      = None
        self.AQUASAFE          = 0



        
        #MAPS
        self.filePath       = None
        self.filePathB       = None
        self.scalar         = None
        self.scalarMax      = None
        self.scalarMin      = None
        self.layerDepth     = 'surface'
        self.vectorX        = None
        self.vectorY        = None
        self.stream         = 0
        self.streamX        = None
        self.streamY        = None
        self.stream_arrow_factor         = 5
        self.stream_color   = None
        self.stream_density = 0.5
        self.stream_linewidth= 1.5
        self.vectorStep     = 1
        self.vectorSize     = None
        self.vectorWidth    = 0.002
        self.legend         = None
        self.gssh           = 0
        self.worldImage     = 0
        self.worldImage_esri= 'World_Imagery'
        self.colorbar       = 1
        self.colormap       = 'jet'
        self.colorbarSpacing= 1
        self.timeZone       = 'UTC'
        self.dt             = 1
        self.filename       = filename
        self.fillValue      = None
        self.fillContinents = 0
        self.fillContinents_color = 'w'
        self.window         = None
        self.dx             = None
        self.dy             = None
        self.resolution     = 'i'
        self.coastline      = 0
        self.X              = 0        
        self.Y              = 0
        self.points         = 0
        self.label          = 1
        self.orientationcolorbar = 'vertical'
        self.logoPath       = None
        self.decimalcolorbar = None
        self.drawBathymetry  = 0
        self.extend          = None
        self.figuretransparent = 0
        self.constantvector   = 0
        self.vectorcolor      = 'k'
        self.figurecolor      = 'w'
        self.xpixel           = None
        self.ypixel           = None
        self.figurequality    = 100
        self.quiverunits      = 'width'
        self.justvector       = 0
        self.polygon          = 0
        self.polygonfill      = 0
        self.polygoncolor     = 'k'
        self.pcolor           = 0
        self.LogMap           = 0
        self.conversionfactor = None
        self.colorpoints      = 'r'
        self.fontsizepoints   = 15
        self.dynamic_limits   = 0

        self.hdf5valida_config     = []
        self.maps_validation_parameters         = []
        self.timeseries_validation_parameters   = []
        self.run_valida   = 1
        self.Xinches   = None
        self.Yinches   = None

        self.validation_grid         = [1,1]
        self.validation_grid_ws      = 0.3
        self.validation_grid_hs      = 0.1

        self.plot_bias         = 0
        self.plot_rmse         = 0
        self.plot_rcorr         = 0

        #TimeSeries
        self.linewidth             = 1
        self.xlabel                = None
        self.ylabel                = None
        self.parameter             = ''
        self.Ymax                  = None
        self.Ymin                  = None
        self.files_list            = []
        self.files_list_column     = []
        self.files_list_name       = []
        self.files_list_type       = []
        self.files_list_color      = []
        self.offset                       = []
        self.timeserieanalyser_config     = []
        self.executable_exe               = None
        self.stdev_obs               =None
        self.average_obs               =None
        self.bias               =None
        self.rmse               =None
        self.normalise_rmse               =None
        self.unbias_rmse               =None
        self.normalise_unbias_rmse               =None
        self.rcorr               =None
        self.nash_sutcliffe               =None
        self.skill               =None
        self.rcorr_quad               =None
        self.z_fisher               =None
        self.alfa               =None
        self.beta_1               =None
        self.am               =None
        self.bm               =None


        self.basemap_config   = None


        readOptions.__scanOptions(self)

    def __scanOptions(self):

        import re
        import os
        import logging
        import sys
        
        try:
            
            fid = open(self.filename, 'r',encoding='utf-8')

        except IOError:
            logging.info(': Modulo General Read Options : Error 001 : Cannot open ' + self.filename)


        try:
            for line in fid:

                auxString=line

                string=auxString.strip()

                stringSplit=re.split(':',string,1)

                if stringSplit[0].strip().lower() == 'PLOT_IMAGE_TYPE'.lower():
                    string=stringSplit[1].strip()
                    mylist=string.split(' ')
                    self.plot_image_type=(mylist[0])
                    
                elif stringSplit[0].strip().lower() == 'PLOT_TYPE'.lower():
                    string=stringSplit[1].strip()
                    mylist=string.split('#')
                    self.plot_type= int(mylist[0])


                elif stringSplit[0].strip().lower() == 'FIGURE_OUT_NAME'.lower():
                    self.figureOutName=stringSplit[1].strip()
                    if not self.figureOutName:
                         raise ValueError('Empty String!')

                elif stringSplit[0].strip().lower() == 'DPI'.lower():
                    self.dpi=int (stringSplit[1].strip())

                elif stringSplit[0].strip().lower() == 'LOGO_PATH'.lower():
                    self.logoPath=stringSplit[1].strip()
                    if not self.logoPath:
                         raise ValueError('Empty String!')

                elif stringSplit[0].strip().lower() == 'FONTSIZE'.lower():
                    self.fontsize= float(stringSplit[1].strip())  

                elif stringSplit[0].strip().lower() == 'COMPRESSIMAGE'.lower():
                    self.CompressImage=int (stringSplit[1].strip())

                elif stringSplit[0].strip().lower() == 'TITLE'.lower():
                    self.title=stringSplit[1].strip()
                    if not self.title:
                         raise ValueError('Empty String!')

                elif stringSplit[0].strip().lower() == 'FILE_PATH'.lower():
                    self.filePath=stringSplit[1].split(',')
                    if not self.filePath:
                            raise ValueError('Empty String!')              
                    #if self.plot_image_type == 'maps' and self.plot_type == 2:
                    #    self.filePathB=self.filePath[1].strip()
                    #    self.filePath=self.filePath[0].strip()
                    #else:
                    self.filePath=self.filePath[0].strip()

                elif stringSplit[0].strip().lower() == 'AQUASAFE'.lower():
                    self.AQUASAFE=int (stringSplit[1].strip())
                    
                elif stringSplit[0].strip().lower() == 'SCALAR'.lower():
                    self.scalar=stringSplit[1].strip()
                    if not self.scalar:
                            raise ValueError('Empty String!')
                
                elif stringSplit[0].strip().lower() == 'SCALAR_MAX'.lower():
                    self.scalarMax= float(stringSplit[1].strip())
                
                elif stringSplit[0].strip().lower() == 'SCALAR_MIN'.lower():
                    self.scalarMin= float(stringSplit[1].strip())                

                    
                elif stringSplit[0].strip().lower() == 'VECTOR_X'.lower():
                    self.vectorX=stringSplit[1].strip()
                    if not self.vectorX:
                            raise ValueError('Empty String!')
                
                elif stringSplit[0].strip().lower() == 'VECTOR_Y'.lower():
                    self.vectorY=stringSplit[1].strip()
                    if not self.vectorY:
                            raise ValueError('Empty String!')

                elif stringSplit[0].strip().lower() == 'STREAMPLOT'.lower():
                    self.stream=int (stringSplit[1].strip())
                    if not self.stream:
                            raise ValueError('Empty String!')   

                elif stringSplit[0].strip().lower() == 'STREAMPLOT_DENSITY'.lower():
                    self.stream_density=float (stringSplit[1].strip())
                    #if self.stream_density > 4:
                    #        raise ValueError('Reduce Stream Density, values must be bellow or equal to 4!')   # se for maior ele gera matriz de 30*densidade

                elif stringSplit[0].strip().lower() == 'STREAMPLOT_LINEWIDTH'.lower():
                    self.stream_linewidth=float (stringSplit[1].strip())

                elif stringSplit[0].strip().lower() == 'STREAMPLOT_ARROW_FACTOR'.lower():
                    self.stream_arrow_factor=float (stringSplit[1].strip())
                        
                elif stringSplit[0].strip().lower() == 'STREAMPLOT_X'.lower():
                    self.streamX=stringSplit[1].strip()
                    if not self.streamX:
                            raise ValueError('Empty String!')
                
                elif stringSplit[0].strip().lower() == 'STREAMPLOT_Y'.lower():
                    self.streamY=stringSplit[1].strip()
                    if not self.streamY:
                            raise ValueError('Empty String!')

                elif stringSplit[0].strip().lower() == 'STREAMPLOT_COLOR'.lower():
                    self.stream_color = stringSplit[1].strip()
                    if self.stream_color.startswith("["):
                        aux = tuple(self.stream_color[1:int(len(self.stream_color))-1].split(','))
                        self.stream_color=float(aux[0]),float(aux[1]),float(aux[2])

                elif stringSplit[0].strip().lower() == 'VECTOR_STEP'.lower():
                    self.vectorStep=int (stringSplit[1].strip())
                
                elif stringSplit[0].strip().lower() == 'VECTOR_SIZE'.lower():
                    self.vectorSize=int (stringSplit[1].strip())
                
                elif stringSplit[0].strip().lower() == 'VECTOR_WIDTH'.lower():
                    self.vectorWidth=float (stringSplit[1].strip())               
                                    
                elif stringSplit[0].strip().lower() == 'LEGEND'.lower():
                    self.legend=stringSplit[1].strip()
                    if not self.legend:
                            raise ValueError('Empty String!')                
                                     
                elif stringSplit[0].strip().lower() == 'GSSH'.lower():
                    self.gssh=int (stringSplit[1].strip())
                
                elif stringSplit[0].strip().lower() == 'WORLD_IMAGE'.lower():
                    self.worldImage=int (stringSplit[1].strip())

                elif stringSplit[0].strip().lower() == 'WORLD_IMAGE_ESRI'.lower():
                    self.worldImage_esri=stringSplit[1].strip().split()[0]
                    if not self.worldImage_esri:
                            raise ValueError('Empty String!')
                         
                elif stringSplit[0].strip().lower() == 'COLORBAR'.lower():
                    self.colorbar=int (stringSplit[1].strip())

                elif stringSplit[0].strip().lower() == 'DYNAMIC_LIMITS'.lower():
                    self.dynamic_limits=int (stringSplit[1].strip())

                elif stringSplit[0].strip().lower() == 'COLORMAP'.lower():
                    stringcolormap = stringSplit[1].strip()
                    if stringcolormap.startswith("["):                      
                        auxColormap = stringcolormap[1:int(len(stringcolormap))-1].split(';')
                        self.colormap= [None]*(len(auxColormap));
                        i=0
                        for x in auxColormap:
                            temp=x.split(',')
                            self.colormap[i] = [float(temp[0]),float(temp[1]),float(temp[2])]
                            i=i+1
                    else:
                        self.colormap = stringSplit[1].strip()
                
                elif stringSplit[0].strip().lower() == 'TIMEZONE'.lower():
                    self.timeZone=stringSplit[1].strip()
                    if not self.timeZone:
                            raise ValueError('Empty String!')
                                
                elif stringSplit[0].strip().lower() == 'DT'.lower():
                    self.dt=int (stringSplit[1].strip())

                elif stringSplit[0].strip().lower() == 'XINCHES'.lower():
                    self.Xinches=float (stringSplit[1].strip())

                elif stringSplit[0].strip().lower() == 'YINCHES'.lower():
                    self.Yinches=float (stringSplit[1].strip())
                    
                elif stringSplit[0].strip().lower() == 'LAYER_DEPTH'.lower():
                    if not stringSplit[1].strip():
                            raise ValueError('Empty String!')
                    elif stringSplit[1].strip().lower() == 'SURFACE'.lower():
                        self.layerDepth=stringSplit[1].strip().lower()
                    else:
                        self.layerDepth=int (stringSplit[1].strip())

                elif stringSplit[0].strip().lower() == 'FILL_VALUE'.lower():
                    auxFields=re.split(r' +',stringSplit[1].strip())
                    self.fillValue=[float(i) for i in auxFields]

                elif stringSplit[0].strip().lower() == 'COLORBAR_SPACING'.lower():
                    self.colorbarSpacing=float (stringSplit[1].strip())

                elif stringSplit[0].strip().lower() == 'FILL_CONTINENTS'.lower():
                    self.fillContinents=int (stringSplit[1].strip())

                elif stringSplit[0].strip().lower() == 'RUN_VALIDA'.lower():
                    self.run_valida=int (stringSplit[1].strip())

                elif stringSplit[0].strip().lower() == 'DX'.lower():
                    self.dx=float (stringSplit[1].strip())

                elif stringSplit[0].strip().lower() == 'DY'.lower():
                    self.dy=float (stringSplit[1].strip())

                elif stringSplit[0].strip().lower() == 'GSSH_RESOLUTION'.lower():
                    self.resolution=stringSplit[1].strip()

                elif stringSplit[0].strip().lower() == 'WINDOW'.lower():
                    stringSplit=re.split(':',string,1)
                    self.Xmin=float (re.split(' ',stringSplit[1].strip(),0)[0])
                    self.Ymin=float (re.split(' ',stringSplit[1].strip(),0)[1])
                    self.Xmax=float (re.split(' ',stringSplit[1].strip(),0)[2])
                    self.Ymax=float (re.split(' ',stringSplit[1].strip(),0)[3])
                    
                elif stringSplit[0].strip().lower() == 'COASTLINE'.lower():
                    coastlineFile=stringSplit[1].strip()
                    if not coastlineFile:
                            raise ValueError('Coastline Empty String!')                    
                    try:
                        self.coastline      = 1
                        fid = open(coastlineFile, 'r',encoding='utf-8')
                        self.X,self.Y = [], []
                        for line in fid:
                            self.X.append(float (re.split(' ',line.strip(),0)[0]))
                            self.Y.append(float (re.split(' ',line.strip(),0)[1]))
                    except ValueError as ex:
                        fid.close()
                        logging.info(': Modulo General Read Options : Error 002 : No Coastline Path ' + stringSplit[0].strip().lower()) 
                        logging.shutdown()
                        sys.exit()
                        
                elif stringSplit[0].strip().lower() == 'POINTS'.lower():
                    pointsFile=stringSplit[1].strip()
                    if not pointsFile:
                            raise ValueError('Points Empty String!')                    
                    try:
                        self.points      = 1
                        fid = open(pointsFile, 'r',encoding='utf-8')

                        self.NamePoints,self.XPoints,self.YPoints = [], [], []
                        for line in fid:
                            self.NamePoints.append(re.split(' ',line.strip(),0)[0])
                            self.XPoints.append(float (re.split(' ',line.strip(),0)[1]))
                            self.YPoints.append(float (re.split(' ',line.strip(),0)[2]))
                    except ValueError as ex:
                        fid.close()
                        logging.info(': Modulo General Read Options : Error 003 : No Points Path ' + stringSplit[0].strip().lower()) 
                        logging.shutdown()
                        sys.exit()

                elif stringSplit[0].strip().lower() == 'LABEL'.lower():
                    self.label=int (stringSplit[1].strip())

                elif stringSplit[0].strip().lower() == 'ORIENTATIONCOLORBAR'.lower():
                    self.orientationcolorbar=stringSplit[1].strip()
                    if not self.orientationcolorbar:
                            raise ValueError('Empty String!')
                
                elif stringSplit[0].strip().lower() == 'JUST_VECTOR'.lower():
                    self.justvector= int(stringSplit[1].strip())    

                elif stringSplit[0].strip().lower() == 'DECIMALCOLORBAR'.lower():
                    self.decimalcolorbar=int (stringSplit[1].strip())

                elif stringSplit[0].strip().lower() == 'DRAW_BATHYMETRY'.lower():
                    self.drawBathymetry=int (stringSplit[1].strip())

                elif stringSplit[0].strip().lower() == 'EXTEND'.lower():
                    self.extend =stringSplit[1].strip()

                elif stringSplit[0].strip().lower() == 'FIGURE_TRANSPARENT'.lower():
                    self.figuretransparent =int (stringSplit[1].strip())

                elif stringSplit[0].strip().lower() == 'CONSTANT_VECTOR'.lower():
                    self.constantvector =int (stringSplit[1].strip())

                elif stringSplit[0].strip().lower() == 'VECTOR_COLOR'.lower():
                    self.vectorcolor = stringSplit[1].strip()
                    if self.vectorcolor.startswith("["):
                        aux = tuple(self.vectorcolor[1:int(len(self.vectorcolor))-1].split(','))
                        self.vectorcolor=float(aux[0]),float(aux[1]),float(aux[2])

                elif stringSplit[0].strip().lower() == 'FIGURE_COLOR'.lower():
                    self.figurecolor = stringSplit[1].strip()
                    if self.figurecolor.startswith("["):
                        aux = tuple(self.figurecolor[1:int(len(self.figurecolor))-1].split(','))
                        self.figurecolor=float(aux[0]),float(aux[1]),float(aux[2])

                elif stringSplit[0].strip().lower() == 'FILL_CONTINENTE_COLOR'.lower():
                    self.fillContinents_color = stringSplit[1].strip()
                    if self.fillContinents_color.startswith("["):
                        aux = tuple(self.fillContinents_color[1:int(len(self.fillContinents_color))-1].split(','))
                        self.fillContinents_color=float(aux[0]),float(aux[1]),float(aux[2])
                        
                elif stringSplit[0].strip().lower() == 'X_PIXEL'.lower():
                    self.xpixel =int (stringSplit[1].strip())
                    
                elif stringSplit[0].strip().lower() == 'Y_PIXEL'.lower():
                    self.ypixel =int (stringSplit[1].strip())
    
                elif stringSplit[0].strip().lower() == 'FIGURE_QUALITY'.lower():
                    self.figurequality =int (stringSplit[1].strip())

                elif stringSplit[0].strip().lower() == 'QUIVER_UNITS'.lower():
                    self.quiverunits = (stringSplit[1].strip())
                                            
                elif stringSplit[0].strip().lower() == 'POLYGON_FILE'.lower():
                    polygonFile=stringSplit[1].strip()
                    if not polygonFile:
                            raise ValueError('Polygon file Empty String!')                    
                    try:
                        self.polygon      = 1
                        fid = open(polygonFile, 'r',encoding='utf-8')
                        self.polyX,self.polyY = [], []
                        for line in fid:
                            self.polyX.append(float (re.split(' ',line.strip(),0)[0]))
                            self.polyY.append(float (re.split(' ',line.strip(),0)[1]))
                    except ValueError as ex:
                        fid.close()
                        logging.info(': Modulo General Read Options : Error 004 : No polygon file Path ' + stringSplit[0].strip().lower()) 
                        logging.shutdown()
                        sys.exit()

                elif stringSplit[0].strip().lower() == 'POLYGON_COLOR'.lower():
                    self.polygoncolor = stringSplit[1].strip()
                    if self.polygoncolor.startswith("["):
                        aux = tuple(self.polygoncolor[1:int(len(self.polygoncolor))-1].split(','))
                        self.polygoncolor=float(aux[0]),float(aux[1]),float(aux[2])

                elif stringSplit[0].strip().lower() == 'POLYGON_FILL'.lower():
                    self.polygonfill=int (stringSplit[1].strip())

                elif stringSplit[0].strip().lower() == 'PCOLOR'.lower():
                    self.pcolor =int (stringSplit[1].strip())


                elif stringSplit[0].strip().lower() == 'LOG_MAP'.lower():
                    self.LogMap =int (stringSplit[1].strip())

                elif stringSplit[0].strip().lower() == 'LOG_MAP_LEVELS'.lower():
                    AuxLogMapLevels   = stringSplit[1].strip().split(',')          
                    self.LogMapLevels = [float(i) for i in AuxLogMapLevels]
                    
                elif stringSplit[0].strip().lower() == 'CONVERSION_FACTOR'.lower():
                    self.conversionfactor =float(stringSplit[1].strip())

                elif stringSplit[0].strip().lower() == 'POINTS_COLOR'.lower():
                    self.pointscolor = stringSplit[1].strip()
                    if self.pointscolor.startswith("["):
                        aux = tuple(self.pointscolor[1:int(len(self.pointscolor))-1].split(','))
                        self.pointscolor=float(aux[0]),float(aux[1]),float(aux[2])

                elif stringSplit[0].strip().lower() == 'FONTSIZE_POINTS'.lower():
                    self.fontsizepoints= float(stringSplit[1].strip())

                elif stringSplit[0].strip().lower() == '<BEGIN_VALIDATION_PARAMETERS_MAPS>'.lower():
                    try:                        
                        for line in fid:
                            auxString=line
                            mylist=auxString.split(',')
                            if line.strip().lower() == '<END_VALIDATION_PARAMETERS_MAPS>'.lower():
                                break
                            else :
                                if int(mylist[1]) == 0:
                                    continue
                                else:
                                    self.maps_validation_parameters.append(mylist)
                    except:
                        logging.info(': Modulo General Read Options : Error 006 : failed to read validation maps request')

                elif stringSplit[0].strip().lower() == '<BEGIN_VALIDATION_PARAMETERS_TS>'.lower():
                    try:                        
                        for line in fid:
                            auxString=line
                            mylist=auxString.split(',')
                            if line.strip().lower() == '<END_VALIDATION_PARAMETERS_TS>'.lower():
                                break
                            else :
                                if int(mylist[1]) == 0:
                                    continue
                                else:
                                    self.timeseries_validation_parameters.append(mylist)
                    except:
                        logging.info(': Modulo General Read Options : Error 007 : failed to read validation maps request')

                elif stringSplit[0].strip().lower() == 'VALIDATION_GRID'.lower():
                    string=stringSplit[1].strip()
                    mylist=string.split(',')
                    _A= mylist[0]
                    _B= mylist[1]
                    self.validation_grid= [int(_A),int(_B)]

                elif stringSplit[0].strip().lower() == 'PLOT_BIAS'.lower():
                    try:
                        string=stringSplit[1].strip()
                        mylist=string.split(',')
                        self.plot_bias = mylist
                        #self.plot_bias.ymin = int(mylist[1])
                        #self.plot_bias.ymax = int(mylist[2])
                        #self.plot_bias.eixo = int(mylist[3])
                        #self.plot_bias.title = mylist[4]                        
                    except ValueError as ex:
                        logging.info(': Modulo General Read Options : Error 008 : failed to process ' + stringSplit[0].strip().lower()) 
                        logging.shutdown()
                        sys.exit()

                elif stringSplit[0].strip().lower() == 'PLOT_RMSE'.lower():
                    try:
                        string=stringSplit[1].strip()
                        mylist=string.split(',')
                        self.plot_rmse = mylist
                        #self.plot_bias.ymin = int(mylist[1])
                        #self.plot_bias.ymax = int(mylist[2])
                        #self.plot_bias.eixo = int(mylist[3])
                        #self.plot_bias.title = mylist[4]                        
                    except ValueError as ex:
                        logging.info(': Modulo General Read Options : Error 009 : failed to process ' + stringSplit[0].strip().lower()) 
                        logging.shutdown()
                        sys.exit()

                elif stringSplit[0].strip().lower() == 'PLOT_RCORR'.lower():
                    try:
                        string=stringSplit[1].strip()
                        mylist=string.split(',')
                        self.plot_rcorr = mylist
                        #self.plot_bias.ymin = int(mylist[1])
                        #self.plot_bias.ymax = int(mylist[2])
                        #self.plot_bias.eixo = int(mylist[3])
                        #self.plot_bias.title = mylist[4]                        
                    except ValueError as ex:
                        logging.info(': Modulo General Read Options : Error 010 : failed to process ' + stringSplit[0].strip().lower()) 
                        logging.shutdown()
                        sys.exit()

                elif stringSplit[0].strip().lower() == 'LINEWIDTH'.lower():
                    self.linewidth=stringSplit[1].strip()
                    if not self.linewidth:
                            raise ValueError('Empty String!')

                elif stringSplit[0].strip().lower() == 'PARAMETER'.lower():
                    self.parameter=stringSplit[1].strip()
                    if not self.parameter:
                            raise ValueError('Empty String!')

                elif stringSplit[0].strip().lower() == 'XLABEL'.lower():
                    self.xlabel=stringSplit[1].strip()
                    if not self.xlabel:
                            raise ValueError('Empty String!')

                elif stringSplit[0].strip().lower() == 'YLABEL'.lower():
                    self.ylabel=stringSplit[1].strip()
                    if not self.ylabel:
                            raise ValueError('Empty String!')

                elif stringSplit[0].strip().lower() == 'FIGURE_COLOR'.lower():
                    try:
                        self.figurecolor = stringSplit[1].strip()
                        if self.figurecolor.startswith("["):
                            aux = tuple(self.figurecolor[1:int(len(self.figurecolor))-1].split(','))
                            self.figurecolor=float(aux[0]),float(aux[1]),float(aux[2])
                        logging.info(': Sucess 001 : Figure Color readed ')
                    except:
                        logging.info(': Modulo General Read Options : Error 011 : Figure color readed failed ')
                        
                elif stringSplit[0].strip().lower() == 'YMAX'.lower():
                    try:
                        self.Ymax=float (stringSplit[1].strip())
                        logging.info(': Sucess 001 : Ymax readed ')
                    except:
                        logging.info(': Modulo General Read Options : Error 012 : Ymax readed failed ')

                elif stringSplit[0].strip().lower() == 'YMIN'.lower():
                    try:
                        self.Ymin=float (stringSplit[1].strip())
                        logging.info(': Sucess 001 : Ymin readed ')
                    except:
                        logging.info(': Modulo General Read Options : Error 013 : Ymin readed failed ')
                   
                elif stringSplit[0].strip().lower() == 'X_PIXEL'.lower():
                    try:
                        self.xpixel =int (stringSplit[1].strip())
                        logging.info(': Sucess 001 : dimensao X readed ')
                    except:
                        logging.info(': Modulo General Read Options : Error 014 : dimensao X readed failed ')
                    
                elif stringSplit[0].strip().lower() == 'Y_PIXEL'.lower():
                    try:
                        self.ypixel =int (stringSplit[1].strip())
                        logging.info(': Sucess 001 : dimensao Y readed ')
                    except:
                        logging.info(': Modulo General Read Options : Error 015 : dimensao Y readed failed ')

                elif stringSplit[0].strip().lower() == '<BEGIN_FILES_LIST>'.lower():
                    try:                        
                        for line in fid:
                            auxString=line
                            string=auxString.strip()

                            if line.strip().lower() == '<END_FILES_LIST>'.lower():
                                break
                            else :
                                auxValues=re.split(' +',string.strip())
                                self.files_list.append(string)
                        logging.info(': Sucess 001 : lista de ficheiros readed ')
                    except:
                        logging.info(': Modulo General Read Options : Error 016 : lista de ficheiros failed ')

                elif stringSplit[0].strip().lower() == '<BEGIN_FILES_LIST_COLUMN>'.lower():
                    try:                        
                        for line in fid:
                            auxString=line
                            string=auxString.strip()

                            if line.strip().lower() == '<END_FILES_LIST_COLUMN>'.lower():
                                break
                            else :
                                auxValues=re.split(' +',string.strip())
                            self.files_list_column.append(int(string))
                        logging.info(': Sucess 001 : lista de coluna de ficheiros readed ')
                    except:
                        logging.info(': Modulo General Read Options : Error 017 : lista de coluna de ficheiros failed ')

                elif stringSplit[0].strip().lower() == '<BEGIN_FILES_LIST_NAME>'.lower():
                    try:                        
                        for line in fid:
                            auxString=line
                            string=auxString.strip()
                            if line.strip().lower() == '<END_FILES_LIST_NAME>'.lower():
                                break
                            else :
                                auxValues=re.split(' +',string.strip())
                            self.files_list_name.append(string)
                        logging.info(': Sucess 001 : lista de nomes dos ficheiros readed ')
                    except:
                        logging.info(': Modulo General Read Options : Error 018 : lista de nomes dos ficheiros failed ')

                elif stringSplit[0].strip().lower() == '<BEGIN_FILES_OFFSET>'.lower():
                    try:                        
                        for line in fid:
                            auxString=line
                            string=auxString.strip()
                            if line.strip().lower() == '<END_FILES_OFFSET>'.lower():
                                break
                            else :
                                auxValues=re.split(' +',string.strip())
                                self.offset.append(float(string))
                        logging.info(': Sucess 001 : lista de offsets readed ')
                    except:
                        logging.info(': Modulo General Read Options : Error 019 : lista de offsets failed ')

                elif stringSplit[0].strip().lower() == '<BEGIN_TimeSeriesAnalyser>'.lower():
                    try:                        
                        for line in fid:
                            auxString = line
                            if line.strip().lower() == '<END_TimeSeriesAnalyser>'.lower():
                                break
                            else :
                                self.timeserieanalyser_config.append(auxString)
                        logging.info(': Sucess 001 : configuracoes timeseriesanalyser readed ')
                    except:
                        logging.info(': Modulo General Read Options : Error 020 : configuracoes timeseranalyser ')

                elif stringSplit[0].strip().lower() == '<BEGIN_hdf5nalyser>'.lower():
                    try:                        
                        for line in fid:
                            auxString = line
                            if line.strip().lower() == '<end_hdf5nalyser>'.lower():
                                break
                            else :
                                self.hdf5valida_config.append(auxString)
                        logging.info(': Sucess 001 : configuracoes timeseriesanalyser readed ')
                    except:
                        logging.info(': Modulo General Read Options : Error 020 : configuracoes timeseranalyser ')


                elif stringSplit[0].strip().lower() == '<BEGIN_FILES_COLOR>'.lower():
                    try:                        
                        for line in fid:
                            auxString=line
                            string=auxString.strip()
                            if line.strip().lower() == '<END_FILES_COLOR>'.lower():
                                break
                            else :
                                auxValues=re.split(' +',string.strip())
                            self.files_list_color.append(string)
                        logging.info(': Sucess 001 : lista de nomes dos ficheiros readed ')
                    except:
                        logging.info(': Modulo General Read Options : Error 000 : Lista de cores das Séries temporais ')

                elif stringSplit[0].strip().lower() == '<BEGIN_FILES_TYPE>'.lower():
                    try:                        
                        for line in fid:
                            auxString=line
                            string=auxString.strip()
                            if line.strip().lower() == '<END_FILES_TYPE>'.lower():
                                break
                            else :
                                auxValues=re.split(' +',string.strip())
                            self.files_list_type.append(string)
                        logging.info(': Sucess 001 : lista de nomes dos ficheiros readed ')
                    except:
                        logging.info(': Modulo General Read Options : Error 018 : lista de tipos de timeseries simbolos ')

                elif stringSplit[0].strip().lower() == 'EXECUTABLE_PATH'.lower():
                    try:
                        self.executable_exe=stringSplit[1].strip()
                        logging.info(': Sucess 001 : caminho para o executavel encontrado ')
                        if not self.logoPath:
                                raise ValueError('Empty String!')
                    except:
                        logging.info(': Modulo General Read Options : Error 021 : Caminho para o executavel nao encontrado')

                elif stringSplit[0].strip().lower() == 'STDEV_OBS'.lower():
                    try:
                        self.stdev_obs=float (stringSplit[1].strip())
                        logging.info(': Sucess 001 : Apresentar STDEV_OBS ')
                    except:
                        logging.info(': Modulo General Read Options : Error 022 : Não consegui ler a opção 0/1 em STDEV_OBS ')    

                elif stringSplit[0].strip().lower() == 'AVERAGE_OBS'.lower():
                    try:
                        self.average_obs=float (stringSplit[1].strip())
                        logging.info(': Sucess 001 : Apresentar AVERAGE_OBS ')
                    except:
                        logging.info(': Modulo General Read Options : Error 023 : Não consegui ler a opção 0/1 em AVERAGE_OBS ')   

                elif stringSplit[0].strip().lower() == 'BIAS'.lower():
                    try:
                        self.bias=float (stringSplit[1].strip())
                        logging.info(': Sucess 001 : Apresentar BIAS ')
                    except:
                        logging.info(': Modulo General Read Options : Error 024 : Não consegui ler a opção 0/1 em BIAS ')       

                elif stringSplit[0].strip().lower() == 'RMSE'.lower():
                    try:
                        self.rmse=float (stringSplit[1].strip())
                        logging.info(': Sucess 001 : Apresentar RMSE ')
                    except:
                        logging.info(': Modulo General Read Options : Error 025 : Não consegui ler a opção 0/1 em RMSE ')     

                elif stringSplit[0].strip().lower() == 'NORMALISE_RMSE'.lower():
                    try:
                        self.normalise_rmse=float (stringSplit[1].strip())
                        logging.info(': Sucess 001 : Apresentar Normalise RMSE [%] ')
                    except:
                        logging.info(': Modulo General Read Options : Error 026 : Não consegui ler a opção 0/1 em Normalise RMSE [%] ')  

                elif stringSplit[0].strip().lower() == 'UNBIAS_RMSE'.lower():
                    try:
                        self.unbias_rmse=float (stringSplit[1].strip())
                        logging.info(': Sucess 001 : Apresentar Unbias RMSE ')
                    except:
                        logging.info(': Modulo General Read Options : Error 027 : Não consegui ler a opção 0/1 em Unbias RMSE ')                         

                elif stringSplit[0].strip().lower() == 'NORMALISE_UNBIAS_RMSE'.lower():
                    try:
                        self.normalise_unbias_rmse=float (stringSplit[1].strip())
                        logging.info(': Sucess 001 : Apresentar Normalise unbias RMSE[%] ')
                    except:
                        logging.info(': Modulo General Read Options : Error 028 : Não consegui ler a opção 0/1 em Normalise unbias RMSE[%] ')                                 

                elif stringSplit[0].strip().lower() == 'RCORR'.lower():
                    try:
                        self.rcorr=float (stringSplit[1].strip())
                        logging.info(': Sucess 001 : Apresentar rcorr ')
                    except:
                        logging.info(': Modulo General Read Options : Error 029 : Não consegui ler a opção 0/1 em rcorr ')                                 

                elif stringSplit[0].strip().lower() == 'NASH_SUTCLIFFE'.lower():
                    try:
                        self.nash_sutcliffe=float (stringSplit[1].strip())
                        logging.info(': Sucess 001 : Apresentar NASH–SUTCLIFFE ')
                    except:
                        logging.info(': Modulo General Read Options : Error 030 : Não consegui ler a opção 0/1 em NASH–SUTCLIFFE ')                                 

                elif stringSplit[0].strip().lower() == 'SKILL'.lower():
                    try:
                        self.skill=float (stringSplit[1].strip())
                        logging.info(': Sucess 001 : Apresentar SKILL ')
                    except:
                        logging.info(': Modulo General Read Options : Error 031 : Não consegui ler a opção 0/1 em SKILL ')                                 

                elif stringSplit[0].strip().lower() == 'RCORR_QUAD'.lower():
                    try:
                        self.rcorr_quad=float (stringSplit[1].strip())
                        logging.info(': Sucess 001 : Apresentar rcorr_quad ')
                    except:
                        logging.info(': Modulo General Read Options : Error 032 : Não consegui ler a opção 0/1 em rcorr_quad ')                                 

                elif stringSplit[0].strip().lower() == 'Z_FISHER'.lower():
                    try:
                        self.z_fisher=float (stringSplit[1].strip())
                        logging.info(': Sucess 001 : Apresentar z_fisher ')
                    except:
                        logging.info(': Modulo General Read Options : Error 033 : Não consegui ler a opção 0/1 em z_fisher ')                                 

                elif stringSplit[0].strip().lower() == 'ALFA'.lower():
                    try:
                        self.alfa=float (stringSplit[1].strip())
                        logging.info(': Sucess 001 : Apresentar alfa ')
                    except:
                        logging.info(': Modulo General Read Options : Error 034 : Não consegui ler a opção 0/1 em alfa ')                                 

                elif stringSplit[0].strip().lower() == 'BETA_1'.lower():
                    try:
                        self.beta_1=float (stringSplit[1].strip())
                        logging.info(': Sucess 001 : Apresentar beta_1 ')
                    except:
                        logging.info(': Modulo General Read Options : Error 035 : Não consegui ler a opção 0/1 em beta_1 ')                                 

                elif stringSplit[0].strip().lower() == 'AM'.lower():
                    try:
                        self.am=float (stringSplit[1].strip())
                        logging.info(': Sucess 001 : Apresentar Am ')
                    except:
                        logging.info(': Modulo General Read Options : Error 036 : Não consegui ler a opção 0/1 em Am ')                                 

                elif stringSplit[0].strip().lower() == 'BM'.lower():
                    try:
                        self.bm=float (stringSplit[1].strip())
                        logging.info(': Sucess 001 : Apresentar Bm ')
                    except:
                        logging.info(': Modulo General Read Options : Error 037 : Não consegui ler a opção 0/1 em Bm ')  

                elif stringSplit[0].strip().lower() == 'VALIDATION_GRID_WS'.lower():
                    self.validation_grid_ws= float(stringSplit[1].strip())    

                elif stringSplit[0].strip().lower() == 'VALIDATION_GRID_HS'.lower():
                    self.validation_grid_hs= float(stringSplit[1].strip())    
                    
        except ValueError as ex:
            fid.close()
            logging.info(': Modulo General Read Options : Error 038 : No value for ' + stringSplit[0].strip().lower()) 
            logging.shutdown()
            sys.exit()

        fid.close()
        
    def readoptions(filename):

        logging.info(': Reading Configuration File')
        options = readOptions(filename)
        logging.info(': Finished reading Configuration File')
        
        return options 