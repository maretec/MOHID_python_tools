#!/bin/bash

clear

# "dataDir" is named according to the testcase ----- CHANGE THIS HERE --------
dataDir=../TestFiles

# "executables" are renamed and called from their directory
src=../src
MXDMF=${src}/MXDMF_run.py

# CODES are executed according the selected parameters of execution in this testcase
errcode=0
if [ $errcode -eq 0 ]; then
  python $MXDMF -i $dataDir
  #python $MXDMF -i $dataDir -g true
  # python $MXDMF -i $dataDir -g true -fd "2000-08-19 01:01:35"
  # python $MXDMF -i $dataDir -g true -fd "2000-08-19 01:01:35" -ld "2000-08-20 00:00:00"
  errcode=$?
fi

if [ $errcode -eq 0 ]; then
  echo All done
else
  echo Execution aborted
fi
read -n1 -r -p "Press any key to continue..." key
echo