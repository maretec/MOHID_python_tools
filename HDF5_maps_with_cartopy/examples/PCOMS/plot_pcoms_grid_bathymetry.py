import sys
sys.path.append('../../../Common')
from MHDF5_reader import MHDF5Reader
sys.path.append('../../src')
from lonlat_ticks import ticks_definer
from scalebar import scale_bar

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

# sets min and max values, leave None for automatic setting
minValue = None
maxValue = None

# figure information and titles
figTitle = 'PCOMS'
subplotTitle = 'Bathymetry'
widthInInches = 6.3
heightInInches = 7
figSaveName = 'pcoms_gridbathymetry'
imgFormat = '.png'
dpi = 300

# colorbar title and settings
colorbarLabel = 'Depth $(m)$'
colorbarLabelRotation = 90
colorbarNticks = 5
colorbarTicksDecimals = 0

# choose colormap from matplotlib options
cmap_name = 'viridis_r'

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

# creates matplotlib figure object and sets size and title
fig = plt.figure()
fig.set_size_inches(widthInInches, heightInInches)
fig.suptitle(figTitle)

# adds a subplot to the figure with the desired projection
ax = fig.add_subplot(projection=ccrs.Mercator())
# sets subplot title
ax.set_title(subplotTitle)

# sets extent of the subplot based on the grid of the hdf5 file
ax.set_extent([
    np.min(MHDF5Reader.getLonHorizontalGrid()),
    np.max(MHDF5Reader.getLonHorizontalGrid()),
    np.min(MHDF5Reader.getLatHorizontalGrid()),
    np.max(MHDF5Reader.getLatHorizontalGrid())],
    crs=ccrs.Mercator())

# get bathymetry array and sets -99.0 values to nan using the numpy library
bathymetryArray = MHDF5Reader.getBathymetry()
bathymetryArray = np.where(bathymetryArray == -99.0, np.nan, bathymetryArray)

# sets colormap and normalization of the color gradient
cmap = plt.get_cmap(cmap_name)
cmap.set_under(alpha=0)
if not minValue:
    minValue = np.nanmin(bathymetryArray)
else:
    minValue = minValue
if not maxValue:
    maxValue = np.nanmax(bathymetryArray)
else:
    maxValue = maxValue
norm = Normalize(vmin=minValue, vmax=maxValue)

# adds property using pcolormesh
mappable = ax.pcolormesh(
    MHDF5Reader.getLonHorizontalGrid(),
    MHDF5Reader.getLatHorizontalGrid(),
    bathymetryArray,
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
cbar.ax.invert_yaxis()

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
