# -*- coding: utf-8 -*-

class MXDMFwriter:
    def __init__(self, filename, directory):
        self.filename = filename
        self.directory = directory
        self.f = open(self.directory +'/'+ self.filename + '.xdmf', 'w')
        
    def writeHeader(self):
        self.f.write('''<?xml version="1.0" ?>
<!DOCTYPE Xdmf SYSTEM "Xdmf.dtd" []>
<Xdmf Version="2.0">
    <Domain>
        <Grid Name="Box" GridType="Collection" CollectionType="Temporal">
''')
        
    def closeFile(self):
        self.f.write('''        </Grid>
    </Domain>
</Xdmf>
''')
        self.f.close()
        
    def openGrid(self,gridName):
        self.f.write('''            <Grid Name="'''+gridName+'''" GridType="Uniform">
''')
        
    def closeGrid(self):
        self.f.write('''            </Grid>
''')
         
    def writeGeo(self,fileType,timeIndex,date,geoDims):
        timeIndexStr = str(timeIndex).zfill(5)
        if fileType != 'Lagrangian':
            geoDimsStr = ' '.join(str(e) for e in geoDims)
            toWrite = '''                <Topology TopologyType="3DSMesh" Dimensions="'''+geoDimsStr+'''"/>">
                <Time Value="'''+str(date)+'''" />
                <Geometry GeometryType="X_Y_Z">
                    <DataItem Dimensions="'''+geoDimsStr+'''" NumberType="Float" Precision="8" Format="HDF">
                        '''+self.filename+'''.hdf5:/Grid/Corners3D/Longitude
                    </DataItem>
                    <DataItem Dimensions="'''+geoDimsStr+'''" NumberType="Float" Precision="8" Format="HDF">
                        '''+self.filename+'''.hdf5:/Grid/Corners3D/Latitude
                    </DataItem>
                    <DataItem Dimensions="'''+geoDimsStr+'''" NumberType="Float" Precision="8" Format="HDF">
                        '''+self.filename+'''.hdf5:/Grid/Corners3D/Vertical
                    </DataItem>
                </Geometry>
'''
        if fileType == 'Lagrangian':
            geoDimsStr = str(geoDims)
            toWrite = '''                <Topology TopologyType="Polyvertex" Dimensions="'''+geoDimsStr+'''"/>
                <Time Value="'''+str(date)+'''" />
                <Geometry GeometryType="X_Y_Z">
                    <DataItem Dimensions="'''+geoDimsStr+'''" NumberType="Float" Precision="8" Format="HDF">
                        '''+self.filename+'''.hdf5:/Results/Group_1/Data_1D/Longitude/Longitude_'''+timeIndexStr+'''
                    </DataItem>
                    <DataItem Dimensions="'''+geoDimsStr+'''" NumberType="Float" Precision="8" Format="HDF">
                        '''+self.filename+'''.hdf5:/Results/Group_1/Data_1D/Latitude/Latitude_'''+timeIndexStr+'''
                    </DataItem>
                    <DataItem Dimensions="'''+geoDimsStr+'''" NumberType="Float" Precision="8" Format="HDF">
                        '''+self.filename+'''.hdf5:/Results/Group_1/Data_1D/Z Pos/Z Position_'''+timeIndexStr+'''
                    </DataItem>
                </Geometry>
'''
        self.f.write(toWrite)
        
    def writeAttribute(self,fileType,attr,geoDims):
        attrName = attr[0]
        attrPath = attr[1]
        if fileType != 'Lagrangian':
            geoDimsStr = ' '.join(str(e) for e in geoDims)
        else:
            geoDimsStr = str(geoDims)
        toWrite = '''                <Attribute Name="'''+attrName+'''" AttributeType="Scalar" Center="Cell">
                    <DataItem Dimensions="'''+geoDimsStr+'''" NumberType="Float" Precision="8" Format="HDF">
                        '''+self.filename+'''.hdf5:'''+attrPath+'''
                    </DataItem>
                </Attribute>
'''
        self.f.write(toWrite)
        
