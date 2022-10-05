# %%

import datetime
from http.client import OK
import re
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd
import numpy as np


link = 'http://maree.info/102'

"""
scrape maree info from web site
pour obtenir horaires de pleine mer et basse mer

"""
options = webdriver.ChromeOptions()
# options.add_experimental_option("excludeSwitches",["ignore-certificate-errors"])
# options.add_argument('--disable-gpu')
options.add_argument('--headless')


class Scraper(object):
    def __init__(self):
        # self.driver = webdriver.PhantomJS()
        self.driver = webdriver.Chrome('/Applications/chromedriver', options=options)  # Optional argument, if not specified will search path.
        self.driver.set_window_size(1120, 550)

    def extract_hours(self,df):
        regex =re.compile( "\d{2}h\d{2}")
        result=re.findall(regex, df)
        print(result)
        return result
    
    def extract_date(self,df):
        regex =re.compile( "\w{3}\.\w{2}")
        result=re.findall(regex, df)
        print(result)
        return result

    def time_converter(time):
        return datetime.strptime(time, "%Hh%M")

    def scrape(self):
        print('Loading...')
        self.driver.get(link)
        time.sleep(5) 
        OK_button =self.driver.find_element(By.CLASS_NAME, "Green")
        print(OK_button)
        OK_button.click()
        time.sleep(1) 
        s = BeautifulSoup(self.driver.page_source, "html.parser")
        maree_jours= s.find('table',{'id': "MareeJours"}).find_all("td")
        maree_infos= s.find('table',{'id': "MareeJours"}).find_all("th")
        PM_times=[]
        for maree_jour in maree_jours:
            bolds= maree_jour.find_all('b')
            for bold in bolds:
                if "h" in bold.get_text():
                    PM_maree= bold.get_text()
                    print("PM_maree", PM_maree)
                    PM_times.append(PM_maree)
        print("PM_times",PM_times)

        marees_time=[self.extract_hours(maree_jour.get_text()) for maree_jour in maree_jours  if "h" in maree_jour.get_text()]
        marees_date_arr=[self.extract_date(maree_info.get_text()) for maree_info in maree_infos if (("." in maree_info.get_text()))][1:7]

        marees_PM_BM=[]
        for hours in marees_time:
            daily_PM_BM=[]
            for hour in hours:
                if hour in PM_times:
                    daily_PM_BM.append(('PM', hour))
                else:
                    daily_PM_BM.append(('BM', hour))
            marees_PM_BM.append(daily_PM_BM)
        print(marees_PM_BM)



        merged_list = []
        for l in marees_date_arr:
            merged_list += l
        marees_date= merged_list
        print(marees_date)
        

        print("marees_time", marees_PM_BM)
        print("marees_date", np.array(marees_date))##TODO build loop over days and merge to dict{day:[horaires de marée]}
        keys= np.array(marees_date)
        values = marees_PM_BM
        marees = dict(zip(keys, values))
        print("marees", marees)
        return marees
        
def main():
    scraper = Scraper()
    maree_info=scraper.scrape()
    return maree_info


if __name__ == '__main__':
    main()
   

# %%
