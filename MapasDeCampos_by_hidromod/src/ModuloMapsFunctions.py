# -*- coding: utf-8 -*-
import timeit
import ModuloMapsBasemaps
import sys
import datetime
import logging
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable, axes_size
from scipy.misc import imread
import matplotlib.cbook as cbook
import ModuloMapsFunctions
from PIL import Image
from scipy.interpolate import griddata
import sys, os  


class Maps(object):

    def _Datetime(self):
        
        try:
            self.Y = self.time[0]
            self.M = self.time[1]
            self.D = self.time[2]
            self.h = self.time[3]
            self.m = self.time[4]
            self.s = self.time[5]
        except Exception as ex:
            logging.info(': Modulo Maps Functions : Error 001 : Set datetime for title')
            logging.shutdown()
            sys.exit()

        try:
            if self.options.plot_type == 2:
                self.Y_end = self.time_end[0]
                self.M_end = self.time_end[1]
                self.D_end = self.time_end[2]
                self.h_end = self.time_end[3]
                self.m_end = self.time_end[4]
                self.s_end = self.time_end[5]
                return self
        except Exception as ex:
            logging.info(': Modulo Maps Functions : Error 001a : Set datetime end for title ')
            logging.shutdown()
            sys.exit()

    def _colormap(self):
        
        try:
               
            aux                 = np.float(self.options.scalarMax-self.options.scalarMin);
            aux_max_scale_split = 128
            if  self.options.dynamic_limits == 1:
                a=self.dsScalar[self.dsScalar> -1e5]
                aux= a.max() - a.min()
                #self.options.scalarMin = np.floor(a.min() - 0.1 * aux)
                #self.options.scalarMax = np.ceil(a.max() - 0.1 * aux)
                self.options.scalarMin = np.floor(a.min())
                self.options.scalarMax = np.ceil(a.max())
                aux_max_scale_split = 21

                # casos especais plot_type=2
                try:
                    if 'temp_max' in dir(self.options):
                        pass
                    else:
                        self.options.temp_min = None
                        self.options.temp_max = None

                    if  any('average' in s for s in self.options.maps_validation_parameters[self.options.subplot_index][6].split('/')):  # se for pr observations e modelo escala é igual
                        if self.options.temp_max is not None:
                            self.options.scalarMax=self.options.temp_max
                            self.options.scalarMin=self.options.temp_min
                        else:
                            self.options.temp_min=self.options.scalarMin
                            self.options.temp_max=self.options.scalarMax
                except Exception as ex:
                    logging.info(': Modulo Maps Functions : Error 001_a : set equal colormaps for Average imagens'+ex )
                    logging.shutdown()
                    sys.exit()

                try:
                    if  any('bias' in s for s in self.options.maps_validation_parameters[self.options.subplot_index][6].split('/')):  # se for pr observations e modelo escala é igual
                        aux_1 = [self.options.scalarMin,self.options.scalarMax]
                        value=max(min(aux_1), max(aux_1), key=abs)
                        self.options.scalarMin = abs(value) * -1
                        self.options.scalarMax = abs(value)
                except Exception as ex:
                    logging.info(': Modulo Maps Functions : Error 001_b : force Module values in colorbar for BIAS' + ex)
                    logging.shutdown()
                    sys.exit()

                try:
                    if  'r' in self.options.maps_validation_parameters[self.options.subplot_index][6].split('/'):  # se for pr observations e modelo escala é igual
                        aux_1 = [self.options.scalarMin,self.options.scalarMax]
                        value=max(min(aux_1), max(aux_1), key=abs)
                        self.options.scalarMin = -1
                        self.options.scalarMax = 1
                except Exception as ex:
                    logging.info(': Modulo Maps Functions : Error 001_c : force Module values in colorbar for R' + ex)
                    logging.shutdown()
                    sys.exit()

                try:
                    if  any('rmse' in s for s in self.options.maps_validation_parameters[self.options.subplot_index][6].split('/')):  # se for pr observations e modelo escala é igual
                        self.options.scalarMin = 0
                except Exception as ex:
                    logging.info(': Modulo Maps Functions : Error 001_d : force Module values in colorbar for RMSE' + ex)
                    logging.shutdown()
                    sys.exit()


            if isinstance(self.options.colormap,list):
                self.v = np.linspace(self.options.scalarMin, self.options.scalarMax, ((aux*2)/self.options.colorbarSpacing)+1, endpoint=True)
                self.cmap=mpl.colors.ListedColormap(self.options.colormap)
                #cmap=mpl.colors.ListedColormap([[0.0, 0.0, 0.4],[0.0, 0.0, 0.8],[0.13, 0.33, 0.87],
                #                               [0.27, 0.67, 0.93],[0.4, 1.0, 1.0],[0.3, 0.9, 0.75],
                #                               [0.2, 0.8, 0.5],[0.1, 0.7, 0.25],[0.4, 0.8, 0.0],
                #                               [0.8, 1.0, 0.6],[1.0, 1.0, 0.2],[1.0, 1.0, 0.2],
                #                               [1.0, 0.6, 0.0],[1.0, 0.6, 0.0],[1.0, 0.0, 0.0],
                #                               [1.0, 0.0, 0.0],[0.8, 0.0, 0.0],[0.8, 0.0, 0.0],
                #                               [0.4, 0.0, 0.0],[0.4, 0.0, 0.0]])
            else:
                self.v = np.linspace(self.options.scalarMin, self.options.scalarMax, aux_max_scale_split, endpoint=True)
                self.cmap = plt.get_cmap(self.options.colormap) 
            return self
        except Exception as ex:
            logging.info(': Modulo Maps Functions : Error 002 : Set colormap ' + ex)
            logging.shutdown()
            sys.exit()


    def _ColormapLimit(self):
        
        try:
            if self.options.plot_type is not 0:
                try:
                    if self.options.scalarMin is None:
                        self.options.scalarMin = np.nanmin(np.nanmin(self.dsScalar, axis=1), axis=0)
                    if self.options.scalarMax is None:
                        self.options.scalarMax = np.nanmax(np.nanmax(self.dsScalar, axis=1), axis=0)
                except Exception as ex:
                    logging.info(': Modulo Maps Functions : Error 003 : Failed to set up max and min scale values. ' + ex)
                    logging.shutdown()
                    sys.exit()

                try:
                    min = np.nanmin(np.nanmin(self.dsScalar, axis=1), axis=0)
                    max = np.nanmax(np.nanmax(self.dsScalar, axis=1), axis=0)

                    if  self.options.dynamic_limits == 1:
                        min=self.options.scalarMin
                        max=self.options.scalarMax


                    if self.options.extend is None:
                        if min < self.options.scalarMin and max <= self.options.scalarMax:
                            self.ext = 'min'
                        elif max > self.options.scalarMax and min >= self.options.scalarMin:
                            self.ext = 'max'
                        elif min < self.options.scalarMin and max > self.options.scalarMax:
                            self.ext = 'both'
                        else:
                            self.ext = 'neither'
                    else:
                        self.ext = self.options.extend
                    return self
                except Exception as ex:
                    logging.info(': Modulo Maps Functions : Error 004 : Failed to set up extended scales values. ' + ex)
                    logging.shutdown()
                    sys.exit()
        except Exception as ex:
            logging.info(': Modulo Maps Functions : Error 005 : Failed to manipulate Scale map/bar values.' + ex)
            logging.shutdown()
            sys.exit()


    def _Contour(self):
        try:
            if self.options.plot_type is not 0:
                try:
                    if self.options.justvector is not 1 and self.options.pcolor is not 1:
                        try:
                            if self.options.LogMap == 1:
                                self.pa = plt.contourf(self.lonlatcellcenter.lonC,self.lonlatcellcenter.latC,self.dsScalar,levels=self.options.LogMapLevels,cmap=self.cmap,norm=LogNorm(),spacing='proportional',interpolation="nearest")
                            else:
                                self.pa = plt.contourf(self.lonlatcellcenter.lonC,self.lonlatcellcenter.latC,self.dsScalar,self.v,cmap=self.cmap,extend=self.ext, spacing='proportional',interpolation="nearest")
                        except Exception as ex:
                            logging.info(': Modulo Maps Functions : Error 006 : Failed to set only Vectores field.' + ex)
                            logging.shutdown()
                            sys.exit()                
                except Exception as ex:
                    logging.info(': Modulo Maps Functions : Error 007 : Failed to set only Vectores field.' + ex)
                    logging.shutdown()
                    sys.exit()
                return self
        except Exception as ex:
            logging.info(': Modulo Maps Functions : Error 007 : Failed to manipulate Scale map/bar values.' + ex)
            logging.shutdown()
            sys.exit()


    def _Pcolor(self):
        
        try:
            if self.options.plot_type is not 0:
                try:
                    if self.options.pcolor  == 1:
                        try:
                            masked_array = np.ma.array (self.dsScalar, mask=np.isnan(self.dsScalar))
                            self.pa = plt.pcolormesh(self.lonlatcellcenter.lonC,self.lonlatcellcenter.latC,masked_array,cmap=self.cmap, vmin=self.options.scalarMin, vmax=self.options.scalarMax)
                        except Exception as ex:
                            logging.info(': Modulo Maps Functions : Error 008 : Some problem trying to use Pcolor' + ex)
                            logging.shutdown()
                            sys.exit()          
                except Exception as ex:
                    logging.info(': Modulo Maps Functions : Error 009 : Some problem trying to use Pcolor' + ex)
                    logging.shutdown()
                    sys.exit()
                return self
        except Exception as ex:
            logging.info(': Modulo Maps Functions : Error 010 : Some problem trying to use Pcolor' + ex)
            logging.shutdown()
            sys.exit()


    def _DrawQuiver(self):
        
        try:
            if self.options.plot_type == 1:
                try:
                    if self.options.vectorX is not None and self.options.vectorY is not None:
                        logging.info(': Drawing data (vector)... ')
                        if self.options.constantvector == 1 or (self.options.vectorX.find('wave') == 1 and self.options.figAMOS==1):
                            length  = np.sqrt(self.dsVectorx**2 + self.dsVectory**2)
                            UN = self.dsVectorx/length
                            VN = self.dsVectory/length
                            angles = 'uv'
                        elif self.options.constantvector == 2  or (self.options.vectorX.find('velocity') == 1 and self.options.figAMOS==1):
                            self.dsVectory[(self.dsVectory > -0.0001) & (self.dsVectory < 0.0001) & (self.dsVectorx > -0.0001) & (self.dsVectorx < 0.0001)] = None
                            self.dsVectorx[(self.dsVectorx > -0.0001) & (self.dsVectorx < 0.0001) & (self.dsVectory > -0.0001) & (self.dsVectory < 0.0001)] = None
                            def symlog(x):
                                return np.sign(x) * np.log10(np.abs(x))
                            UN = symlog(self.dsVectorx*1000)
                            VN = symlog(self.dsVectory*1000)
                            angles1=np.arctan2(self.dsVectory,self.dsVectorx)*180.0/np.pi # calculate angles manually
                            angles = angles1[::self.options.vectorStep, ::self.options.vectorStep]
                        else:
                            UN = self.dsVectorx
                            VN = self.dsVectory
                            angles = 'uv'

                        plt.hold(True)
                        plt.quiver(self.lonlatcellcenter.lonC[::self.options.vectorStep, ::self.options.vectorStep],
                                    self.lonlatcellcenter.latC[::self.options.vectorStep, ::self.options.vectorStep],
                                    UN[::self.options.vectorStep, ::self.options.vectorStep],
                                    VN[::self.options.vectorStep, ::self.options.vectorStep],
                                    units=self.options.
                                    quiverunits,
                                    angles=angles,
                                    scale=self.options.vectorSize,
                                    width=(self.options.vectorWidth),
                                    headwidth=4,
                                    headaxislength=4,
                                    edgecolors='none',
                                    headlength=4,
                                    pivot='middle',
                                    linestyle='solid',
                                    color=self.options.vectorcolor)       
                except Exception as ex:
                    logging.info(': Modulo Maps Functions : Error 011 : Failed to draw vectores ' +ex)
                    logging.shutdown()
                    sys.exit()
                return self
        except Exception as ex:
            logging.info(': Modulo Maps Functions : Error 011 : Failed to draw vectores ' +ex)
            logging.shutdown()
            sys.exit()


    def _ColorBar(self):
        
        try:
            if self.options.plot_type is not 0 and self.options.justvector is not 1:
                try:  
                    ax = plt.gca()
                    divider = make_axes_locatable(ax)
                    try:
                        if self.options.decimalcolorbar is not None:
                            decimal = '%.' + str(self.options.decimalcolorbar) + 'f'
                        else:
                            decimal = None
                    except Exception as ex:
                        logging.info(': Modulo Maps Functions : Error 012 : Failed to calculate decimacolorbar ' + ex)
                        logging.shutdown()
                        sys.exit()

                    try:
                        aux = np.float(self.options.scalarMax-self.options.scalarMin);                    
                        if self.options.LogMap == 1:
                            cba   = plt.colorbar(self.pa)
                        else:
                            if self.options.colorbar== 1 or self.options.colorbar==2:
                                try:
                                    if self.options.scalarMin >= self.options.scalarMax:
                                        logging.info(': Modulo Maps Functions : Error 013a : Scalar ´Min is bigger then Max. ' + ex)
                                        logging.shutdown()
                                        sys.exit()
                                except Exception as ex:
                                    logging.info(': Modulo Maps Functions : Error 013a : Scalar ´Min is bigger then Max. ' + ex)
                                    logging.shutdown()
                                    sys.exit()
                                v2 = np.linspace(self.options.scalarMin, self.options.scalarMax,round((aux/self.options.colorbarSpacing)+1,4))

                                
                                if  self.options.dynamic_limits == 1:
                                    v2 = np.linspace(self.options.scalarMin, self.options.scalarMax,11)


                                if len(v2)> 200:
                                    logging.info(': Modulo Maps Functions : Error 013 : you requested more then 200 colorbar splits, please reduce')
                                    logging.shutdown()
                                    sys.exit()

                                if self.options.orientationcolorbar == 'horizontal':
                                    width = axes_size.AxesX(ax, aspect=1/50)
                                    pad = axes_size.Fraction(4, width)
                                    cba = plt.colorbar(selfpa,ticks=v2,extend='max',spacing='proportional',orientation='horizontal',format=decimal)
                                elif self.options.orientationcolorbar == 'vertical':
                                    width = axes_size.AxesY(ax, aspect=1/35)
                                    pad = axes_size.Fraction(0.55, width)
                                    if self.options.plot_type == 2:
                                        divider = make_axes_locatable(ax)
                                        cax = divider.append_axes("right", size="5%", pad=0.05)
                                        cba = plt.colorbar(self.pa,
                                                           cax=cax,
                                                           ticks=v2,
                                                           extend='max',
                                                           spacing='proportional', 
                                                           orientation='vertical',
                                                           format=decimal)
                                    elif self.options.plot_type == 1:
                                        width = axes_size.AxesY(ax, aspect=1/35)
                                        pad = axes_size.Fraction(0.55, width)
                                        cba = plt.colorbar(self.pa, 
                                                           cax=divider.append_axes("right", size=0.085, pad=pad),
                                                           ticks=v2,
                                                           extend='max',
                                                           spacing='proportional', 
                                                           orientation='vertical',
                                                           format=decimal)
                    except Exception as ex:
                        logging.info(': Modulo Maps Functions : Error 013 : Failed to calculate width, pad and cba from colorbar. ' + ex)
                        logging.shutdown()
                        sys.exit()


                    try:
                        mpl.rcParams.update({'font.size': self.options.fontsize}) 
                        if self.options.legend is not None and self.options.colorbar!=0:
                            if self.options.plot_type ==2:
                                cba.set_label(self.options.legend,
                                              fontsize=self.options.fontsize, 
                                              rotation=270,
                                              labelpad=7)
                                for t in cba.ax.get_yticklabels():
                                    t.set_horizontalalignment('right')
                                    t.set_x(2.2)

                            else:
                                cba.set_label(self.options.legend,
                                              fontsize=self.options.fontsize)                            
                    except Exception as ex:
                        logging.info(': Modulo Maps Functions : Error 014 : Failed to draw colorbar title. ' + ex)
                        logging.shutdown()
                        sys.exit()
                except Exception as ex:
                    logging.info(': Modulo Maps Functions : Error 015 : Failed inside colorbar manipulation ')
                    logging.shutdown()
                    sys.exit()
                return self
        except Exception as ex:
            logging.info(': Modulo Maps Functions : Error 016 : Failed inside colorbar manipulation ')
            logging.shutdown()
            sys.exit()


    def _Polygon(self):
        
        try:
            if self.options.plot_type is not 0:
                try:
                    if self.options.polygonfill == 1:
                        if self.options.polygonfill == 1:
                            try:
                                plt.hold(True)
                                plt.fill(self.options.polyX,self.options.polyY,linewidth=0.5, color=self.options.polygoncolor)
                            except Exception as ex:
                                logging.info(': Modulo Maps Functions : Error 017 : Fail to plot the polygon fill' + ex)
                                logging.shutdown()
                                sys.exit() 
                        else:
                            try:
                                plt.hold(True)
                                plt.plot(self.options.polyX,self.options.polyY,linewidth=2, color=self.options.polygoncolor, linestyle='--')
                            except Exception as ex:
                                logging.info(': Modulo Maps Functions : Error 018 : Fail to plot the polygon Line' +ex)
                                logging.shutdown()
                                sys.exit() 
                except Exception as ex:
                    logging.info(': Modulo Maps Functions : Error 019 : Failed inside colorbar manipulation ' +ex)
                    logging.shutdown()
                    sys.exit()
        except Exception as ex:
            logging.info(': Modulo Maps Functions : Error 020 : Failed inside colorbar manipulation ' +ex)
            logging.shutdown()
            sys.exit()


    def _StreamLines(self):
        
        try:
            if self.options.plot_type is 1:
                try:
                    if self.options.streamX is not None and self.options.streamY is not None:
                        try:
                            xx=self.lonlatcellcenter.lonC
                            yy=self.lonlatcellcenter.latC
                            u=self.dsstreamx
                            v=self.dsstreamy

                            x = np.linspace(xx.min(), xx.max(), 50)
                            y = np.linspace(yy.min(), yy.max(), 50)
                            speed = np.sqrt((u**2)+(v**2))

                            xi, yi = np.meshgrid(x,y)

                            px = xx.flatten()
                            py = yy.flatten()
                            pu = u.flatten()
                            pv = v.flatten()
                            pspeed = speed.flatten()

                            gu        = griddata((px,py), pu, (xi,yi))
                            gv        = griddata((px,py), pv, (xi,yi))
                            gspeed    = griddata((px,py), pspeed, (xi,yi))

                            lw = 6*gspeed/np.nanmax(gspeed)
                            if self.options.stream_color is None:
                                color=gspeed
                            else:
                                color=self.options.stream_color


                            c = plt.streamplot(x,
                                              y,
                                              gu,
                                              gv,
                                             density=self.options.stream_density,
                                             linewidth=lw* self.options.stream_linewidth,
                                             color=color,
                                             norm= [0, 1],
                                             arrowsize= self.options.stream_arrow_factor,
                                             cmap=plt.cm.jet)


                        except Exception as ex:
                            logging.info(': StreamLines not developed ' + ex)
                            logging.shutdown()
                            sys.exit()

                except Exception as ex:
                    logging.info(': StreamLines not developed ')
                    logging.shutdown()
                    sys.exit()
        except Exception as ex:
            logging.info(': Modulo Maps Functions : StreamLines : Error 001 : Failed inside colorbar manipulation '  + ex)
            logging.shutdown()
            sys.exit()


    def _AxisLabels(self):
        
        try:
            if self.options.plot_type is not 0:
                try:
                    if self.options.label == 1:
                        logging.info(': Insert x and y label... ')
                        if self.options.dy >= 1:
                            labelpad = 25
                        else:
                            labelpad = 40
                        plt.ylabel('Latitude ($^\circ$)',labelpad=labelpad, fontsize=self.options.fontsize-1)
                        plt.xlabel('Longitude ($^\circ$)',labelpad=12, fontsize=self.options.fontsize-1)
                except Exception as ex:
                    logging.info(': Modulo Maps Functions : Error 022 : Failed to draw Axis Labels ' + ex)
                    logging.shutdown()
                    sys.exit()
        except Exception as ex:
            logging.info(': Modulo Maps Functions : Error 023 : Failed inside colorbar manipulation '  + ex)
            logging.shutdown()
            sys.exit()


    def _PointsLabel(self):
        
        try:
            if self.options.plot_type is not 0:
                    if self.options.points == 1:
                        logging.info(': Insert points in map... ')
                        try:
                            plt.hold(True)
                
                            for ii in range(0,len(self.options.XPoints)):
                                plt.hold(True)
                                plt.text(self.options.XPoints[ii],self.options.YPoints[ii],self.options.NamePoints[ii], color='k', 
                                         fontsize=self.options.fontsizepoints,fontweight='bold',horizontalalignment='right',verticalalignment='top',bbox=dict(facecolor='w', edgecolor='none',alpha=0.4))
                            plt.plot(self.options.XPoints,self.options.YPoints,linestyle='None', marker='o', color=self.options.colorpoints, markersize=5, markeredgecolor ='none')
                        except Exception as ex:
                            logging.info(': Modulo Maps Functions : Error 024 : Points error')
                            logging.shutdown()
                            sys.exit() 
        except Exception as ex:
            logging.info(': Modulo Maps Functions : Error 025 : Failed to add Points in map label '  + ex)
            logging.shutdown()
            sys.exit()


    def _HidroLogo(self):
        
        try:
            if self.options.plot_type is not 0:
                if self.options.logoPath is not None:
                    logging.info(': Insert the Hidromod logo... ')
                    datafile = cbook.get_sample_data(self.options.logoPath, asfileobj=False)
                    datafile = self.options.logoPath
                    img = imread(datafile)
                    height, width = img.shape[:2]
                    dx = (self.options.Xmax-self.options.Xmin)/6
                    extent = [self.options.Xmin,self.options.Xmin+dx, self.options.Ymax-dx*(height/width),self.options.Ymax]
                    plt.imshow(img,zorder=6,alpha=0.8,extent=extent,shape=[width,height])
        except Exception as ex:
            logging.info(': Modulo Maps Functions : Error 026 : Failed to Plot Hidromod Logo '  + ex)
            logging.shutdown()
            sys.exit()

    def _FigureOutName(self,date_object):
        
        try:
            if self.options.plot_type is not 0:
                if self.options.figureOutName is not None:
                    figureNameParts = self.options.figureOutName.split('@')
                    if len(figureNameParts)==3:
                        self.figure_out = figureNameParts[0] + date_object.strftime(figureNameParts[1]) + figureNameParts[2]
                        self.options.figure_out = figureNameParts[0] + date_object.strftime(figureNameParts[1]) + figureNameParts[2]
                    elif len(figureNameParts)==5: #caso de plot_type2
                        self.figure_out = figureNameParts[0] + date_object.strftime(figureNameParts[1]) + '_' + self.date_object_end.strftime(figureNameParts[1]) + figureNameParts[4]
                        self.options.figure_out = figureNameParts[0] + date_object.strftime(figureNameParts[1]) + '_' + self.date_object_end.strftime(figureNameParts[1]) + figureNameParts[4]
                    else:
                        aux = self.options.figureOutName.split('.')
                        self.figure_out = aux[0] + self.timeIndex + '.' + aux[1]
                        self.options.figure_out = aux[0] + self.timeIndex + '.' + aux[1]
                else:
                    stringSplit=self.options.scalar.split('/')
                    self.figure_out = stringSplit[len(stringSplit)-1] + self.timeIndex + ('.png')
                    options.figure_out = stringSplit[len(stringSplit)-1] + self.timeIndex + ('.png')
        except Exception as ex:
            logging.info(': Modulo Maps Functions : Error 027 : Failed to give name to Figure '  + ex)
            logging.shutdown()
            sys.exit()

    def _Transparency(self):
        
        try:
            if self.options.plot_type is not 0:
                logging.info(': Saving figure... ')
                if self.options.figuretransparent is 0:
                    self.options.figuretransparent = False
                elif self.options.figuretransparent is 1:
                    self.options.figuretransparent = True
                    self.options.figurecolor = 'None'
                    self.options.CompressImage = 0
        except Exception as ex:
            logging.info(': Modulo Maps Functions : Error 028 : Failed to give name to Figure '  + ex)
            logging.shutdown()
            sys.exit()

    def _ImageSize(self,fig):
        
        try:
            if self.options.plot_type == 1:
                if self.options.xpixel is not None and self.options.ypixel is not None:
                    fig.set_size_inches(float(self.options.xpixel)/float(self.options.dpi),float(self.options.ypixel)/float(self.options.dpi),forward=True)
                    fig.subplots_adjust(bottom=0.07,left=0.07, right=0.99, top=0.99)
                return fig
            elif self.options.plot_type == 2:
                if self.options.xpixel is not None and self.options.ypixel is not None:
                    fig.set_size_inches(8, 6)

                    fig.set_size_inches(float(self.options.xpixel)/float(self.options.dpi),
                                        float(self.options.ypixel)/float(self.options.dpi),forward=True)
                return fig
        except Exception as ex:
            logging.info(': Modulo Maps Functions : Error 029 : Failed to give name to Figure '  + ex)
            logging.shutdown()
            sys.exit()

    def _SaveImage(self,fig):
                
        try:
            if self.options.plot_type is 2:
                fig.savefig(self.figure_out, 
                            facecolor=self.options.figurecolor, 
                            edgecolor=self.options.figurecolor,
                            orientation='portrait', 
                            papertype=None, 
                            format=None,
                            transparent=self.options.figuretransparent, 
                            pad_inches=0.1,
                            dpi=self.options.dpi)
            elif self.options.plot_type is 1:
                fig.savefig(self.figure_out, 
                            facecolor=self.options.figurecolor, 
                            edgecolor=self.options.figurecolor,
                            orientation='portrait', 
                            papertype=None, 
                            format=None,
                            transparent=self.options.figuretransparent,
                            bbox_inches='tight', 
                            pad_inches=0.1,
                            dpi=self.options.dpi)
        except Exception as ex:
            logging.info(': Modulo Maps Functions : Error 030 : Saving figure '  + ex)
            logging.shutdown()
            sys.exit()


    def _Image2JPEG(self):
        
        try:
            if self.options.plot_type is not 0:
                if self.options.CompressImage == 1 and self.options.figurequality is not None and self.options.figuretransparent is False:  
                    logging.info(': CompressImage figure... ')
                    Image.open(self.figure_out).save(self.figure_out, "JPEG", quality=self.options.figurequality, optimize=True)
        except Exception as ex:
            logging.info(': Modulo Maps Functions : Error 031 : To compress image to JPEG '  + ex)
            logging.shutdown()
            sys.exit()

