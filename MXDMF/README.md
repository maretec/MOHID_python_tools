# MXDMF 

MXDMF creates a light-data .xdmf metadata indexer of .hdf5 heavy-data files written by MOHID. This allows for MOHID hdf5 data to be read and manipulated using Paraview, Visit, etc.

    - Use the run file to point at a directory containing either .hdf5 files or subdirectories with them

    - A .xdmf file will be created next to each valid .hdf5 file (if Eulerian file, it must have a Grid/Corners3D/(lat,lon,z) group (MOHID update 2/1/2019)
    
    - Glue made easy, just use the glue option (see the run scripts) and a master indexer file will be created, that points to the correct parts of the correct files in the correct order for postprocessing tools to access. No more copying heavy data.

    - TODO:
        - Generalize for more Eulerian files (should work, but not tested)
        - Get Eulerian fields from Lagrangian files
