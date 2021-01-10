#Import libraries
from pathlib import Path
from selenium import webdriver #importing webdriver
from selenium.webdriver.common.keys import Keys #functionality to enter text and etc.
import time
import datetime
import pandas as pd
import re#REGEX
import sys

print(f'The execution of script "{__file__}" with argument:{sys.argv[1]} has started')

region_mapping = {"Республика Крым":91, "Город Севастополь":92}

#Specifying direction where all files will be saved
file_path = Path(__file__).parent
save_dir = file_path/'excel_files'


#Retrieving the last available date for both regions
"""Right now it exctracts date from the Excel file. When Oracle DB is set up the code would be amended"""
scraped_df = pd.read_excel(file_path/'developers_data_sev_and_crimea.xlsx', index_col=0)

last_date = scraped_df['date'][scraped_df['region_code']==region_mapping[sys.argv[1]]].max()
today = datetime.datetime.now()
difference_in_days = (today - last_date).days

print(f'The last available date for {sys.argv[1]} is {last_date}')
print(f'The difference between today and the last avilablae date in days is {difference_in_days}')

if difference_in_days == 0:
    # exits the program 
    sys.exit(f"The data in the database for {sys.argv[1]} is up-to-date") 


#Setting up a new folder - 'excel_files'
if save_dir.exists():
    pass
else:
    save_dir.mkdir()

#Setting up the Yandex browser
binary_yandex_driver_file = file_path/'Yandex_browser_webdriver/yandexdriver.exe' # path to YandexDriver
options = webdriver.ChromeOptions()
options.headless = True #do not to open the Yandex browser
prefs = {"download.default_directory": str(save_dir)}
options.add_experimental_option('prefs', prefs)
# options.headless = True #do not to open the Yandex browser
driver = webdriver.Chrome(executable_path=binary_yandex_driver_file, options=options)

nash_dom_rf_devs = 'https://xn--80az8a.xn--d1aqf.xn--p1ai/%D0%B0%D0%BD%D0%B0%D0%BB%D0%B8%D1%82%D0%B8%D0%BA%D0%B0/%D0%B6%D0%B8%D0%BB%D0%B8%D1%89%D0%BD%D0%BE%D0%B5_%D1%81%D1%82%D1%80%D0%BE%D0%B8%D1%82%D0%B5%D0%BB%D1%8C%D1%81%D1%82%D0%B2%D0%BE'
driver.get(nash_dom_rf_devs)

