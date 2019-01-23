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
renderView1.ViewSize = [2218, 852]
renderView1.AnnotationColor = [0.0, 0.0, 0.0]
renderView1.AxesGrid = 'GridAxes3DActor'
renderView1.OrientationAxesVisibility = 0
renderView1.OrientationAxesLabelColor = [0.0, 0.0, 0.0]
renderView1.OrientationAxesOutlineColor = [0.0, 0.0, 0.0]
renderView1.CenterOfRotation = [-8.879999999999999, 39.660000000000004, -1.3369729375]
renderView1.StereoType = 0
renderView1.CameraPosition = [-8.879999999999999, 39.660000000000004, 24.147973827377296]
renderView1.CameraFocalPoint = [-8.879999999999999, 39.660000000000004, -1.3369729375]
renderView1.CameraParallelScale = 6.595989586174117
renderView1.Background = [1.0, 1.0, 1.0]
renderView1.OSPRayMaterialLibrary = materialLibrary1

# init the 'GridAxes3DActor' selected for 'AxesGrid'
renderView1.AxesGrid.Visibility = 1
renderView1.AxesGrid.XTitle = 'Longitude'
renderView1.AxesGrid.YTitle = 'Latitude'
renderView1.AxesGrid.ZTitle = 'Depth'
renderView1.AxesGrid.XTitleColor = [0.0, 0.0, 0.0]
renderView1.AxesGrid.XTitleFontFile = ''
renderView1.AxesGrid.XTitleFontSize = 13
renderView1.AxesGrid.YTitleColor = [0.0, 0.0, 0.0]
renderView1.AxesGrid.YTitleFontFile = ''
renderView1.AxesGrid.YTitleFontSize = 13
renderView1.AxesGrid.ZTitleColor = [0.0, 0.0, 0.0]
renderView1.AxesGrid.ZTitleFontFile = ''
renderView1.AxesGrid.ZTitleFontSize = 13
renderView1.AxesGrid.GridColor = [0.0, 0.0, 0.0]
renderView1.AxesGrid.ShowGrid = 1
renderView1.AxesGrid.XLabelColor = [0.0, 0.0, 0.0]
renderView1.AxesGrid.XLabelFontFile = ''
renderView1.AxesGrid.YLabelColor = [0.0, 0.0, 0.0]
renderView1.AxesGrid.YLabelFontFile = ''
renderView1.AxesGrid.ZLabelColor = [0.0, 0.0, 0.0]
renderView1.AxesGrid.ZLabelFontFile = ''

# ----------------------------------------------------------------
# restore active view
SetActiveView(renderView1)
# ----------------------------------------------------------------

# ----------------------------------------------------------------
# setup the data processing pipelines
# ----------------------------------------------------------------

# create a new 'XDMF Reader'
hydrodynamicxdmf = XDMFReader(FileNames=['C:\\Users\\RBC_workhorse\\Documents\\GitHub\\MOHID_python_tools\\MXDMF\\TestFiles_op\\Hydrodynamic.xdmf'])
hydrodynamicxdmf.CellArrayStatus = ['velocity U', 'velocity V', 'velocity W', 'velocity modulus']
hydrodynamicxdmf.GridStatus = ['Solution_00001', 'Solution_00002', 'Solution_00003', 'Solution_00004', 'Solution_00005', 'Solution_00006', 'Solution_00007', 'Solution_00008', 'Solution_00009']

# create a new 'Transform'
vertical_scaling = Transform(Input=hydrodynamicxdmf)
vertical_scaling.Transform = 'Transform'

# init the 'Transform' selected for 'Transform'
vertical_scaling.Transform.Scale = [1.0, 1.0, -0.0005]

# ----------------------------------------------------------------
# setup the visualization in view 'renderView1'
# ----------------------------------------------------------------

# show data from vertical_scaling
vertical_scalingDisplay = Show(vertical_scaling, renderView1)

# get color transfer function/color map for 'velocitymodulus'
velocitymodulusLUT = GetColorTransferFunction('velocitymodulus')
velocitymodulusLUT.RGBPoints = [0.0, 0.231373, 0.298039, 0.752941, 0.6137547492980957, 0.865003, 0.865003, 0.865003, 1.2275094985961914, 0.705882, 0.0156863, 0.14902]
velocitymodulusLUT.ScalarRangeInitialized = 1.0

# get opacity transfer function/opacity map for 'velocitymodulus'
velocitymodulusPWF = GetOpacityTransferFunction('velocitymodulus')
velocitymodulusPWF.Points = [0.0, 0.0, 0.5, 0.0, 1.2275094985961914, 1.0, 0.5, 0.0]
velocitymodulusPWF.ScalarRangeInitialized = 1

