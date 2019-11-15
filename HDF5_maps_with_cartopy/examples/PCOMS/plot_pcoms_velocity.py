import sys
sys.path.append('../../../Common')
from MHDF5_reader import MHDF5Reader
sys.path.append('../../src')
from lonlat_ticks import ticks_definer
from scalebar import scale_bar
from grid_to_center_cells import lonlat_grid_to_center_cells

import numpy as np
import h5py

import matplotlib as mlp
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize

import cartopy.crs as ccrs
from cartopy.feature import ShapelyFeature
from cartopy.io.shapereader import Reader

### USER INPUT ############################################################
# information on the hdf5 file 
fileName = 'Hydrodynamic_Surface.hdf5'
directory = 'Results_HDF/2019-08-07_2019-08-08'
propertyName = 'velocity modulus'
timeIndex = 8
Kcell = 1
# for plotting vectors
UpropertyName = 'velocity U'
VpropertyName = 'velocity V'

# sets min and max values, leave None for automatic setting
minValue = None
maxValue = None

# figure information and titles
figTitle = 'PCOMS'
subplotTitle = '2019-08-07 12:00'
widthInInches = 6.3
heightInInches = 7
figSaveName = 'pcoms_velocity'
imgFormat = '.png'
dpi = 300

# colorbar title and settings
colorbarLabel = 'Velocity $(m/s)$'
colorbarLabelRotation = 90
colorbarNticks = 5
colorbarTicksDecimals = 2

# useful options from matplotlib.quiver to change arrow appearence
## arrowScale - bigger values means smaller arrows
## arrowsRegridShape = bigger values means more arrows on the plot
arrowsScale = 2
arrowsRegridShape = 40

# choose colormap from matplotlib options
cmap_name = 'rainbow'

# number of levels for the contours
nLevels = 100

# longitude and latitude tick interval
tickInterval = 1.0

# shapefile for the land area
landShapefile = 'shapefile/portugal_extended.shp'
facecolor = 'lightgrey'
edgecolor = 'black'
###############################################################################

### MATPLOTLIB USEFUL PARAMETERS ##############################################
#more at https://matplotlib.org/users/customizing.html
# font used
mlp.rcParams['font.family'] = 'arial'
# figure title size
mlp.rcParams['figure.titlesize'] = 14
# subplot title size
mlp.rcParams['axes.titlesize'] = 12
# size of axis labels and colorbar label
mlp.rcParams['axes.labelsize'] = 10
# size of tick labels
mlp.rcParams['xtick.labelsize'] = 8
mlp.rcParams['ytick.labelsize'] = 8
###############################################################################


# creates an MHDF5Reader object to get data from the hdf5 file
MHDF5Reader = MHDF5Reader(fileName, directory, mandatoryMesh=False)

# because MOHID K starts at 1 and python indexes starts at 0
Kcell = Kcell - 1


# creates matplotlib figure object and sets size and title
fig = plt.figure()
fig.set_size_inches(widthInInches, heightInInches)
fig.suptitle(figTitle)

# adds a subplot to the figure with the desired projection
ax = fig.add_subplot(projection=ccrs.Mercator())
ax.set_title(subplotTitle)

# sets extent of the subplot based on the grid of the hdf5 file
ax.set_extent([
    np.min(MHDF5Reader.getLonHorizontalGrid()),
    np.max(MHDF5Reader.getLonHorizontalGrid()),
    np.min(MHDF5Reader.getLatHorizontalGrid()),
    np.max(MHDF5Reader.getLatHorizontalGrid())],
    crs=ccrs.Mercator())

# gets the desired property array from the hdf5 file
# propertyArray = MHDF5Reader.getProperty(propertyName, timeIndex)[k,j,i]
propertyArray = MHDF5Reader.getPropertyResults(propertyName, timeIndex)[Kcell,:,:]

# sets colormap and normalization of the color gradient
cmap = plt.get_cmap(cmap_name)
cmap.set_under(alpha=0)
if not minValue:
    minValue = np.min(propertyArray)
else:
    minValue = minValue
if not maxValue:
    maxValue = np.max(propertyArray)
else:
    maxValue = maxValue
norm = Normalize(vmin=minValue, vmax=maxValue)

# adds property using contourf

lonHorizontalCenterCells, latHorizontalCenterCells = lonlat_grid_to_center_cells(
    MHDF5Reader.getLonHorizontalGrid(),
    MHDF5Reader.getLatHorizontalGrid())

levels = np.linspace(minValue, maxValue, nLevels)
mappable = ax.contourf(
    lonHorizontalCenterCells,
    latHorizontalCenterCells,
    propertyArray,
    levels=levels,
    transform=ccrs.Mercator(),
    cmap=cmap,
    norm=norm)

# adds colorbar to plot
cbar = plt.colorbar(mappable, shrink=1, use_gridspec=True, cmap=cmap, norm=norm)
cbar_ticks = np.linspace(minValue, maxValue, colorbarNticks)
cbar.set_ticks(cbar_ticks)
if colorbarTicksDecimals == 0:
    cbar.set_ticklabels([int(x) for x in list(cbar_ticks)])
elif colorbarTicksDecimals > 0:
    cbar.set_ticklabels([round(x,colorbarTicksDecimals) for x in list(cbar_ticks)])
cbar.set_label(colorbarLabel, rotation=colorbarLabelRotation)

# adds arrows to plot
UpropArray = MHDF5Reader.getPropertyResults(UpropertyName, timeIndex)[Kcell,:,:]
VpropArray = MHDF5Reader.getPropertyResults(VpropertyName, timeIndex)[Kcell,:,:]
ax.quiver(
    x=lonHorizontalCenterCells,
    y=latHorizontalCenterCells,
    u=UpropArray,
    v=VpropArray,
    units='xy',
    angles='xy',
    scale_units='xy',
    scale=arrowsScale,
    regrid_shape=arrowsRegridShape,
    pivot='middle',
    transform=ccrs.Mercator())

# adds shapefile
land_feature = ShapelyFeature(
    Reader(landShapefile).geometries(),
    crs=ccrs.Mercator(),
    facecolor=facecolor)

ax.add_feature(
    land_feature,
    edgecolor=edgecolor)

# adds longitude and latitude ticks
xticks, yticks, xticklabels, yticklabels = ticks_definer(
    MHDF5Reader.getLonHorizontalGrid(),
    MHDF5Reader.getLatHorizontalGrid(),
    tickInterval)
ax.set_xticks(xticks, crs=ccrs.Mercator())
ax.set_yticks(yticks, crs=ccrs.Mercator())
ax.set_xticklabels(xticklabels)
ax.set_yticklabels(yticklabels)

scale_bar(ax, (0.8, 0.3), length=100)

fig.savefig(figSaveName+imgFormat, dpi=dpi)
