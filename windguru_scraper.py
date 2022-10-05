# %%
##test pour webscrape windguru et recommander best surf spot
import re
import time
from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd

link = 'https://www.windguru.cz/18'


options = webdriver.ChromeOptions()
# options.add_experimental_option("excludeSwitches",["ignore-certificate-errors"])
# options.add_argument('--disable-gpu')
options.add_argument('--headless')
# chrome_driver_path = "C:\Python27\Scripts\chromedriver.exe"

class Scraper(object):
    def __init__(self):
        # self.driver = webdriver.PhantomJS()
        self.driver = webdriver.Chrome('/Applications/chromedriver', options=options)  # Optional argument, if not specified will search path.
        self.driver.set_window_size(1120, 550)

    def scrape(self):
        print('Loading...')
        self.driver.get(link)
        time.sleep(10) # Let the user actually see something!
        OK_button =self.driver.find_element("id", "accept-choices")
        OK_button.click()
        time.sleep(1) # Let the user actually see something!

        forecast = {}

        s = BeautifulSoup(self.driver.page_source, "html.parser")

        rows = s.select(".tabulka tbody tr")

        # for row in rows[0:11]:
        for row in rows[0:19]:
            cells = row.find_all("td")
            id = row['id']
            forecast[id] = []
            i = 0
            # for cell in cells:
            for cell in cells[0:19]:#select only first 10 values

                # print(cell, i)
                if ('DIRPW' in id): # or ('DIRPW' in id):
                    # print(id + " " + str(i))
                    value = cell.find('span').find('svg').find('g')["transform"]
                    # print(value)
                elif('SMER' in id):
                    value = cell.find('span')["title"]
                elif('CDC') in id:
                    # value = cell.find('div').get_text()
                    clouds_alts=cell.find_all('div')
                    value=[]
                    for alt in clouds_alts:
                        value.append(alt.get_text())
                else:
                    value = cell.get_text()
                forecast[id].append(value)
                i = i + 1

        print("forecast",forecast)

        self.driver.quit()
        return forecast

def function_any():
    return print("any")

def extract(df):##TODO:should return letter without square bracket
    # regex = re.compile("^[^\(]+")
    regex =re.compile( "^[^\s(]+")
    return re.findall(regex, df)[0]

def extract_degre(df):##TODO:should return letter without square bracket
    # regex = re.compile("^[^\(]+")
    regex =re.compile( "\d+\.\d+")
    return re.findall(regex, df)[0]

def main():
    scraper = Scraper()
    forecast0=scraper.scrape()
   
    your_keys=["tabid_0_0_dates", "tabid_0_0_WINDSPD", "tabid_0_0_SMER", "tabid_0_0_HTSGW","tabid_0_0_PERPW", "tabid_0_0_WINDSPD","tabid_0_0_APCP1s", "tabid_0_0_CDC"]
    subsets={ your_key: forecast0[your_key] for your_key in your_keys }
    df= pd.DataFrame(subsets)
    df.columns = df.columns.str.replace('tabid_0_0_', '')
    df["wind_direction"]=df['SMER'].apply(lambda x: extract(x))##TODO:should return letter without square bracket
    df["wind_direction_degre"]=df['SMER'].apply(lambda x: extract_degre(x))##TODO:should return letter without square bracket
    # df['spot_best'] = ['sainte barbe' if 'N' in x else 'guerite' for x in df['SMER']]
    
    next_cond=[]
    for i in range(0, 19):
        
        df_i= df.iloc[i]
        cond= {
            'date': df_i['dates'],
            'tide':"midlow",
            "wave_height":float(df_i["HTSGW"]),
            "wave_period":int(df_i["PERPW"]),
            "wind_speed":int(df_i["WINDSPD"]),
            "wind_dir":df_i["wind_direction"],
            "wind_dir_deg":round(float(df_i["wind_direction_degre"]),2),
            "rain":df_i["APCP1s"], 
            "clouds":df_i["CDC"]
            }
        next_cond.append(cond)
    print("next_cond", next_cond)

    # return conditions
    return next_cond





if __name__ == '__main__':
    main()
# %%

# %%

# %%
