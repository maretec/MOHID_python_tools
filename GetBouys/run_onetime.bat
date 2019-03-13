@echo off
rem set output direcory
set output=.

remp python GetBouys.py -d %output% -strd 20190101 -endd 20190129 -t -u {your_username} -p {your_password}

rem python GetBouys.py -d %output% -strm 201901 -endm 201902 -t -u {your_username} -p {your_password}
rem python GetBouys.py -d %output% -strm 201901 -endm 201902 -t -u {your_username} -p {your_password}

python GetBouys.py -d %output% -f datetime.dat -t -u {your_username} -p {your_password}


cmd