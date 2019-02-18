# Get_Boys.py

Created by : Jorge Palma and Ligia Pinto
Edited by  : Mariangel Garcia 

Last Update: 02-18-2019

## Get_Boys.py
- Donwload time series daily and monthly  insitu data from ftp server nrt.cmems-du.eu in netcdf format.
	- Built for operational use
	- Read selected ocean buoys from jason files
	- Run program by passing arguments such a starting dates, end dates, station ID, monthly or daily data, location of output directory, username and password
    - .barc
		
### How to use this code:

#### From Command Arguments
Inside the run folders there is a two .bash that runs for windows:
 - run.bat          : Is meant to run in operational mode. It will look for the current date and donwload data for the last 3 days
 - run_one_time.bat : Donwload data for specific dates, could be from the daily folder or montlhy directory


## REQUIREMENT 
- You must have an account on nrt.cmems-du.eu to be able to donwload this data

