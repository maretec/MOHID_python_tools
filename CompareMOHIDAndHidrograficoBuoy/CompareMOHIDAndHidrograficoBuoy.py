"""
This tool compares the temperature from MOHID timeseries file
with a timeserie file of a 'Instituto Hidrografico' buoy.
"""


import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from datetime import datetime, timedelta
from math import sqrt


### User input needed to run ###################################################
directory_location = '\\\\MWDATA\\Storage02\\Modelos\PCOMS\\PCOMS_MPI\\BIOPCOMSUP_V3\\Portugal\\Results_TimeSeries\\' # directory where the folders of the days are
mohid_timeseries_filename = 'Sines Buoy.srw' # name of the file
buoy_timeseries_filename = '\\\\Mar\\d\\Aplica\\OPValidation\\Buoys\\ReadRSS\\Sines.dat' # name or location/name of the file
start_date = '2016-01-01' # format: YYYY-MM-DD
end_date = '2016-01-02' # format: YYYY-MM-DD
want_plot_correlation = True # True or False
want_plot_timeseries = True # True or False
################################################################################


# Changes starting variables to python datetime format
start_date = datetime.strptime(start_date, '%Y-%m-%d')
end_date = datetime.strptime(end_date, '%Y-%m-%d')


### Functions ##################################################################
def read_buoy_timeseries(start_date, end_date):

    print('Reading buoy timeseries...')

    with open(buoy_timeseries_filename) as f:

        f.readline()    # skips the first line
        for line in f:
            # I found tabs instead of spaces in some lines, this is for
            # replacing them with spaces
            while line.find('\t') > -1:
                i = line.find('\t')
                line = line[:i] + ' ' + line[i+1:]

            line = line.replace('\n','').split(' ')
            line = list(filter(None, line))

            current_date = datetime.strptime(line[0]+' '+line[1], '%Y-%m-%d %H:%M')

            if start_date <= current_date <= end_date:
                try:
                    observed_array = np.append(observed_array, [[current_date, float(line[-1])]], axis=0)
                except NameError:
                    observed_array = [[current_date, float(line[-1])]]
            elif current_date > end_date:
                break
    return observed_array


def read_mohid_timeseries(start_date, end_date):

    print('Reading Mohid timeseries...')

    current_date = start_date

    while current_date < end_date:
        folder = current_date.strftime('%Y-%m-%d') + '_' + (current_date + timedelta(days=1)).strftime('%Y-%m-%d')

        in_block = False

        with open(directory_location + folder + '/' + mohid_timeseries_filename) as f:
            
            for line in f:
                if line.startswith('      Seconds'):
                    header = line.replace('\n','').split(' ')
                    header = list(filter(None, header))
                elif line.startswith('<BeginTimeSerie>'):
                    in_block = True
                elif line.startswith('<EndTimeSerie>'):
                    break
                
                elif in_block == True:
                    line = line.replace('\n','').split(' ')
                    line = list(filter(None, line))
                    line = [float(i) for i in line]
                    
                    instant = [line[header.index('YY')], line[header.index('MM')], line[header.index('DD')], \
                    line[header.index('hh')], line[header.index('mm')], line[header.index('ss')]]

                    instant = [int(i) for i in instant]
                    instant = datetime(instant[0], instant[1], instant[2], instant[3], instant[4], instant[5])

                    time_and_property = [instant, line[header.index('temperature')]]
                    try:
                        model_array = np.append(model_array, [time_and_property], axis=0)
                    except NameError:
                        model_array = [time_and_property]
                    
            # this is so we don't have two entries with the same time:
            if end_date - current_date > timedelta(days=1):
                model_array = np.delete(model_array, -1, 0)
        
        current_date += timedelta(days=1)

    return model_array


def calculate_statistics(observed_array, model_array):

    print('\nCalculating Pearson correlation, RMSE and bias...')

    RMSE = 0

    while observed_array[-1,0] < model_array[-1,0]:
        model_array = np.delete(model_array, -1, axis=0)


    n = 0
    missed_observed = 0
    while n < len(observed_array[:,0]):

        while observed_array[n,0] != model_array[n,0]:

            if observed_array[n,0] > model_array[n,0]:
                model_array = np.delete(model_array, n, axis=0)

            elif observed_array[n,0] < model_array[n,0]:
                missed_observed += 1
                observed_array = np.delete(observed_array, n, axis=0)

        if observed_array[n,0] == model_array[n,0]:
            RMSE += (observed_array[n,1] - model_array[n,1])**2
        
        n += 1

    if missed_observed > 0:
        print('\nWARNING\n'+str(missed_observed)+' data points from the Hidrografico buoy timeserie were ' \
        'not used due to not having a corresponding data point in the MOHID timeserie.')
        print('A more frequent output of the MOHID timeserie is recommended.\n')

    RMSE = sqrt(RMSE / len(observed_array[:,0]))

    pearson, p_value = stats.pearsonr(observed_array[:,1], model_array[:,1])

    bias = np.mean(model_array[:,1]) - np.mean(observed_array[:,1])

    return(observed_array, model_array, pearson, RMSE, bias)


