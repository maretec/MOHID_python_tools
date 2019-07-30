# state file generated using paraview version 5.5.2

# ----------------------------------------------------------------
# setup views used in the visualization
# ----------------------------------------------------------------

# trace generated using paraview version 5.5.2

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# get the material library
materialLibrary1 = GetMaterialLibrary()

# Create a new 'Render View'
renderView1 = CreateView('RenderView')
renderView1.ViewSize = [2073, 852]
renderView1.AnnotationColor = [0.0, 0.0, 0.0]
renderView1.InteractionMode = '2D'
renderView1.AxesGrid = 'GridAxes3DActor'
renderView1.OrientationAxesLabelColor = [0.0, 0.0, 0.0]
renderView1.OrientationAxesOutlineColor = [0.0, 0.0, 0.0]
renderView1.CenterOfRotation = [-0.03351329999998143, 0.03342329999999549, 0.0]
renderView1.StereoType = 0
renderView1.CameraPosition = [-0.03351329999998143, 0.03342329999999549, 777.3817258562809]
renderView1.CameraFocalPoint = [-0.03351329999998143, 0.03342329999999549, 0.0]
renderView1.CameraParallelScale = 120.11471723575981
renderView1.Background = [1.0, 1.0, 1.0]
renderView1.OSPRayMaterialLibrary = materialLibrary1

# init the 'GridAxes3DActor' selected for 'AxesGrid'
renderView1.AxesGrid.Visibility = 1
renderView1.AxesGrid.XTitle = 'Lon'
renderView1.AxesGrid.YTitle = 'Lat'
renderView1.AxesGrid.XTitleColor = [0.0, 0.0, 0.0]
renderView1.AxesGrid.XTitleFontFile = ''
renderView1.AxesGrid.YTitleColor = [0.0, 0.0, 0.0]
renderView1.AxesGrid.YTitleFontFile = ''
renderView1.AxesGrid.ZTitleColor = [0.0, 0.0, 0.0]
renderView1.AxesGrid.ZTitleFontFile = ''
renderView1.AxesGrid.GridColor = [0.0, 0.0, 0.0]
renderView1.AxesGrid.ShowGrid = 1
renderView1.AxesGrid.XLabelColor = [0.0, 0.0, 0.0]
renderView1.AxesGrid.XLabelFontFile = ''
renderView1.AxesGrid.YLabelColor = [0.0, 0.0, 0.0]
renderView1.AxesGrid.YLabelFontFile = ''
renderView1.AxesGrid.ZLabelColor = [0.0, 0.0, 0.0]
renderView1.AxesGrid.ZLabelFontFile = ''
renderView1.AxesGrid.DataBoundsScaleFactor = 1.0

# ----------------------------------------------------------------
# restore active view
SetActiveView(renderView1)
# ----------------------------------------------------------------

# ----------------------------------------------------------------
# setup the data processing pipelines
# ----------------------------------------------------------------

# create a new 'PNG Series Reader'
worldtopobathy2004093x5400x2700png = PNGSeriesReader(FileNames=['C:\\Users\\RBC_workhorse\\Documents\\GitHub\\MOHID_PP_sessions\\Paraview\\world.topo.bathy.200409.3x5400x2700.png'])

# ----------------------------------------------------------------
# setup the visualization in view 'renderView1'
# ----------------------------------------------------------------

# show data from worldtopobathy2004093x5400x2700png
worldtopobathy2004093x5400x2700pngDisplay = Show(worldtopobathy2004093x5400x2700png, renderView1)

# get color transfer function/color map for 'PNGImage'
pNGImageLUT = GetColorTransferFunction('PNGImage')
pNGImageLUT.RGBPoints = [0.0, 0.141176, 0.14902, 0.2, 22.083647796503186, 0.215686, 0.258824, 0.321569, 44.16729559300637, 0.243137, 0.368627, 0.380392, 66.25094338950956, 0.27451, 0.439216, 0.4, 88.33459118601274, 0.32549, 0.501961, 0.384314, 110.41823898251593, 0.403922, 0.6, 0.419608, 132.50188677901912, 0.486275, 0.701961, 0.454902, 154.5855345755223, 0.556863, 0.74902, 0.494118, 176.6691823720255, 0.670588, 0.8, 0.545098, 220.83647796503186, 0.854902, 0.901961, 0.631373, 242.92012576153508, 0.92549, 0.941176, 0.694118, 265.00377355803823, 0.960784, 0.94902, 0.776471, 287.08742135454145, 0.988235, 0.968627, 0.909804, 309.1710691510446, 0.839216, 0.815686, 0.772549, 331.25471694754776, 0.701961, 0.662745, 0.615686, 353.338364744051, 0.6, 0.529412, 0.478431, 375.42201254055414, 0.501961, 0.403922, 0.360784, 397.50566033705735, 0.439216, 0.313725, 0.290196, 441.6729559300637, 0.301961, 0.164706, 0.176471]
pNGImageLUT.ColorSpace = 'Lab'
pNGImageLUT.NanColor = [0.25, 0.0, 0.0]
pNGImageLUT.ScalarRangeInitialized = 1.0

