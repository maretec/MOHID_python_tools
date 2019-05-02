#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()
# find source
source = GetActiveSource()
# create a new 'Programmable Filter'
programmableFilter1 = ProgrammableFilter(Input=source)
programmableFilter1.RequestInformationScript = ''
programmableFilter1.RequestUpdateExtentScript = ''
programmableFilter1.PythonPath = ""
# Properties modified on programmableFilter1
programmableFilter1.OutputDataSetType = 'vtkTable'

programmableFilter1.Script = '\
import sys\n\
import os\n\
basePath = os.path.dirname(os.path.realpath("__file__"))\n\
commonPath = os.path.abspath(os.path.join(basePath,"..","Common"))\n\
sys.path.append(commonPath)\n\
import MDateTime as mdate\n\
t = inputs[0].GetInformation().Get(vtk.vtkDataObject.DATA_TIME_STEP())\n\
date_time = mdate.getDateStringFromTimeStamp(t)\n\
outputarray = vtk.vtkStringArray()\n\
outputarray.SetName("datetime")\n\
outputarray.SetNumberOfTuples(1)\n\
outputarray.SetValue(0, "{}".format(date_time))\n\
print("{} -> {}".format(t, date_time))\n\
output.RowData.AddArray(outputarray)'

# find view
renderView1 = GetActiveView()
# create a new 'Python Annotation'
pythonAnnotation1 = PythonAnnotation(Input=programmableFilter1)
# Properties modified on pythonAnnotation1
pythonAnnotation1.ArrayAssociation = 'Row Data'
pythonAnnotation1.Expression ='"{}".format(input.RowData["datetime"].GetValue(0))'
# show data in view
pythonAnnotation1Display = Show(pythonAnnotation1, renderView1)
# update the view to ensure updated data information
renderView1.Update()