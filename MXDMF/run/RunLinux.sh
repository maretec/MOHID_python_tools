#!/bin/bash

clear

# "dataDir" is named according to the testcase ----- CHANGE THIS HERE --------
# dataDir=/Users/rbc-laptop/Documents/GitHub/MOHID_python_tools/MXDMF/TestFiles
dataDir=/Users/rbc-laptop/Desktop/TestFiles

# "executables" are renamed and called from their directory
src=../src
MXDMF=${src}/MXDMF_run.py

# CODES are executed according the selected parameters of execution in this testcase
errcode=0
if [ $errcode -eq 0 ]; then
  #python $MXDMF $dataDir glue
  python $MXDMF $dataDir
  errcode=$?
fi

if [ $errcode -eq 0 ]; then
  echo All done
else
  echo Execution aborted
fi
read -n1 -r -p "Press any key to continue..." key
echo