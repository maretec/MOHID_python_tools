@echo off

set output=.

rem python GetBouys.py -d %output% -strd 20190101 -endd 20190102 -u fcampuzano -p RAkopeci

rem python GetBouys.py -d %output% -strm 201901 -endm 201902 

python GetBouys.py -d %output% -f datetime.dat -t -u fcampuzano -p RAkopeci

cmd