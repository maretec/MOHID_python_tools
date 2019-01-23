@echo off
cls

rem "dataDir" is named according to the testcase ----- CHANGE THIS HERE --------
set dataDir=C:\\YourHDF5Directory

rem "executables" are renamed and called from their directory
set src=../src
set MXDMF="%src%/MXDMF_run.py"

rem CODES are executed according the selected parameters of execution in this case
python %MXDMF% %dataDir%
rem python %MXDMF% %dataDir% glue
if not "%ERRORLEVEL%" == "0" goto fail

:success
echo All done
goto end

:fail
echo Execution aborted.

:end
pause