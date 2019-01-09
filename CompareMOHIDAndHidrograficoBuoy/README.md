# CompareMohidAndHidrograficoBuoy

	Author - Alexandre Correia
	Purpose - Read temperature from MOHID timeseries and Hidrografico buoy timeseries from operational
	MOHID datasource to perform statistical comparisons. It calculates the Pearson Correlation, RMSE,
bias and plots the regression and timeseries of the 2 datasources.
Specifics - 

## REQUIREMENTS
INPUT: - path of the folder which contains the day folders (i.e. YYYY-MM-DD_YYYY-MM-DD), must end with '/' or '\\'
       - name of the MOHID timeserie inside of day folders to be read by the script
       - path of the buoy timeserie
       - start and end date in the format YYYY-MM-DD