# get opacity transfer function/opacity map for 'PNGImage'
pNGImagePWF = GetOpacityTransferFunction('PNGImage')
pNGImagePWF.Points = [0.0, 0.0, 0.5, 0.0, 441.6729559300637, 1.0, 0.5, 0.0]
pNGImagePWF.ScalarRangeInitialized = 1

# trace defaults for the display properties.
worldtopobathy2004093x5400x2700pngDisplay.Representation = 'Surface'
worldtopobathy2004093x5400x2700pngDisplay.AmbientColor = [0.0, 0.0, 0.0]
worldtopobathy2004093x5400x2700pngDisplay.ColorArrayName = ['POINTS', 'PNGImage']
worldtopobathy2004093x5400x2700pngDisplay.LookupTable = pNGImageLUT
worldtopobathy2004093x5400x2700pngDisplay.Position = [-180.0, 90.0, 0.0]
worldtopobathy2004093x5400x2700pngDisplay.Scale = [0.0666666, -0.0666666, 1.0]
worldtopobathy2004093x5400x2700pngDisplay.OSPRayScaleArray = 'PNGImage'
worldtopobathy2004093x5400x2700pngDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
worldtopobathy2004093x5400x2700pngDisplay.SelectOrientationVectors = 'None'
worldtopobathy2004093x5400x2700pngDisplay.ScaleFactor = 539.9
worldtopobathy2004093x5400x2700pngDisplay.SelectScaleArray = 'PNGImage'
worldtopobathy2004093x5400x2700pngDisplay.GlyphType = 'Arrow'
worldtopobathy2004093x5400x2700pngDisplay.GlyphTableIndexArray = 'PNGImage'
worldtopobathy2004093x5400x2700pngDisplay.GaussianRadius = 26.995
worldtopobathy2004093x5400x2700pngDisplay.SetScaleArray = ['POINTS', 'PNGImage']
worldtopobathy2004093x5400x2700pngDisplay.ScaleTransferFunction = 'PiecewiseFunction'
worldtopobathy2004093x5400x2700pngDisplay.OpacityArray = ['POINTS', 'PNGImage']
worldtopobathy2004093x5400x2700pngDisplay.OpacityTransferFunction = 'PiecewiseFunction'
worldtopobathy2004093x5400x2700pngDisplay.DataAxesGrid = 'GridAxesRepresentation'
worldtopobathy2004093x5400x2700pngDisplay.SelectionCellLabelFontFile = ''
worldtopobathy2004093x5400x2700pngDisplay.SelectionPointLabelFontFile = ''
worldtopobathy2004093x5400x2700pngDisplay.PolarAxes = 'PolarAxesRepresentation'
worldtopobathy2004093x5400x2700pngDisplay.ScalarOpacityUnitDistance = 24.71231946253772
worldtopobathy2004093x5400x2700pngDisplay.ScalarOpacityFunction = pNGImagePWF
worldtopobathy2004093x5400x2700pngDisplay.IsosurfaceValues = [127.5]

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
worldtopobathy2004093x5400x2700pngDisplay.ScaleTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 255.0, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
worldtopobathy2004093x5400x2700pngDisplay.OpacityTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 255.0, 1.0, 0.5, 0.0]

# init the 'GridAxesRepresentation' selected for 'DataAxesGrid'
worldtopobathy2004093x5400x2700pngDisplay.DataAxesGrid.XTitleColor = [0.0, 0.0, 0.0]
worldtopobathy2004093x5400x2700pngDisplay.DataAxesGrid.XTitleFontFile = ''
worldtopobathy2004093x5400x2700pngDisplay.DataAxesGrid.YTitleColor = [0.0, 0.0, 0.0]
worldtopobathy2004093x5400x2700pngDisplay.DataAxesGrid.YTitleFontFile = ''
worldtopobathy2004093x5400x2700pngDisplay.DataAxesGrid.ZTitleColor = [0.0, 0.0, 0.0]
worldtopobathy2004093x5400x2700pngDisplay.DataAxesGrid.ZTitleFontFile = ''
worldtopobathy2004093x5400x2700pngDisplay.DataAxesGrid.GridColor = [0.0, 0.0, 0.0]
worldtopobathy2004093x5400x2700pngDisplay.DataAxesGrid.XLabelColor = [0.0, 0.0, 0.0]
worldtopobathy2004093x5400x2700pngDisplay.DataAxesGrid.XLabelFontFile = ''
worldtopobathy2004093x5400x2700pngDisplay.DataAxesGrid.YLabelColor = [0.0, 0.0, 0.0]
worldtopobathy2004093x5400x2700pngDisplay.DataAxesGrid.YLabelFontFile = ''
worldtopobathy2004093x5400x2700pngDisplay.DataAxesGrid.ZLabelColor = [0.0, 0.0, 0.0]
worldtopobathy2004093x5400x2700pngDisplay.DataAxesGrid.ZLabelFontFile = ''

