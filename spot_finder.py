# %%
from dataclasses import dataclass
import datetime
from datetime import datetime, timedelta
from heapq import merge

from symtable import Class
from flask import render_template
import numpy as np
import pandas as pd
import re
### test for multiple filter on spot
tiny_to_big= np.arange(5, 35, 1)/10
tiny_to_correct= np.arange(5, 20, 1)/10
big_to_massive= np.arange(15, 80, 1)/10
massive= np.arange(25, 80, 1)/10
tiny= np.arange(0, 6, 1)/10
small_period = np.arange(0,8,1)
good_period= np.arange(8,30,1)
est_wind=["NNE","NE","ENE","E","ESE","SE"]
nord_wind=["NNO","N", "NNE", "NE", "ENE"]
ouest_wind=["NNO", "NO", "ONO", "O", "OSO", "SO", "SSO"]
sud_wind=["OSO" ,"SO", "SSO", "S", "SSE", "SE"]
desc_start="descending (start)"
desc_mid="descending (middle)"
desc_end= "descending (end)"
asc_start="ascending (start)"
asc_mid="ascending (middle)"
asc_end="ascending (end)"
base_col="blue"
#https://www.gpsvisualizer.com/calculators pour définir angle de la côte

spots=[
{"id":"surf_sainte_barbe", "activity": "surf", "name": "surf sainte barbe", "tide":[asc_mid, asc_end, desc_start, desc_mid], "wave_height":tiny_to_big, "wind_dir":est_wind, "wave_period": good_period, "orientation":147.11},
{"id":"surf_guerite","activity": "surf" , "name": "surf guerite", "tide":[asc_mid, asc_end, desc_start, desc_mid], "wave_height":tiny_to_big, "wind_dir":est_wind, "wave_period": good_period, "orientation":157.904},
{"id":"surf_kerillio", "activity": "surf", "name": "surf kerillio", "tide":[asc_mid, asc_end, desc_start, desc_mid], "wave_height":tiny_to_correct, "wind_dir":est_wind, "wave_period": good_period, "orientation":129.458},
{"id":"surf_kerouriec", "activity": "surf", "name": "surf kerouriec", "tide":[asc_mid, asc_end, desc_start, desc_mid], "wave_height":big_to_massive, "wind_dir":est_wind, "wave_period": good_period, "orientation":103.722},
{"id":"surf_port_bara", "activity": "surf", "name": "surf port bara", "tide":[asc_start, desc_end], "wave_height":tiny_to_correct, "wind_dir":est_wind, "wave_period": good_period, "orientation":163.84},
{"id":"surf_port_blanc","activity": "surf" , "name": "surf port blanc", "tide":[asc_start, desc_end], "wave_height":tiny_to_correct, "wind_dir":est_wind, "wave_period": good_period, "orientation":146.153},
{"id":"surf_port_louis", "activity": "surf", "name": "surf port louis", "tide":[asc_mid,desc_mid], "wave_height":massive, "wind_dir":nord_wind, "wave_period": good_period, "orientation":116.269},
{"id":"surf_penthievre", "activity": "surf", "name": "surf penthievre", "tide":[asc_mid, asc_end, desc_start, desc_mid], "wave_height":big_to_massive, "wind_dir":["E", "NE", "NNE", "SE", "SSE"], "wave_period": good_period, "orientation":187.173},
{"id":"surf_carnac", "activity": "surf", "name": "surf carnac", "tide":[asc_mid, desc_mid], "wave_height":massive, "wind_dir":["E", "NE", "NNE", "SE", "SSE"], "wave_period": good_period, "orientation":78.857},
{"id":"swim_penthievre", "activity": "swim", "name": "swim pentievre", "tide":[asc_mid, asc_end, desc_start, desc_mid], "wave_height":tiny_to_correct, "wind_dir":ouest_wind, "wave_period": small_period, "orientation":187.173},
{"id":"swim_sainte_barbe", "activity": "swim", "name": "swim sainte barbe", "tide":[asc_mid, asc_end, desc_start, desc_mid], "wave_height":tiny, "wind_dir":est_wind, "wave_period": small_period,"orientation":147.11},
{"id":"swim_kernevest", "activity": "swim", "name": "swim kernevest", "tide":[asc_mid, asc_end, desc_start, desc_mid], "wave_height":tiny_to_correct, "wind_dir":est_wind, "wave_period": small_period,"orientation":95.02},
{"id":"swim_saint_pierre", "activity": "swim", "name": "swim Saint Pierre", "tide":[asc_mid, asc_end, desc_start, desc_mid], "wave_height":tiny_to_correct, "wind_dir":est_wind, "wave_period": small_period,"orientation":129.983},
{"id":"swim_locqmariaquer","activity": "swim" , "name": "swim Locmariaquer", "tide":[asc_mid, asc_end, desc_start, desc_mid], "wave_height":tiny_to_correct, "wind_dir":est_wind, "wave_period": small_period,"orientation":87.979},
{"id":"surf_men_du", "activity": "surf", "name": "surf Men Du", "tide":[asc_mid, asc_end, desc_start, desc_mid], "wave_height":massive, "wind_dir":est_wind, "wave_period": good_period,"orientation":81.453},
{"id":"surf_quiberon", "activity": "surf", "name": "surf Quiberon", "tide":[asc_mid, asc_end, desc_start, desc_mid], "wave_height":big_to_massive, "wind_dir":est_wind, "wave_period": good_period,"orientation":110.441},
# {"id":"nothing", "activity": "surf", "name": "nothing", "tide":[asc_mid, asc_end,asc_start, desc_start, desc_mid, desc_end], "wave_height":tiny_to_correct, "wind_dir":sud_wind, "wave_period": small_period, "orientation":0},
]

