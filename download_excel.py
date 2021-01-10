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


#Specifying direction where all files will be saved
file_path = Path(__file__).parent
save_dir = file_path/'excel_files'

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

driver.implicitly_wait(5)

#Selecting 'Республика Крым' or 'Город Севастополь' in region input field
region_field = driver.find_elements_by_class_name('styles__SelectControlSearch-sc-1vse7ay-5')[0]
region_field.click()
region_field.send_keys(str(sys.argv[1]), Keys.ENTER)

#Defining how many times button for the previous month should be clicked
first_available_date = datetime.datetime(2019, 10, 1)
current_date = datetime.datetime.now()

how_many_push_prev_arrow = (current_date.year - first_available_date.year)*12 + (current_date.month - first_available_date.month)

#Clicking 'previous' arrow required amount of times
driver.find_element_by_xpath('//*[@id="content-layout"]/div/div[2]/div[1]/div[2]').click()


for _ in range(how_many_push_prev_arrow):
    # Search for the button that allows to go back
    previous_arrow = driver.find_element_by_xpath('//*[@id="content-layout"]/div/div[2]/div[1]/div[2]/div[2]/div/table/tbody/tr[1]/td[1]')
    # Make click on that button
    webdriver.ActionChains(driver).click(previous_arrow).perform()

#Savingy from October 2019 (Наш Дом публикует показатели с 1-го Октября 2019) till today
for _ in range(how_many_push_prev_arrow+1): ###DO NOT FORGET TO FIX
    for day in driver.find_elements_by_class_name('datePickerSelectorTableDays'):
        day.click()
        driver.implicitly_wait(3)
        #Download button
        driver.find_element_by_xpath('//*[@id="content-layout"]/div/div[1]/div[2]/div[1]/div').click()
        #Click again on the element to select next day
        driver.find_element_by_xpath('//*[@id="content-layout"]/div/div[2]/div[1]/div[2]').click()
        driver.implicitly_wait(2)
    #Click next month arrow
    driver.find_element_by_xpath('//*[@id="content-layout"]/div/div[2]/div[1]/div[2]/div[2]/div/table/tbody/tr[1]/td[3]').click()
    driver.implicitly_wait(7)