def plot_correlation(observed_array, model_array, start_date, end_date, pearson=None, RMSE=None, bias=None):

    title = ''
    title += ' | Pearson correlation: ' + str(round(pearson,2)) if pearson is not None else ''
    title += ' | RMSE: ' + str(round(RMSE,2)) + ' ºC' if RMSE is not None else ''
    title += ' | Bias: ' + str(round(bias,2)) + ' ºC' if bias is not None else ''
    title = title.strip(' | ')

    plt.rc('axes', axisbelow=True) # set grid below points
    fig, ax = plt.subplots()
    min_temp = min(list(observed_array[:,1]) + list(model_array[:,1]))
    max_temp = max(list(observed_array[:,1]) + list(model_array[:,1]))
    margem = round(0.1 * (max_temp - min_temp), 2)

    ax.scatter(observed_array[:,1], model_array[:,1], c='black', s=0.5)

    ax.plot([min_temp-margem, max_temp+margem], [min_temp-margem, max_temp+margem], color='grey', linewidth=0.5)
    plt.xlim(min_temp-margem, max_temp+margem)
    plt.ylim(min_temp-margem, max_temp+margem)

    ax.set_xlabel('Observed temperature (ºC)')
    ax.set_ylabel('Modeled temperature (ºC)')
    plt.title(title)
    plt.grid()
    fig.set_size_inches(9,9)
    fig.savefig('Temperature_correlation_' + datetime.strftime(start_date,'%Y-%m-%d') \
    + '_' + datetime.strftime(end_date,'%Y-%m-%d') + '.png', dpi=300)
    print('Saved correlation plot as image.')


def plot_timeseries(observed_array, model_array, start_date, end_date, pearson=None, RMSE=None, bias=None):

    title = ''
    title += ' | Pearson correlation: ' + str(round(pearson,2)) if pearson is not None else ''
    title += ' | RMSE: ' + str(round(RMSE,2)) + ' ºC' if RMSE is not None else ''
    title += ' | Bias: ' + str(round(bias,2)) + ' ºC' if bias is not None else ''
    title = title.strip(' | ')

    plt.rc('axes', axisbelow=True) # set grid below points
    fig, ax = plt.subplots()

    ax.scatter(observed_array[:,0], observed_array[:,1], c='red', s=0.5)
    ax.scatter(model_array[:,0], model_array[:,1], c='blue', s=0.5)
    ax.plot(observed_array[:,0], observed_array[:,1], c='red', linewidth=0.25, label='Buoy')
    ax.plot(model_array[:,0], model_array[:,1], c='blue', linewidth=0.25, label='Model')

    ax.set_xlabel('Date')
    ax.set_ylabel('Temperature (ºC)')
    ax.legend(loc='upper right')

    plt.title(title)
    plt.grid()
    fig.set_size_inches(16,9)
    fig.savefig('Temperature_timeserie_' + datetime.strftime(start_date,'%Y-%m-%d') \
    + '_' + datetime.strftime(end_date,'%Y-%m-%d') + '.png', dpi=300)
    print('Saved timeserie plot as image.')


################################################################################


if __name__ == '__main__':

    observed_array = read_buoy_timeseries(start_date, end_date)
    model_array = read_mohid_timeseries(start_date, end_date)

    observed_array_short, model_array_short, pearson, RMSE, bias = calculate_statistics(observed_array, model_array)
    print('Pearson correlation:', round(pearson,3))
    print('RMSE:', round(RMSE,3), 'ºC')
    print('Bias:', round(bias,3), 'ºC\n')

    if want_plot_correlation:
        plot_correlation(observed_array_short, model_array_short, start_date, end_date, pearson, RMSE, bias)
    if want_plot_timeseries:
        plot_timeseries(observed_array, model_array, start_date, end_date, pearson, RMSE, bias)