# spots=[surf_sainte_barbe, surf_port_bara, surf_port_louis, surf_penthievre, nothing, swim_penthievre, swim_sainte_barbe]
angle_to_shore = 80


@dataclass
class Spot_Finder():
    # def __init__(self, conditions) -> None:
    #     self.conditions= conditions
    conditions: any

    def get_maree_info(self):
        maree_info= self.conditions["conditions_maree_info"]
        print("maree_info")
        # merge_maree_info= zip(maree_info.PMBM, maree_info.horaires)
        return maree_info.items()

    def compute_var_for_spots(self):
        spots_df=pd.DataFrame(spots)
        spots_df["best_wind_dir_min"]= round(spots_df["orientation"]-90+ angle_to_shore, 2)
        spots_df["best_wind_dir_max"]= round(spots_df["orientation"]-90+360-angle_to_shore, 2)
        spots_df["best_wind_dir"] = list(zip(spots_df["best_wind_dir_min"],spots_df["best_wind_dir_max"]))
        is_swim= [True if (action=="swim") else False for action in spots_df["activity"]]
        spots_df["is_swim"]=is_swim
        return spots_df

    def get_best_spot_list(self):
        best_spots_list=[]
        print("conditions from get_best_spot_list", self.conditions)

        merge_maree_info= self.get_maree_info()
        print("merge maree info", merge_maree_info)
        for i,condition, in enumerate(self.conditions["conditions_windguru"]):
            
            best_spot_builder= Best_Spot_Builder(condition, merge_maree_info)
            next_extreme= Next_Extreme()
            is_cloudy= best_spot_builder.define_is_cloudy()
            is_raining=best_spot_builder.define_is_raining()
            filtered_maree_info= best_spot_builder.filter_maree_info()
            clouds = condition["clouds"]
            clouds_max= max(clouds)
            next_tide= next_extreme.find_next_extreme(condition["date"], filtered_maree_info)
            tide_dir=best_spot_builder.define_tide_dir(next_tide)
            tide_diagramm= best_spot_builder.convert_tide_dir(tide_dir)
            
            #turn surf spots in dataframe and compute new var(best wind direction, swim vs surf...)
            spots_df= self.compute_var_for_spots()


            tide= [True if (tide_dir in i) else False for i in spots_df["tide"]]
            tide_s= pd.Series(tide)
            wave_height= [True if (condition['wave_height'] in i) else False for i in spots_df["wave_height"]]
            wave_height_s=  pd.Series(wave_height)
            wind_dir_deg= [True if ((i[0]>condition['wind_dir_deg']) | (i[1]<condition['wind_dir_deg'])) else False for i in spots_df['best_wind_dir']]
            wind_dir_deg_s= pd.Series(wind_dir_deg)
            wave_period= [True if (condition['wave_period'] in i) else False for i in spots_df['wave_period']]
            wave_period_s=  pd.Series(wave_period)


            #filter spots_df according to tide, wave, wind conditions
            best_spot= spots_df[tide_s & wave_height_s & wind_dir_deg_s & wave_period_s]
            print("best spot", best_spot)

          
            best_spots_list.append({"time":condition["date"],"spot":best_spot[["name", "orientation", "activity", "is_swim"]],"spot_orientation":best_spot["orientation"], "tide":condition["tide"], "wave_height":condition["wave_height"],  "wave_period":condition["wave_period"], "wind_dir":condition["wind_dir"], "wind_dir_deg":condition["wind_dir_deg"], "wind_speed": condition["wind_speed"], "rain": condition["rain"], 'is_raining':is_raining, "clouds": clouds_max, 'is_cloudy': is_cloudy, "maree_info":merge_maree_info, "filtered_maree_info": filtered_maree_info, "next_tide":next_tide, "tide_dir": tide_dir, "tide_diagramm": tide_diagramm})
         
        print("best_spots_list",best_spots_list)


        return best_spots_list

