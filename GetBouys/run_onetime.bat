@echo off

set output=.

python GetBouys.py -d %output% -strd 20190101 -endd 20190129 -u {your_username} -p {your_password}

rem python GetBouys.py -d %output% -strm 201901 -endm 201902 


cmd