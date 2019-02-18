@echo off

set output=\\DAVINCI\DataCenter\DadosBase\Oceanografia\Fixed_Stations

python ..\GetBouys.py -d %output% -strd 20190101 -endd 20190129

rem python ..\GetBouys.py -d %output% -strm 201901 -endm 201902 


cmd