class Best_Spot_Builder():
        def __init__(self, condition, merge_maree_info):
            self.condition= condition
            self.merge_maree_info= merge_maree_info

        def define_is_raining(self):
            if (self.condition["rain"] != "\xa0"):
                is_raining = True
            else:
                is_raining= False
            return is_raining

        def define_is_cloudy(self):
            if (self.condition["clouds"] != ["\xa0","\xa0","\xa0" ]):
                is_cloudy = True
            else:
                is_cloudy= False
            return is_cloudy

        def extract_date_number_windguru(self, df):
            regex =re.compile("(\d+)\.")
            # result=re.findall(regex, df)
            result = re.search(regex, df)
            date_number= result.group(1)
            print("date number windguru", date_number)
            return date_number

        def extract_date_number_maree_info(self, df):
            regex =re.compile("\d+")
            result=re.findall(regex, df)
            date_number= result[0]
            print("date number maree info", date_number)
            return date_number

        def define_tide_dir(self, next_tide):
            print("define_tide_function")
            PMBM= next_tide[0][0]
            next_previous= next_tide[1]
            time_to_tide = next_tide[3]
            desc_start="descending (start)"
            desc_mid="descending (middle)"
            desc_end= "descending (end)"
            asc_start="ascending (start)"
            asc_mid="ascending (middle)"
            asc_end="ascending (end)"
            print("time_to_tide", time_to_tide)
            print("time_to_tide_min", time_to_tide)
            if PMBM =='PM' and next_previous=="previous" and time_to_tide<timedelta(minutes=120):
                tide_dir= desc_start
            elif PMBM =='PM' and next_previous=="previous" and (timedelta(minutes=120)<=time_to_tide<= timedelta(minutes=240)):
                tide_dir= desc_mid
            elif PMBM =='PM' and next_previous=="previous" and time_to_tide > timedelta(minutes=240):
                tide_dir= desc_end

            elif PMBM=='PM' and next_previous=="next" and time_to_tide<timedelta(minutes=120):
                tide_dir= asc_end
            elif PMBM=='PM' and next_previous=="next" and (timedelta(minutes=120) <= time_to_tide <= timedelta(minutes=240)):
                tide_dir= asc_mid
            elif PMBM=='PM' and next_previous=="next" and  time_to_tide > timedelta(minutes=240):
                tide_dir= asc_start

            elif PMBM=='BM' and next_previous=="next" and time_to_tide<timedelta(minutes=120):
                tide_dir= desc_end
            elif PMBM=='BM' and next_previous=="next" and  timedelta(minutes=120)<time_to_tide:
                tide_dir= desc_mid
            elif PMBM=='BM' and next_previous=="next" and  time_to_tide > timedelta(minutes=240):
                tide_dir= desc_start


            elif PMBM=='BM' and next_previous=="previous" and time_to_tide<timedelta(minutes=120):
                tide_dir= asc_start
            elif PMBM=='BM' and next_previous=="previous" and (timedelta(minutes=120)<time_to_tide and time_to_tide<timedelta(minutes=240)):
                tide_dir= asc_mid
            elif PMBM=='BM' and next_previous=="previous" and  time_to_tide > timedelta(minutes=240):
                tide_dir= asc_end
            return tide_dir

        def convert_tide_dir(self, tide_dir):
            desc_start="descending (start)"
            desc_mid="descending (middle)"
            desc_end= "descending (end)"
            asc_start="ascending (start)"
            asc_mid="ascending (middle)"
            asc_end="ascending (end)"
            base_col="blue"
            if tide_dir== asc_start:
                tide_diagramm= ["aqua", base_col, base_col, base_col, base_col, base_col]
            elif tide_dir== asc_mid:
                tide_diagramm= [base_col, "aqua", base_col, base_col, base_col, base_col]
            elif tide_dir== asc_end:
                tide_diagramm= [base_col, base_col, "aqua", base_col, base_col, base_col]
            elif tide_dir== desc_start:
                tide_diagramm= [base_col, base_col, base_col, "aqua", base_col, base_col]
            elif tide_dir== desc_mid:
                tide_diagramm= [base_col, base_col, base_col, base_col, "aqua", base_col]
            elif tide_dir== desc_end:
                tide_diagramm= [base_col, base_col, base_col, base_col, base_col, "aqua"]
            return tide_diagramm


        def filter_maree_info(self):
            # time_beginning= extract_two_first_letters(condition["date"])
            date_number_windguru= self.extract_date_number_windguru(self.condition["date"])
            # print('time_begining', time_beginning)
            print('date_number_windguru', date_number_windguru)
            # filtered_maree_info= [maree_info for maree_info in merge_maree_info if extract_two_first_letters(maree_info[0])==time_beginning]#TODO fix this part ther's somthong wrong
            filtered_maree_info= [maree_info for maree_info in self.merge_maree_info if int(self.extract_date_number_maree_info(maree_info[0]))==int(date_number_windguru)]#TODO fix this part ther's somthong wrong
            return filtered_maree_info       
    