# trace defaults for the display properties.
vertical_scalingDisplay.Representation = 'Surface'
vertical_scalingDisplay.AmbientColor = [0.0, 0.0, 0.0]
vertical_scalingDisplay.ColorArrayName = ['CELLS', 'velocity modulus']
vertical_scalingDisplay.LookupTable = velocitymodulusLUT
vertical_scalingDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
vertical_scalingDisplay.SelectOrientationVectors = 'None'
vertical_scalingDisplay.ScaleFactor = 1.0560000000000003
vertical_scalingDisplay.SelectScaleArray = 'None'
vertical_scalingDisplay.GlyphType = 'Arrow'
vertical_scalingDisplay.GlyphTableIndexArray = 'None'
vertical_scalingDisplay.GaussianRadius = 0.052800000000000014
vertical_scalingDisplay.SetScaleArray = [None, '']
vertical_scalingDisplay.ScaleTransferFunction = 'PiecewiseFunction'
vertical_scalingDisplay.OpacityArray = [None, '']
vertical_scalingDisplay.OpacityTransferFunction = 'PiecewiseFunction'
vertical_scalingDisplay.DataAxesGrid = 'GridAxesRepresentation'
vertical_scalingDisplay.SelectionCellLabelFontFile = ''
vertical_scalingDisplay.SelectionPointLabelFontFile = ''
vertical_scalingDisplay.PolarAxes = 'PolarAxesRepresentation'
vertical_scalingDisplay.ScalarOpacityFunction = velocitymodulusPWF
vertical_scalingDisplay.ScalarOpacityUnitDistance = 0.12558076935254783

# init the 'GridAxesRepresentation' selected for 'DataAxesGrid'
vertical_scalingDisplay.DataAxesGrid.XTitleColor = [0.0, 0.0, 0.0]
vertical_scalingDisplay.DataAxesGrid.XTitleFontFile = ''
vertical_scalingDisplay.DataAxesGrid.YTitleColor = [0.0, 0.0, 0.0]
vertical_scalingDisplay.DataAxesGrid.YTitleFontFile = ''
vertical_scalingDisplay.DataAxesGrid.ZTitleColor = [0.0, 0.0, 0.0]
vertical_scalingDisplay.DataAxesGrid.ZTitleFontFile = ''
vertical_scalingDisplay.DataAxesGrid.GridColor = [0.0, 0.0, 0.0]
vertical_scalingDisplay.DataAxesGrid.ShowGrid = 1
vertical_scalingDisplay.DataAxesGrid.XLabelColor = [0.0, 0.0, 0.0]
vertical_scalingDisplay.DataAxesGrid.XLabelFontFile = ''
vertical_scalingDisplay.DataAxesGrid.YLabelColor = [0.0, 0.0, 0.0]
vertical_scalingDisplay.DataAxesGrid.YLabelFontFile = ''
vertical_scalingDisplay.DataAxesGrid.ZLabelColor = [0.0, 0.0, 0.0]
vertical_scalingDisplay.DataAxesGrid.ZLabelFontFile = ''

# init the 'PolarAxesRepresentation' selected for 'PolarAxes'
vertical_scalingDisplay.PolarAxes.PolarAxisTitleColor = [0.0, 0.0, 0.0]
vertical_scalingDisplay.PolarAxes.PolarAxisTitleFontFile = ''
vertical_scalingDisplay.PolarAxes.PolarAxisLabelColor = [0.0, 0.0, 0.0]
vertical_scalingDisplay.PolarAxes.PolarAxisLabelFontFile = ''
vertical_scalingDisplay.PolarAxes.LastRadialAxisTextColor = [0.0, 0.0, 0.0]
vertical_scalingDisplay.PolarAxes.LastRadialAxisTextFontFile = ''
vertical_scalingDisplay.PolarAxes.SecondaryRadialAxesTextColor = [0.0, 0.0, 0.0]
vertical_scalingDisplay.PolarAxes.SecondaryRadialAxesTextFontFile = ''

# setup the color legend parameters for each legend in this view

# get color legend/bar for velocitymodulusLUT in view renderView1
velocitymodulusLUTColorBar = GetScalarBar(velocitymodulusLUT, renderView1)
velocitymodulusLUTColorBar.Title = 'velocity modulus'
velocitymodulusLUTColorBar.ComponentTitle = ''
velocitymodulusLUTColorBar.TitleColor = [0.0, 0.0, 0.0]
velocitymodulusLUTColorBar.TitleFontFile = ''
velocitymodulusLUTColorBar.LabelColor = [0.0, 0.0, 0.0]
velocitymodulusLUTColorBar.LabelFontFile = ''

# set color bar visibility
velocitymodulusLUTColorBar.Visibility = 1

# show color legend
vertical_scalingDisplay.SetScalarBarVisibility(renderView1, True)

# ----------------------------------------------------------------
# setup color maps and opacity mapes used in the visualization
# note: the Get..() functions create a new object, if needed
# ----------------------------------------------------------------

# ----------------------------------------------------------------
# finally, restore active source
SetActiveSource(vertical_scaling)
# ----------------------------------------------------------------