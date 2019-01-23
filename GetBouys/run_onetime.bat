@echo off

set output=\\DAVINCI\DataCenter\DadosBase\Oceanografia\Fixed_Stations

python GetBouys.py -d %output% -t -strm 201901 -endm 201901



cmd