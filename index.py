# %%
from flask import Flask, render_template, request
from hello import Hello
from spot_finder import Spot_Finder

from flask_navigation import Navigation
import windguru_scraper as windguru_scraper
# import maree_info_scraper
# import conditions_scraper
from multiprocessing import Process

import multiprocessing
import conditions_scraper as cs
import time
import asyncio


"""
main module to display best water sport option
run with: "flask --app app.py --debug run"
"""
 
#initiate app
app = Flask(__name__)
nav = Navigation(app)

nav.Bar('top', [
    nav.Item('conditions', 'surf_condition'),
    nav.Item('spots', 'find_spot_list'),

])

#define objects needed for each page/module
# conditions_windguru= windguru_scraper.main()
# conditions_maree_info= maree_info_scraper.main()
# conditions={"conditions_windguru":conditions_windguru, "conditions_maree_info":conditions_maree_info}
# print("conditions", conditions)

# conditions=conditions_scraper.conditions



def get_conditions():
    '''return conditions dict from windguru and maree info scraping scraping 
    use multiprocessing to speed up the scraping
    
    '''
    start_time= time.time()
    manager = multiprocessing.Manager()
    conditions = manager.dict()

    p1 = multiprocessing.Process(target=cs.scrape_windguru, args=(conditions,))
    p2 = multiprocessing.Process(target=cs.scrape_maree_info, args=(conditions,))
    p1.start()
    p2.start()
    jobs=[p1, p2]
    for proc in jobs:
        proc.join()
    result= conditions
    print("result", result)
    duration = time.time()-start_time
    print(f"duration to conditions scraping: %.2f s" %duration)
    return conditions




# async def get_conditions_async():
#     start_time= time.time()
#     mi_task= asyncio.create_task(cs.scrape_maree_info_async())
#     wg_task=  asyncio.create_task(cs.scrape_windguru_async())

#     done, pending= await asyncio.wait([mi_task,wg_task])
#     print("done", done)
#     conditions= cs.scrape_conditions(done, pending)
#     duration = time.time()-start_time
#     print(f"duration: %.2f s" %duration)
#     print("conditions", conditions)
#     return conditions

@app.route("/")
def welcome():
    # return hello.sayHello()
    return render_template('home.html', nav=nav)

# @app.route("/conditions")
# def surf_condition():
#     return render_template('conditions.html', conds=conds)

# @app.route('/conditions', methods=['POST'])
# def my_form_post():
#     text = request.form['text']
#     processed_text = text.upper()
#     return processed_text

# @app.route("/spot")
# def find_spot():
#     return spot_finder.get_best_spot(conditions=conditions)

# conditions= await get_conditions_async()

@app.route("/spotdate")
def find_spot_list():
   
    # return spot_finder.get_best_spot_list(conditions=conditions)
    conditions=get_conditions()
    spot_finder= Spot_Finder(conditions)
    # conditions=await get_conditions_async()
    best_spots_list=spot_finder.get_best_spot_list()
    return render_template("spots.html",best_spots_list=best_spots_list, color="red" )



# @app.route("/quit")
# def Bye_friend():
#     return hello.sayBye()

# print("main outside")
# if __name__=='__main__':
#     print("main inside")
#     conditions_windguru= windguru_scraper.main()
#     conditions_maree_info= maree_info_scraper.main()
#     conditions={"conditions_windguru":conditions_windguru, "conditions_maree_info":conditions_maree_info}
#     print("conditions", conditions)

#     spot_finder= Spot_Finder()





if __name__ == '__main__':
    get_conditions()
#    await get_conditions_async()
    # await find_spot_list()


# %%