class Next_Extreme():

    def extract_hours(self,df):##TODO:should return letter without square bracket
        regex =re.compile( "\d{2}h\d{2}")
        result=re.findall(regex, df)
    
        return result

    def extract_hours_from_date(self,df):
        regex =re.compile( "\d+h")
        result=re.findall(regex, df)
        
        return result
        
    def time_converter(self, time):
        return datetime.strptime(time, "%Hh%M")

    def find_next_extreme(self,time, best_spot_list):
        # time=best_spot_list['time']
        print("time", time)
        time_hour= self.extract_hours_from_date(time)[0]+"00"
        print("time_hour", time_hour)
        print("best spot list",best_spot_list )
        PMBMs= best_spot_list[0][1]
        print("PMBMs",PMBMs)

        deltas=[]
        for PMBM in PMBMs:
            if self.time_converter(PMBM[1])<self.time_converter(time_hour):
                delta = (PMBM, "previous", "+", self.time_converter(time_hour)-self.time_converter(PMBM[1]), (self.time_converter(time_hour)-self.time_converter(PMBM[1])).min)
            else:
                delta = (PMBM, "next","-",self.time_converter(PMBM[1])-self.time_converter(time_hour),(self.time_converter(PMBM[1])-self.time_converter(time_hour)).min)
            deltas.append(delta)
        print("deltas",deltas)
        # next_extreme= min(deltas)
        next_extreme = min(deltas, key=lambda delta: delta[3])
        print("next_extreme", next_extreme)
        print(f"{next_extreme[3]} to {next_extreme[1]} {next_extreme[0]}")
        print(f"{next_extreme[0]} {next_extreme[2]} {next_extreme[3]}")
        return next_extreme

