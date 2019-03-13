import matplotlib.pyplot as plt
import matplotlib.pyplot as plt_date
import matplotlib.dates as datesMat
import logging
import sys
from matplotlib import gridspec
import matplotlib as mpl
from matplotlib.offsetbox import AnchoredText
import numpy as np
import ModuloTimeSeriesFunctions as MTSF

class Draw_timeseries:
    def __init__(plottype,Timeseries,options):

        if options.plot_image_type == 'timeseries':
            if plottype == 1:
                Draw_timeseries.drawplot_solo(options,serie1y)
            elif plottype == 2:
                Draw_timeseries.drawplot2(Timeseries,options)
            elif plottype == 3:
                DRAW.drawplot_solo(options,serie1y)
            elif plottype == 4:
                Draw_timeseries.drawpscatter(options,serie1y)
            elif plottype == 5:
                Draw_timeseries.drawplot5(Timeseries,options)
        if options.plot_image_type == 'maps':
            if plottype == 2:
                Draw_timeseries.drawplot2Maps(Timeseries,options)


    def drawplot2(Timeseries,options):
        import matplotlib.pyplot as plt
        import matplotlib.pyplot as plt_date
        import matplotlib.dates as datesMat
        import logging
        import sys

        try:
            logging.info(': A desenhar o Grafico')

            fig = plt.figure()
            ax1 = fig.add_subplot(111)

            if options.xpixel is not None and options.ypixel is not None:
                fig.set_size_inches(float(options.xpixel)/float(options.dpi),float(options.ypixel)/float(options.dpi),forward=True)
                fig.subplots_adjust(bottom=0.07,left=0.07, right=0.99, top=0.99)

            ax1.set_title(options.title,fontsize=options.fontsize)    
            ax1.set_xlabel(options.xlabel,fontsize=options.fontsize-1)

            if options.xlabel is None:
                ax1.set_xlabel('',fontsize=options.fontsize-1)
            else:
                ax1.set_xlabel(options.xlabel,fontsize=options.fontsize-1)

            if options.ylabel is None:
                ax1.set_ylabel('',fontsize=options.fontsize-1)
            else:
                ax1.set_ylabel(options.ylabel,fontsize=options.fontsize-1)

            ax1.tick_params(labelsize=options.fontsize-1)
            ax1.hold(True)

            for x in range(0,len(options.files_list)):
                linestyle1= options.files_list_type[x].strip('"\'')

                try:
                    plt_date.plot_date(datesMat.date2num(Timeseries[x].ValuesX_datenum),
                                    Timeseries[x].ValuesY, 
                                    color                            =options.files_list_color[x].strip('"\''),
                                    label                            =options.files_list_name[x],
                                    linestyle                        = linestyle1,
                                    linewidth                        =options.linewidth, 
                                    xdate                            =True,
                                    ydate                            =False,
                                    marker                           =None)

                except Exception as ex:
                    logging.info(': Modulo TimeSeries Draw : Error 001 : Failed to draw TimeSerie Plot "' + options.files_list_name[0] + '"'+ ex)
                    logging.shutdown()
                    sys.exit()  

            fig.tight_layout()

        # Valor maximo da serie
            if options.Ymax is None:
                options.Ymax = max(Timeseries.Serie1.ValuesY)
            if options.Ymin is None:
                options.Ymax = min(Timeseries.Serie1.ValuesY)

            leg = ax1.legend(fontsize=options.fontsize-1)

            ax1.set_ylim([options.Ymin, options.Ymax])
            fig.autofmt_xdate()



        except Exception as ex:
            logging.info(': Error 008 : Cant plot the data')
            logging.shutdown()
            sys.exit()   

        try:
            logging.info(': A salvar a figura')

            fig.savefig(options.figureOutName, facecolor='w', edgecolor='w',
                orientation='portrait', papertype=None, format=None,
                transparent=True, bbox_inches='tight', pad_inches=0.01, dpi=options.dpi)
        except Exception as ex:
            logging.info(': Modulo TimeSeries Draw : Error 001 : Error Saving the Figure')
            logging.shutdown()
            sys.exit()   

    def drawplot_solo(serie1x,serie1y,serie2x,serie2y,options):
        logging.info('Trying to plot a single timeserie, not configured to')
        logging.shutdown()
        sys.exit()   
    def drawpscatter(Timeseries,options):
        logging.info('Trying to plot a scatter plot, not configured to')
        logging.shutdown()
        sys.exit()   

    def drawmultiplot(serie1x,serie1y,serie2x,serie2y,options):
        logging.info('Trying to plot a multi plot, not configured to')
        logging.shutdown()
        sys.exit()   

    def drawplot5(Timeseries,options):


        try:
            logging.info(': A desenhar o Grafico')

            fig = plt.figure()
            gs = gridspec.GridSpec(1, 2, width_ratios=[5, 1]) 
            ax1 = plt.subplot(gs[0]) # plot das séries
            ax2 = plt.subplot(gs[1]) # lista de validaçoes


            if options.xpixel is not None and options.ypixel is not None:
                fig.set_size_inches(float(options.xpixel)/float(options.dpi),float(options.ypixel)/float(options.dpi),forward=True)

            try:
                ax1.set_title(options.title,fontsize=options.fontsize)
            except:
                logging.info(': Modulo TimeSeries Draw : Error 002 : Erro no titulo/resumo erros')
                logging.shutdown()
                sys.exit()   


            ax1.set_xlabel(options.xlabel,fontsize=options.fontsize-1)

            if options.xlabel is None:
                ax1.set_xlabel('',fontsize=options.fontsize-1)
            else:
                ax1.set_xlabel(options.xlabel,fontsize=options.fontsize-1)

            if options.ylabel is None:
                ax1.set_ylabel('',fontsize=options.fontsize-1)
            else:
                ax1.set_ylabel(options.ylabel,fontsize=options.fontsize-1)

            ax1.tick_params(labelsize=options.fontsize-1)
            ax1.hold(True)

            # reduz o tamanho da série em função da primeira série
            max_plot_number = 1000
            plot_every_x_points = []
            try:
                if len(Timeseries.Serie1.ValuesX_datenum) <= max_plot_number:
                    plot_every_x_points = 1
                else:
                    for x in range(1,1000):
                        if round(len(Timeseries.Serie1.ValuesX_datenum) /  max_plot_number) <= max_plot_number:
                            plot_every_x_points = x
                            break
            except Exception as ex:
                logging.info(': Modulo TimeSeries Draw : Error 003 : Erro do limite de pontos a ser desenhado'+ str(ex))
                logging.shutdown()
                sys.exit()  

            # Desenha Plot 1
            try:
                plot1=ax1.plot_date(datesMat.date2num(Timeseries.Serie1.ValuesX_datenum[::plot_every_x_points]),
                              [x for x in Timeseries.Serie1.ValuesY[::plot_every_x_points]], 
                              marker='*', 
                              color='r',
                              markersize=2,
                              label=options.files_list_name[0],
                              xdate=True, 
                              ydate=False, 
                              markeredgecolor  ='r')
            except Exception as ex:
                logging.info(': Modulo TimeSeries Draw : Error 004 : Erro a desenhar o Plot 1'+ str(ex))
                logging.shutdown()
                sys.exit()   

            # Desenha Plot 2
            try:                
                plot2=ax1.plot_date(datesMat.date2num(Timeseries.Serie2.ValuesX_datenum[::plot_every_x_points]),
                                    [x for x in Timeseries.Serie2.ValuesY[::plot_every_x_points]], 
                                    '-', 
                                    color='k',
                                   linewidth=options.linewidth, 
                                   label=options.files_list_name[1], 
                                   xdate=True, 
                                   ydate=False)
            except Exception as ex:
                logging.info(': Modulo TimeSeries Draw : Error 005 : Erro a desenhar o Plot 2 ' + str(ex))
                logging.shutdown()
                sys.exit()   

        # Valor maximo da serie
            try:
                limits=[min(Timeseries.Serie1.ValuesY),min(Timeseries.Serie2.ValuesY),max(Timeseries.Serie1.ValuesY),max(Timeseries.Serie2.ValuesY)]
                if options.Ymax is None:
                    options.Ymax = max(limits)+0.15*(max(limits)-min(limits))
            except Exception as ex:                            
                logging.info(': Modulo TimeSeries Draw : Error 006 : Não consegui implemtnar os limites YMAX pedido ' + str(ex))
                logging.shutd

        # Valor minimo da serie
            try:
                limits=[min(Timeseries.Serie1.ValuesY),min(Timeseries.Serie2.ValuesY),max(Timeseries.Serie1.ValuesY),max(Timeseries.Serie2.ValuesY)]
                if options.Ymin is None:
                    options.Ymin = round(min(limits)-0.15*(max(limits)-min(limits)),1)
                    if round(options.Ymin,1) == 0:
                        options.Ymin = 0
                    elif min(limits) >0 or options.Ymin < 0:
                            options.Ymin = 0
            except Exception as ex:                            
                logging.info(': Modulo TimeSeries Draw : Error 007 : Não consegui implementar os limites YMIN pedido ' + str(ex))
                logging.shutdown()
                sys.exit()  

            ax1.set_ylim([options.Ymin, options.Ymax])

        # Desenhar Legenda
            try:
                mpl.rcParams['legend.numpoints'] = 1
                leg= ax1.legend(fontsize=options.fontsize-1, loc='upper center',ncol=3, fancybox=True, shadow=True)
            except Exception as ex:                            
                logging.info(': Modulo TimeSeries Draw : Error 008 : Problemas a desenhar a Legenda do grafico ' + str(ex))
                logging.shutdown()
                sys.exit()  

        # Formatar a caixa de erros.         
            try:
                xxx=list()
                numero_casas_decimais=3
                if options.stdev_obs == 1:
                    xxx.append('Stdev Obs = '+ str(format(round(Timeseries.Serie1.rmse,numero_casas_decimais))) + ' ' + options.parameter +  '\n')
                if options.average_obs == 1:
                    xxx.append('Average Obs = '+ str(format(round(Timeseries.Serie1.average_obs,numero_casas_decimais))) + ' ' + options.parameter +  '\n')
                if options.bias == 1:
                    xxx.append('BIAS = '+ str(format(round(Timeseries.Serie1.bias,numero_casas_decimais))) + ' ' + options.parameter +  '\n')
                if options.rmse == 1:
                    xxx.append('RMSE = '+ str(format(round(Timeseries.Serie1.rmse,numero_casas_decimais))) + ' ' + options.parameter +  '\n')
                if options.normalise_rmse == 1:
                    xxx.append('Normalise RMSE = '+ str(format(round(Timeseries.Serie1.normalise_rmse,numero_casas_decimais))) + '%\n')
                if options.unbias_rmse == 1:
                    xxx.append('Unbias RMSE = '+ str(format(round(Timeseries.Serie1.unbias_rmse,numero_casas_decimais))) + ' ' + options.parameter +  '\n')
                if options.normalise_unbias_rmse == 1:
                    xxx.append('Normalise Unbias RMSE = '+ str(format(round(Timeseries.Serie1.normalise_unbias_rmse,numero_casas_decimais))) + '%\n')
                if options.rcorr == 1:
                    xxx.append('R = '+ str(format(round(Timeseries.Serie1.rcorr,numero_casas_decimais))) + '\n')
                if options.nash_sutcliffe == 1:
                    xxx.append('Nash-Sutcliff = '+ str(format(round(Timeseries.Serie1.nash_sutcliffe,numero_casas_decimais))) + '\n')
                if options.skill == 1:
                    xxx.append('SKILL = '+ str(format(round(Timeseries.Serie1.skill,numero_casas_decimais))) + '\n')
                if options.rcorr_quad == 1:
                    xxx.append('Rcorr Quad = '+ str(format(round(Timeseries.Serie1.rcorr_quad,numero_casas_decimais))) + '\n')
                if options.z_fisher == 1:
                    xxx.append('Z-Fisher = '+ str(format(round(Timeseries.Serie1.z_fisher,numero_casas_decimais))) + '\n')
                if options.alfa == 1:
                    xxx.append('Alfa = '+ str(format(round(Timeseries.Serie1.alfa,numero_casas_decimais))) + '\n')
                if options.beta_1 == 1:
                    xxx.append('Beta 1 = '+ str(format(round(Timeseries.Serie1.beta_1,numero_casas_decimais))) + '\n')
                if options.am == 1:
                    xxx.append('Am = '+ str(format(round(Timeseries.Serie1.am,numero_casas_decimais))) + ' ' + options.parameter +  '\n')
                if options.bm == 1:
                    xxx.append('Bm = '+ str(format(round(Timeseries.Serie1.bm,numero_casas_decimais))) + ' ' + options.parameter +  '\n')
            except Exception as ex:                            
                logging.info(': Modulo TimeSeries Draw : Error 009 : Erro criar string de validação com ' + str(ex) + '\n')
                logging.shutdown()
                sys.exit()   


        # Desenha a caixa dos erros
            try:
                ax2.axis('off')
                anchored_text = AnchoredText(('\n'.join(xxx)),loc=7,prop=dict(size=options.fontsize),frameon=False)
                ax2.add_artist(anchored_text)
            except Exception as ex:                            
                logging.info(': Modulo TimeSeries Draw : Error 010 : Erro a desenhar string de erros ' + str(ex))
                logging.shutdown()
                sys.exit()  
                

            fig.autofmt_xdate()


            #try:
                #fig.tight_layout()
            #except Exception as ex:
                #logging.info(': Error 008 : Falha a fazer o tight layout')
                #logging.shutdown()
                #sys.exit()   


        except Exception as ex:
            logging.info(': Modulo TimeSeries Draw : Error 011 : Cant plot the data')
            logging.shutdown()
            sys.exit()   

        try:
            logging.info(': A salvar a figura')
            fig.savefig(options.figureOutName, facecolor='w', edgecolor='w',
                orientation='portrait',bbox_inches='tight', papertype=None, format=None,
                transparent=True, pad_inches=0.1, dpi=options.dpi)
            logging.info(': SUCESSO : figura salva')

        except Exception as ex:
            logging.info(': Modulo TimeSeries Draw : Error 012 : Error Saving the Figure')
            logging.shutdown()
            sys.exit()   


    def drawplot2Maps(Timeseries,options):
        
        try:
            logging.info(': Ploting TimeSerie Graph')

            ax = plt.subplot(str(options.validation_grid[0])+str(options.validation_grid[1])+str(int(options.maps_validation_parameters[options.subplot_index][1])))
            #ax.set_aspect(1.0)
            a=['','','','','','','','']
            #ax.set_yticks([])
                        
            for x in range(len(options.timeseries_validation_parameters)):
                try:
                    aux=0
                    rot=90
                    auxlabelpad=0

                    if x is not 0:
                        if int(options.timeseries_validation_parameters[x-1][6]) is not int((options.timeseries_validation_parameters[x][6])):
                            ax=ax.twinx()
                            rot=270
                            auxlabelpad=8

                        else:    
                            aux =1

                    linestyle1 = None;
                    if aux == 1:
                        linestyle1= '--'
                        del aux
                    else:
                        linestyle1= '-'
                    
                    a[x]=ax.plot_date(datesMat.date2num(Timeseries[x].ValuesX_datenum),
                                 Timeseries[x].ValuesY, 
                                 color                            =options.timeseries_validation_parameters[x][3].strip(' ')[1],
                                 label                            =options.timeseries_validation_parameters[x][7],
                                 linestyle                        = linestyle1,
                                 xdate                            =True,
                                 ydate                            =False,
                                 marker                           =None)

                    try:
                        if options.dynamic_limits == 1:
                            MTSF.TS._Dynamic_plot_limit(Timeseries,ax, options, x)
                        else:
                            ax.set(ylim=[float(options.timeseries_validation_parameters[x][4]),float(options.timeseries_validation_parameters[x][5])])
                    except Exception as ex:
                        logging.info(': Modulo TimeSeries Functions : Error 012a : Dynamic plot timeseries limits' + ex)
                        logging.shutdown()
                        sys.exit()

                        
                    plt.ylabel(options.timeseries_validation_parameters[x][8].strip(),
                               rotation=rot,
                               labelpad=auxlabelpad,
                               color=options.timeseries_validation_parameters[x][3].strip(' ')[1])

                    plt.setp( ax.xaxis.get_majorticklabels(), rotation=20, horizontalalignment='right' )

                    ax.xaxis.set_major_locator(datesMat.AutoDateLocator())
                    ax.xaxis.set_major_formatter(datesMat.DateFormatter('%Y %m %d'))

                    for tl in ax.get_yticklabels():
                        tl.set_color(options.timeseries_validation_parameters[x][3].strip(' ')[1])
                    #ax.set_ylim([0,100])
                except Exception as ex:
                    logging.info(': Modulo TimeSeries Draw : Error 013 : Erro a desenhar o Plot '+ options.timeseries_validation_parameters[x][7] +  str(ex))
                    logging.shutdown()
                    sys.exit()   
                    
        # Desenhar Legenda
            try:
                #mpl.rcParams['legend.numpoints'] = 2
                plt.subplots_adjust()
                b=[]
                for x in range(len(options.timeseries_validation_parameters)):
                    b=b+a[x]

                labs = [l.get_label() for l in b]

                for x in range(len(labs)):
                    labs[x]=labs[x].strip()

                leg= ax.legend(b,
                               labs,
                               fontsize=options.fontsize, 
                               loc='upper center',
                               ncol=3, 
                               fancybox=False, 
                               shadow=False,
                               handlelength=4)
            except Exception as ex:                            
                logging.info(': Modulo TimeSeries Draw : Error 014 : Problemas a desenhar a Legenda do grafico ' + str(ex))
                logging.shutdown()
                sys.exit()  
                             
            #fig = plt.gcf()

            #fig.autofmt_xdate()

        except Exception as ex:
            logging.info(': Modulo TimeSeries Draw : Error 015 : Cant plot the ')
            logging.shutdown()
            sys.exit()   
