# -*- coding: utf-8 -*-

import numpy as np


class MXDMFwriter:
    def __init__(self, filename, directory):
        self.filename = filename
        self.directory = directory
        self.f = []
        
    def openfile(self):
        self.f = open(self.directory +'/'+ self.filename + '.xdmf', 'w')
        
    def writeheader(self):
        self.f.write('''<?xml version="1.0" ?>
<!DOCTYPE Xdmf SYSTEM "Xdmf.dtd" []>
<Xdmf Version="2.0">
    <Domain>
        <Grid Name="Box" GridType="Collection" CollectionType="Temporal">
''')
        
        

filename = 'Name_of_h5.xmf'
f = open(filename, 'w')

# defining the grid
Nx,Ny,Nz =64, 64, 64

# Total time steps
tEnd = 5000

# Data dumping step
nOutput = 10

# Not taking initial points
waittime = 3400

filename = 'Name_of_h5.xmf'
f = open(filename, 'w')

# Header for xml file
f.write('''<?xml version="1.0" ?>
<!DOCTYPE Xdmf SYSTEM "Xdmf.dtd" []>
<Xdmf Version="2.0">
<Domain>
<Grid Name="Box" GridType="Collection" CollectionType="Temporal">
''')

# loop over the attributes name written using time
t = 0
frameN = 0 # For time sequence 
while t <= tEnd :
    t = t + 1; 
    if( np.mod(t, nOutput) == 0):

        # Naming datasets 
        dataSetName1 = 'Name_of_h5.h5:/S_%.8d'%(t)
        dataSetName2 = 'Name_of_h5.h5:/V_%.8d'%(t)

        # at individual time write the time independent Box grid. is it overdoing?
        f.write('''
        <!-- time step -->
        <Grid Name="Box %d" GridType="Uniform"> # 
        <Topology TopologyType="3DCoRectMesh" Dimensions="%d %d %d"/>
        <Geometry GeometryType="ORIGIN_DXDYDZ">
           <DataItem DataType="Float" Dimensions="3" Format="XML">0.0 0.0 0.0</DataItem>
           <DataItem DataType="Float" Dimensions="3" Format="XML">1.0 1.0 1.0</DataItem>
        </Geometry>
        <Time Value="%d" />
        '''%(frameN, Nx, Ny, Nz, frameN))

        # First Attribute
        f.write('''\n
        <Attribute Name="S" AttributeType="Scalar" Center="Node">
        <DataItem Dimensions="%d %d %d" NumberType="Float" Precision="4"
        Format="HDF">%s
        </DataItem>
        </Attribute>
        '''%(Nx, Ny, Nz, dataSetName1))

        # Second Attribute
        f.write('''\n
        <Attribute Name="N" AttributeType="Vector" Center="Node">
        <DataItem Dimensions="%d %d %d 3" NumberType="Float" Precision="4"
        Format="HDF"> %s
        </DataItem>
        </Attribute>
        </Grid>\n'''%(Nx, Ny, Nz, dataSetName2))
        frameN +=1

# End the xmf file
f.write('''
   </Grid>
</Domain>
</Xdmf>
''')