# if __name__ == "__main__":
# spot_finder= Spot_Finder()
# next_extreme = Next_Extreme()
# conditions= {'tide':"midlow", "wave_height":0.5, "wind_dir":"E"}
# spot_finder.get_best_spot(conditions)

# conditions= [{'date': 'Lu29.20h', 'tide': 'midlow', 'wave_height': 0.5, 'wind_dir': 'E'}, {'date': 'Lu29.22h', 'tide': 'midlow', 'wave_height': 7, 'wind_dir': 'E'}, {'date': 'Ma30.03h', 'tide': 'midlow', 'wave_height': 0.7, 'wind_dir': 'NE'}, {'date': 'Ma30.05h', 'tide': 'midlow', 'wave_height': 0.7, 'wind_dir': 'NE'}]
# conditions= {'conditions_windguru': [{'date': 'Di11.11h', 'tide': 'midlow', 'wave_height': 0.7, 'wave_period': 11, 'wind_speed': 13, 'wind_dir': 'ESE', 'wind_dir_deg': 115.21, 'rain': '\xa0', 'clouds': ['8', '\xa0', '66']}, {'date': 'Di11.13h', 'tide': 'midlow', 'wave_height': 0.7, 'wave_period': 11, 'wind_speed': 11, 'wind_dir': 'SE', 'wind_dir_deg': 124.75, 'rain': '\xa0', 'clouds': ['\xa0', '\xa0', '13']}, {'date': 'Di11.15h', 'tide': 'midlow', 'wave_height': 0.6, 'wave_period': 10, 'wind_speed': 9, 'wind_dir': 'SE', 'wind_dir_deg': 131.43, 'rain': '\xa0', 'clouds': ['\xa0', '\xa0', '\xa0']}, {'date': 'Di11.17h', 'tide': 'midlow', 'wave_height': 0.5, 'wave_period': 10, 'wind_speed': 6, 'wind_dir': 'SE', 'wind_dir_deg': 129.99, 'rain': '\xa0', 'clouds': ['\xa0', '9', '\xa0']}, {'date': 'Di11.19h', 'tide': 'midlow', 'wave_height': 0.5, 'wave_period': 10, 'wind_speed': 3, 'wind_dir': 'ESE', 'wind_dir_deg': 108.06, 'rain': '\xa0', 'clouds': ['32', '16', '\xa0']}, {'date': 'Di11.21h', 'tide': 'midlow', 'wave_height': 0.5, 'wave_period': 10, 'wind_speed': 3, 'wind_dir': 'ENE', 'wind_dir_deg': 60.43, 'rain': '\xa0', 'clouds': ['23', '\xa0', '\xa0']}, {'date': 'Lu12.03h', 'tide': 'midlow', 'wave_height': 0.6, 'wave_period': 10, 'wind_speed': 14, 'wind_dir': 'E', 'wind_dir_deg': 97.62, 'rain': '\xa0', 'clouds': ['25', '15', '\xa0']}, {'date': 'Lu12.05h', 'tide': 'midlow', 'wave_height': 0.7, 'wave_period': 9, 'wind_speed': 14, 'wind_dir': 'E', 'wind_dir_deg': 92.3, 'rain': '\xa0', 'clouds': ['48', '7', '\xa0']}, {'date': 'Lu12.07h', 'tide': 'midlow', 'wave_height': 0.7, 'wave_period': 9, 'wind_speed': 14, 'wind_dir': 'E', 'wind_dir_deg': 89.72, 'rain': '\xa0', 'clouds': ['64', '5', '\xa0']}, {'date': 'Lu12.09h', 'tide': 'midlow', 'wave_height': 0.8, 'wave_period': 9, 'wind_speed': 14, 'wind_dir': 'E', 'wind_dir_deg': 90.44, 'rain': '\xa0', 'clouds': ['81', '42', '\xa0']}], 'conditions_maree_info': {'Dim.11': ['00h04', '06h21', '12h23', '18h31'], 'Lun.12': ['00h46', '06h54', '13h05', '19h03'], 'Mar.13': ['01h27', '07h22', '13h46', '19h33'], 'Mer.14': ['02h06', '07h48', '14h26', '20h02'], 'Jeu.15': ['02h45', '08h14', '15h07', '20h33'], 'Ven.16': ['03h23', '08h43', '15h49', '21h08']}}
# conditions= {'conditions_windguru': [{'date': 'Me14.17h', 'tide': 'midlow', 'wave_height': 0.8, 'wave_period': 14, 'wind_speed': 11, 'wind_dir': 'OSO', 'wind_dir_deg': 257.08, 'rain': '\xa0', 'clouds': ['99', '23', '70']}, {'date': 'Me14.19h', 'tide': 'midlow', 'wave_height': 0.8, 'wave_period': 14, 'wind_speed': 11, 'wind_dir': 'O', 'wind_dir_deg': 266.45, 'rain': '\xa0', 'clouds': ['89', '24', '85']}, {'date': 'Me14.21h', 'tide': 'midlow', 'wave_height': 0.8, 'wave_period': 14, 'wind_speed': 11, 'wind_dir': 'O', 'wind_dir_deg': 275.15, 'rain': '\xa0', 'clouds': ['79', '61', '84']}, {'date': 'Je15.03h', 'tide': 'midlow', 'wave_height': 0.7, 'wave_period': 14, 'wind_speed': 9, 'wind_dir': 'N', 'wind_dir_deg': 0.81, 'rain': '\xa0', 'clouds': ['12', '16', '75']}, {'date': 'Je15.05h', 'tide': 'midlow', 'wave_height': 0.7, 'wave_period': 13, 'wind_speed': 10, 'wind_dir': 'N', 'wind_dir_deg': 0.8, 'rain': '\xa0', 'clouds': ['28', '16', '76']}, {'date': 'Je15.07h', 'tide': 'midlow', 'wave_height': 0.7, 'wave_period': 13, 'wind_speed': 11, 'wind_dir': 'N', 'wind_dir_deg': 349.66, 'rain': '\xa0', 'clouds': ['24', '22', '35']}, {'date': 'Je15.09h', 'tide': 'midlow', 'wave_height': 0.6, 'wave_period': 13, 'wind_speed': 12, 'wind_dir': 'NNO', 'wind_dir_deg': 347.27, 'rain': '\xa0', 'clouds': ['14', '11', '23']}, {'date': 'Je15.11h', 'tide': 'midlow', 'wave_height': 0.6, 'wave_period': 13, 'wind_speed': 9, 'wind_dir': 'N', 'wind_dir_deg': 354.27, 'rain': '\xa0', 'clouds': ['10', '9', '47']}, {'date': 'Je15.13h', 'tide': 'midlow', 'wave_height': 0.5, 'wave_period': 13, 'wind_speed': 8, 'wind_dir': 'NO', 'wind_dir_deg': 315.46, 'rain': '\xa0', 'clouds': ['\xa0', '8', '40']}, {'date': 'Je15.15h', 'tide': 'midlow', 'wave_height': 0.5, 'wave_period': 13, 'wind_speed': 10, 'wind_dir': 'NO', 'wind_dir_deg': 307.39, 'rain': '\xa0', 'clouds': ['7', '\xa0', '12']}], 'conditions_maree_info': {'Mer.14': [('BM', '02h06'), ('PM', '07h48'), ('BM', '14h26'), ('PM', '20h02')], 'Jeu.15': [('BM', '02h45'), ('PM', '08h14'), ('BM', '15h07'), ('PM', '20h33')], 'Ven.16': [('BM', '03h23'), ('PM', '08h43'), ('BM', '15h49'), ('PM', '21h08')], 'Sam.17': [('BM', '04h05'), ('PM', '09h18'), ('BM', '16h38'), ('PM', '21h54')], 'Dim.18': [('BM', '04h55'), ('PM', '10h08'), ('BM', '17h40')], 'Lun.19': [('PM', '00h07'), ('BM', '06h02'), ('PM', '13h12'), ('BM', '19h10')]}}

