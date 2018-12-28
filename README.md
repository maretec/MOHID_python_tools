# MOHID_python_tools
Repository of post and pre-processing tools for MOHID written using python 

HDF5toNetCDF - converts hydrodynamic and Lagrangian MOHID output files (HDF5) to NetCDF and csv, respectively. 
    - The NetCDF files are 2D, only the bathymetry and surface layer are written at the moment.
    - The files are created as a stream, one file per time step.
    - The converter was built around the outputs of operational outputs, so a master directory is expected, where the subdirectories contain the .hdf5 files for a given interval. 
    - The converter is date sensitive, so it will disregard repeated time instants.

MXDMF - creates a light data .xdmf metadata description of .hdf5 heavy data files written by MOHID. WIP. 
