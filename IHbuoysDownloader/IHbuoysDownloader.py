import os
import time
from datetime import datetime
from datetime import timedelta
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import numpy as np
from unidecode import unidecode


def round_if_number(number, n):
    try: return round(float(number), n)
    except ValueError: return number


def get_old_data(boia_name, year, month):
    df = pd.read_csv(
        './output/'+boia_name+'/'+boia_name+'_'+str(year)+'-'+str(month).zfill(2)+'.csv',
        sep=',', index_col='SDATA')
    return df


def get_new_data(par_dropdown):
    global driver
    par_dropdown_options = [x.text for x in par_dropdown.find_elements_by_tag_name('option')]
    df_final = None
    for par_opt in par_dropdown_options:
        par_dropdown.click()
        select = Select(par_dropdown)
        select.select_by_visible_text(par_opt)
        time.sleep(2)
        data = driver.find_element_by_id('showData')
        aux = []
        rows = data.find_elements_by_tag_name('tr')
        header = rows.pop(0)
        header = [c.text for c in header.find_elements_by_tag_name('th')]
        for row in rows:
            aux.append([round_if_number(c.text, 1) for c in row.find_elements_by_tag_name('td')])
        df = pd.DataFrame.from_records(aux, columns=header)
        df = df.set_index(header[0])
        if df_final is None:
            df_final = df
        else:
            df_final = df_final.join(df)
    return df_final


def concat_old_and_new_df(df_new, df_old):
    df_old_indexes = df_old.index.values
    for df_new_index in df_new.index.values:
        if df_new_index in df_old_indexes:
            df_new = df_new.drop(df_new_index)
    return pd.concat([df_old, df_new])


def save_data_in_csv(boia_name, df, year, month):
    output_location = './output/' + boia_name + '/'
    if os.path.isdir(output_location) is False:
        os.makedirs(output_location)
    output_location = output_location + boia_name+'_'+str(year)+'-'+str(month).zfill(2)+'.csv'
    df.to_csv(output_location, sep=',')


def split_df_by_month(df):
    df_indexes = df.index.values
    df_indexes_last_month = []
    df_indexes_curr_month = []
    for i in df_indexes:
        if datetime.strptime(i, '%Y-%m-%d %H:%M') < datetime(year=datetime.now().year,
                                                             month=datetime.now().month,
                                                             day=1):
            df_indexes_last_month.append(i)
        else:
            df_indexes_curr_month.append(i)
    df1 = df.loc[:df_indexes_last_month[-1],:]
    df2 = df.loc[df_indexes_curr_month[0]:,:]
    return df1, df2


def main():
    global driver

    print('Starting')

    url = 'https://www.hidrografico.pt/m.boias'

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)

    boia_dropdown = driver.find_element_by_id('dropdown')
    boia_dropdown_options = [x.text for x in boia_dropdown.find_elements_by_tag_name('option')]

    per_dropdown = driver.find_element_by_id('per')
    per_dropdown.click()
    time.sleep(1)
    select = Select(per_dropdown)
    select.select_by_visible_text('Últimas 48 horas')
    time.sleep(1)
    print('\nDownloading buoys data:')
    for boia_opt in boia_dropdown_options:
        print('- ' + boia_opt + '...', end='\r')
        boia_dropdown.click()
        select = Select(boia_dropdown)
        select.select_by_visible_text(boia_opt)
        time.sleep(1)
        par_dropdown = driver.find_element_by_id('par')

        boia_name = unidecode(boia_opt).replace(' ','_')

        now = datetime.now()

        if now.day > 2:
            df_new = get_new_data(par_dropdown)
            df_new = df_new.apply(lambda x: x.str.strip() if \
                isinstance(x, str) else x).replace('', np.nan)
            df_new = df_new.dropna(how='all')
            if df_new.empty:
                print(' '*30, end='\r')
                continue
            try:
                df_old = get_old_data(boia_name, now.year, now.month)
                df_old = df_old.apply(lambda x: x.str.strip() if \
                    isinstance(x, str) else x).replace('', np.nan)
                df_old = df_old.dropna(how='all')
                df = concat_old_and_new_df(df_new, df_old)
                save_data_in_csv(boia_name, df, now.year, now.month)
            except FileNotFoundError:
                save_data_in_csv(boia_name, df_new, now.year, now.month)

        elif now.day <= 2:
            last_month = now - timedelta(days=15)
            df_new = get_new_data(par_dropdown)
            df_new = df_new.apply(lambda x: x.str.strip() if \
                isinstance(x, str) else x).replace('', np.nan)
            df_new = df_new.dropna(how='all')
            if df_new.empty:
                print(' '*30, end='\r')
                continue
            df_new_1, df_new_2 = split_df_by_month(df_new)
            try:
                df_old = get_old_data(boia_name, last_month.year, last_month.month)
                df_old = df_old.apply(lambda x: x.str.strip() if \
                    isinstance(x, str) else x).replace('', np.nan)
                df_old = df_old.dropna(how='all')
                df = concat_old_and_new_df(df_new_1, df_old)
                save_data_in_csv(boia_name, df, last_month.year, last_month.month)
            except FileNotFoundError:
                save_data_in_csv(boia_name, df_new_1, last_month.year, last_month.month)
            try:
                df_old = get_old_data(boia_name, now.year, now.month)
                df_old = df_old.apply(lambda x: x.str.strip() if isinstance(x, str) \
                    else x).replace('', np.nan)
                df_old = df_old.dropna(how='all')
                df = concat_old_and_new_df(df_new_2, df_old)
                save_data_in_csv(boia_name, df, now.year, now.month)
            except FileNotFoundError:
                save_data_in_csv(boia_name, df_new_2, now.year, now.month)
        print('- ' + boia_opt + '.  ')
    print('Finished downloading data')
    driver.quit()
    print('Closed chromedriver')
    print('Finished')


if __name__ == '__main__':
    main()