# init the 'PolarAxesRepresentation' selected for 'PolarAxes'
worldtopobathy2004093x5400x2700pngDisplay.PolarAxes.Translation = [-180.0, 90.0, 0.0]
worldtopobathy2004093x5400x2700pngDisplay.PolarAxes.Scale = [0.0666666, -0.0666666, 1.0]
worldtopobathy2004093x5400x2700pngDisplay.PolarAxes.PolarAxisTitleColor = [0.0, 0.0, 0.0]
worldtopobathy2004093x5400x2700pngDisplay.PolarAxes.PolarAxisTitleFontFile = ''
worldtopobathy2004093x5400x2700pngDisplay.PolarAxes.PolarAxisLabelColor = [0.0, 0.0, 0.0]
worldtopobathy2004093x5400x2700pngDisplay.PolarAxes.PolarAxisLabelFontFile = ''
worldtopobathy2004093x5400x2700pngDisplay.PolarAxes.LastRadialAxisTextColor = [0.0, 0.0, 0.0]
worldtopobathy2004093x5400x2700pngDisplay.PolarAxes.LastRadialAxisTextFontFile = ''
worldtopobathy2004093x5400x2700pngDisplay.PolarAxes.SecondaryRadialAxesTextColor = [0.0, 0.0, 0.0]
worldtopobathy2004093x5400x2700pngDisplay.PolarAxes.SecondaryRadialAxesTextFontFile = ''

# setup the color legend parameters for each legend in this view

# get color transfer function/color map for 'velocity'
velocityLUT = GetColorTransferFunction('velocity')
velocityLUT.RGBPoints = [0.0, 0.231373, 0.298039, 0.752941, 1.1224415376095425, 0.865003, 0.865003, 0.865003, 2.244883075219085, 0.705882, 0.0156863, 0.14902]
velocityLUT.ScalarRangeInitialized = 1.0

# get color legend/bar for velocityLUT in view renderView1
velocityLUTColorBar = GetScalarBar(velocityLUT, renderView1)
velocityLUTColorBar.Title = 'velocity'
velocityLUTColorBar.ComponentTitle = 'Magnitude'
velocityLUTColorBar.TitleColor = [0.0, 0.0, 0.0]
velocityLUTColorBar.TitleFontFile = ''
velocityLUTColorBar.LabelColor = [0.0, 0.0, 0.0]
velocityLUTColorBar.LabelFontFile = ''

# set color bar visibility
velocityLUTColorBar.Visibility = 0

# get color legend/bar for pNGImageLUT in view renderView1
pNGImageLUTColorBar = GetScalarBar(pNGImageLUT, renderView1)
pNGImageLUTColorBar.WindowLocation = 'UpperRightCorner'
pNGImageLUTColorBar.Title = 'PNGImage'
pNGImageLUTColorBar.ComponentTitle = 'Magnitude'
pNGImageLUTColorBar.TitleColor = [0.0, 0.0, 0.0]
pNGImageLUTColorBar.TitleFontFile = ''
pNGImageLUTColorBar.LabelColor = [0.0, 0.0, 0.0]
pNGImageLUTColorBar.LabelFontFile = ''

# set color bar visibility
pNGImageLUTColorBar.Visibility = 0

# ----------------------------------------------------------------
# setup color maps and opacity mapes used in the visualization
# note: the Get..() functions create a new object, if needed
# ----------------------------------------------------------------

# get opacity transfer function/opacity map for 'velocity'
velocityPWF = GetOpacityTransferFunction('velocity')
velocityPWF.Points = [0.0, 0.0, 0.5, 0.0, 2.244883075219085, 1.0, 0.5, 0.0]
velocityPWF.ScalarRangeInitialized = 1

# ----------------------------------------------------------------
# finally, restore active source
SetActiveSource(worldtopobathy2004093x5400x2700png)
# ----------------------------------------------------------------