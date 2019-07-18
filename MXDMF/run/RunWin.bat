@echo off
cls

rem IF YOU ARE USING ANACONDA, OPEN A CMD LINE, TYPE 'ACTIVATE BASE' AND THEN RUN THIS BATCH THERE


rem "dataDir" is named according to the testcase ----- CHANGE THIS HERE --------
set dataDir=../TestFiles_op

rem "executables" are renamed and called from their directory
set src=../src
set MXDMF="%src%/MXDMF_run.py"

rem CODES are executed according the selected parameters of execution in this case
python %MXDMF% -i %dataDir% -g true
rem python %MXDMF% -i %dataDir% -f true
rem python %MXDMF% -i %dataDir% -g true
rem python %MXDMF% -i %dataDir% -g true -fd "2000-08-19 01:01:35"
rem python %MXDMF% -i %dataDir% -g true -fd "2000-08-19 01:01:35" -ld "2000-08-20 00:00:00"
if not "%ERRORLEVEL%" == "0" goto fail

:success
echo All done
goto end

:fail
echo Execution aborted.

:end
pause