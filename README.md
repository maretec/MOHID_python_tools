# MOHID_python_tools
Repository of post and pre-processing tools for MOHID written using python 

Common - Python modules common to most tools. Directory manipulation, math functions, etc.

HDF5toNetCDF - converts hydrodynamic and Lagrangian MOHID output files (HDF5) to NetCDF and csv, respectively. 
    - The NetCDF files are 2D, only the bathymetry and surface layer are written at the moment.
    - The files are created as a stream, one file per time step.
    - The converter was built around the outputs of operational outputs, so a master directory is expected, where the subdirectories contain the .hdf5 files for a given interval. 
    - The converter is date sensitive, so it will disregard repeated time instants.

MXDMF - creates a light-data .xdmf metadata indexer of .hdf5 heavy-data files written by MOHID. This allows for MOHID hdf5 data to be read and manipulated using Paraview, Visit, etc.
    - Use the run file to point at a directory containing either .hdf5 files or subdirectories with them
    - A .xdmf file will be created next to each valid .hdf5 file (if Eulerian file, it must have a Grid/Corners3D/(lat,lon,z) group (MOHID update 2/1/2019)
    - TODO:
        - Generalize for more Eulerian files (should work, but not tested)
        - Get Eulerian fields from Lagrangian files
        - Implement date-awareness
        - Option to write a global file, indexing every time-step of a colection of files. This effectivelly bypasses the glue operations and should be very useful for operational-style runs.