# conditions ={'conditions_windguru': [{'date': 'Ve16.17h', 'tide': 'midlow', 'wave_height': 0.5, 'wave_period': 11, 'wind_speed': 12, 'wind_dir': 'N', 'wind_dir_deg': 357.86, 'rain': '\xa0', 'clouds': ['94', '\xa0', '56']}, {'date': 'Ve16.19h', 'tide': 'midlow', 'wave_height': 0.5, 'wave_period': 11, 'wind_speed': 14, 'wind_dir': 'N', 'wind_dir_deg': 8.77, 'rain': '\xa0', 'clouds': ['61', '\xa0', '21']}, {'date': 'Ve16.21h', 'tide': 'midlow', 'wave_height': 0.8, 'wave_period': 11, 'wind_speed': 16, 'wind_dir': 'NNE', 'wind_dir_deg': 28.05, 'rain': '\xa0', 'clouds': ['\xa0', '\xa0', '\xa0']}, {'date': 'Sa17.03h', 'tide': 'midlow', 'wave_height': 0.6, 'wave_period': 11, 'wind_speed': 10, 'wind_dir': 'NNE', 'wind_dir_deg': 11.47, 'rain': '\xa0', 'clouds': ['\xa0', '\xa0', '\xa0']}, {'date': 'Sa17.05h', 'tide': 'midlow', 'wave_height': 0.5, 'wave_period': 11, 'wind_speed': 9, 'wind_dir': 'NNE', 'wind_dir_deg': 31.16, 'rain': '\xa0', 'clouds': ['\xa0', '\xa0', '\xa0']}, {'date': 'Sa17.07h', 'tide': 'midlow', 'wave_height': 0.5, 'wave_period': 13, 'wind_speed': 7, 'wind_dir': 'NE', 'wind_dir_deg': 43.32, 'rain': '\xa0', 'clouds': ['\xa0', '\xa0', '\xa0']}, {'date': 'Sa17.09h', 'tide': 'midlow', 'wave_height': 0.5, 'wave_period': 12, 'wind_speed': 9, 'wind_dir': 'NE', 'wind_dir_deg': 44.9, 'rain': '\xa0', 'clouds': ['\xa0', '\xa0', '\xa0']}, {'date': 'Sa17.11h', 'tide': 'midlow', 'wave_height': 0.5, 'wave_period': 12, 'wind_speed': 8, 'wind_dir': 'ENE', 'wind_dir_deg': 61.31, 'rain': '\xa0', 'clouds': ['18', '\xa0', '\xa0']}, {'date': 'Sa17.13h', 'tide': 'midlow', 'wave_height': 0.5, 'wave_period': 12, 'wind_speed': 7, 'wind_dir': 'ENE', 'wind_dir_deg': 78.7, 'rain': '\xa0', 'clouds': ['26', '\xa0', '7']}, {'date': 'Sa17.15h', 'tide': 'midlow', 'wave_height': 0.5, 'wave_period': 12, 'wind_speed': 6, 'wind_dir': 'NE', 'wind_dir_deg': 48.36, 'rain': '\xa0', 'clouds': ['28', '\xa0', '12']}], 'conditions_maree_info': {'Ven.16': [('BM', '03h23'), ('PM', '08h43'), ('BM', '15h49'), ('PM', '21h08')], 'Sam.17': [('BM', '04h05'), ('PM', '09h18'), ('BM', '16h38'), ('PM', '21h54')], 'Dim.18': [('BM', '04h55'), ('PM', '10h08'), ('BM', '17h40')], 'Lun.19': [('PM', '00h07'), ('BM', '06h02'), ('PM', '13h12'), ('BM', '19h10')], 'Mar.20': [('PM', '02h02'), ('BM', '07h37'), ('PM', '14h33'), ('BM', '20h41')], 'Mer.21': [('PM', '03h04'), ('BM', '08h57'), ('PM', '15h24'), ('BM', '21h36')]}}
# spot_finder.get_best_spot_list(conditions)

# %%




# %%
