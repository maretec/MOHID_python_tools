# -*- coding: utf-8 -*-

#    !------------------------------------------------------------------------------
#    !        IST/MARETEC, Water Modelling Group, Mohid modelling system
#    !------------------------------------------------------------------------------
#    !
#    ! TITLE         : MXDMF_writer
#    ! PROJECT       : Mohid python tools
#    ! MODULE        : background
#    ! URL           : http://www.mohid.com
#    ! AFFILIATION   : IST/MARETEC, Marine Modelling Group
#    ! DATE          : January 2019
#    ! REVISION      : Canelas 0.1
#    !> @author
#    !> Ricardo Birjukovs Canelas
#    !
#    ! DESCRIPTION:
#    !Class that describes methods to write an xdmf file from MOHID output. 
#    !Hardcoded paths, and other weird assumptions are to be expected
#    !------------------------------------------------------------------------------
#    
#    MIT License
#    
#    Copyright (c) 2018 RBCanelas
#    
#    Permission is hereby granted, free of charge, to any person obtaining a copy
#    of this software and associated documentation files (the "Software"), to deal
#    in the Software without restriction, including without limitation the rights
#    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#    copies of the Software, and to permit persons to whom the Software is
#    furnished to do so, subject to the following conditions:
#    
#    The above copyright notice and this permission notice shall be included in all
#    copies or substantial portions of the Software.
#    
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#    SOFTWARE.

class MXDMFwriter:
    def __init__(self):
        self.filename = []
        self.directory = []
        
    def openFile(self, filename, directory):
        self.filename = filename
        self.directory = directory
        self.f = open(self.directory +'/'+ self.filename + '.xdmf', 'w')
        self.writeHeader()
    
    def closeFile(self):
        self.f.write('''        </Grid>
    </Domain>
</Xdmf>
''')
        self.f.close()
        
    def writeHeader(self):
        self.f.write('''<?xml version="1.0" ?>
<!DOCTYPE Xdmf SYSTEM "Xdmf.dtd" []>
<Xdmf Version="2.0">
    <Domain>
        <Grid Name="Box" GridType="Collection" CollectionType="Temporal">
''')
        
    def openGrid(self,gridName):
        self.f.write('''            <Grid Name="'''+gridName+'''" GridType="Uniform">
''')
        
    def closeGrid(self):
        self.f.write('''            </Grid>
''')
         
    def writeGeo(self,fileType,timeIndex,timeStamp,dateStr,geoDims,dimensionality, hasCorners3D, LatLon, path = ''):
        timeIndexStr = str(timeIndex).zfill(5)
        coordName = ['Longitude', 'Latitude']
        if not LatLon:
            coordName = ['ConnectionX', 'ConnectionY']
        if fileType != 'Lagrangian':
            geoDimsStr = ' '.join(str(e) for e in geoDims)
            if dimensionality == 2:
                topology = '2DSMesh'
                #if coners3D are available use that
                address = '/Grid'
                if hasCorners3D:
                    dimensionality = 3
                    geoDimsStr = '2 '+geoDimsStr
            if dimensionality == 3:
                topology = '3DSMesh'
                address = '/Grid/Corners3D'
            toWrite = '''                <Topology TopologyType="'''+topology+'''" Dimensions="'''+geoDimsStr+'''"/>">
                <Time Value="'''+str(timeStamp)+'''" /> <!--date: '''+dateStr+'''-->
                <Geometry GeometryType="X_Y">
                    <DataItem Dimensions="'''+geoDimsStr+'''" NumberType="Float" Precision="8" Format="HDF">
                        '''+path+self.filename+'''.hdf5:'''+address+'''/'''+coordName[0]+'''
                    </DataItem>
                    <DataItem Dimensions="'''+geoDimsStr+'''" NumberType="Float" Precision="8" Format="HDF">
                        '''+path+self.filename+'''.hdf5:'''+address+'''/'''+coordName[1]+'''
                    </DataItem>
                </Geometry>
'''
            if dimensionality == 3:
                toWrite = '''                <Topology TopologyType="3DSMesh" Dimensions="'''+geoDimsStr+'''"/>">
                <Time Value="'''+str(timeStamp)+'''" /> <!--date: '''+dateStr+'''-->
                <Geometry GeometryType="X_Y_Z">
                    <DataItem Dimensions="'''+geoDimsStr+'''" NumberType="Float" Precision="8" Format="HDF">
                        '''+path+self.filename+'''.hdf5:/Grid/Corners3D/'''+coordName[0]+'''
                    </DataItem>
                    <DataItem Dimensions="'''+geoDimsStr+'''" NumberType="Float" Precision="8" Format="HDF">
                        '''+path+self.filename+'''.hdf5:/Grid/Corners3D/'''+coordName[1]+'''
                    </DataItem>
                    <DataItem Dimensions="'''+geoDimsStr+'''" NumberType="Float" Precision="8" Format="HDF">
                        '''+path+self.filename+'''.hdf5:/Grid/Corners3D/Vertical
                    </DataItem>
                </Geometry>
'''
        if fileType == 'Lagrangian':
            geoDimsStr = str(geoDims)
            toWrite = '''                <Topology TopologyType="Polyvertex" Dimensions="'''+geoDimsStr+'''"/>
                <Time Value="'''+str(timeStamp)+'''" /> <!--date: '''+dateStr+'''-->
                <Geometry GeometryType="X_Y_Z">
                    <DataItem Dimensions="'''+geoDimsStr+'''" NumberType="Float" Precision="8" Format="HDF">
                        '''+path+self.filename+'''.hdf5:/Results/Group_1/Data_1D/Longitude/Longitude_'''+timeIndexStr+'''
                    </DataItem>
                    <DataItem Dimensions="'''+geoDimsStr+'''" NumberType="Float" Precision="8" Format="HDF">
                        '''+path+self.filename+'''.hdf5:/Results/Group_1/Data_1D/Latitude/Latitude_'''+timeIndexStr+'''
                    </DataItem>
                    <DataItem Dimensions="'''+geoDimsStr+'''" NumberType="Float" Precision="8" Format="HDF">
                        '''+path+self.filename+'''.hdf5:/Results/Group_1/Data_1D/Z Pos/Z Position_'''+timeIndexStr+'''
                    </DataItem>
                </Geometry>
'''
        self.f.write(toWrite)
        
    def writeAttribute(self,fileType,attr,geoDims,dimensionality, hasCorners3D, path = ''):
        attrName = attr[0]
        attrPath = attr[1]        
        if fileType != 'Lagrangian':
            meshDims = []
            if dimensionality == 3:
                meshDims = geoDims[0]-1, geoDims[1], geoDims[2]
            if dimensionality == 2:
                meshDims[:] = [x - 1 for x in geoDims]
                
            geoDimsStr = ' '.join(str(e) for e in meshDims)
        else:
            geoDimsStr = str(geoDims)
            
        if dimensionality == 2:
            if hasCorners3D:
                geoDimsStr = geoDimsStr +' 1'
                
        toWrite = '''                <Attribute Name="'''+attrName+'''" AttributeType="Scalar" Center="Cell">
                    <DataItem Dimensions="'''+geoDimsStr+'''" NumberType="Float" Precision="8" Format="HDF">
                        '''+path+self.filename+'''.hdf5:'''+attrPath+'''
                    </DataItem>
                </Attribute>
'''
        self.f.write(toWrite)
        
