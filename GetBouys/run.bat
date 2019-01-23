@echo off

set output=\\DAVINCI\DataCenter\DadosBase\Oceanografia\Fixed_Stations

: ====daily
python GetBouys.py -d  %output% -t > daily.log 2>&1

: ====monthly
for /f "skip=8 tokens=2,3,4,5,6,7,8 delims=: " %%D in ('robocopy /l * \ \ /ns /nc /ndl /nfl /np /njh /XF * /XD *') do (
  set "year=%%J"
  set "month=%%E"
  set "day=%%F"
  set "dow=%%D"
  set "HH=%%G"
  set "MM=%%H"
  set "SS=%%I"
)
if %day%==01 python GetBouys.py -m -d %output% -t > monthly.log 2>&1

