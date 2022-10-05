# %%
import windguru_scraper as windguru_scraper
import maree_info_scraper
import multiprocessing
from multiprocessing import Process

def func1():
  print ('func1: starting')
  for i in range(10000000): pass
  print ('func1: finishing')
  return 1

def func2():
  print ('func2: starting')
  for i in range(10000000): pass
  print ('func2: finishing')
  return 2

def worker(procnum, return_dict):
    """worker function"""
    print(str(procnum) + " represent!")
    return_dict[procnum] = procnum


def worker1(queue):
    ret = queue.get()
    ret['foo'] = True
    queue.put(ret)

def worker2(queue):
    ret = queue.get()
    ret['baz'] = True
    queue.put(ret)
  
conditions={}
def scrape_windguruOld(queue):
    conditions = queue.get()
    conditions_windguru= windguru_scraper.main()
    print("conditions_windguru",conditions_windguru)
    conditions["conditions_windguru"]=conditions_windguru
    queue.put(conditions)

    # return conditions_windguru

def scrape_maree_infoOld(queue):
    conditions = queue.get()
    conditions_maree_info= maree_info_scraper.main()
    conditions["conditions_maree_info"]=conditions_maree_info
    print("conditions_maree_info", conditions_maree_info)
    # return conditions_maree_info
    queue.put(conditions)

def scrape_windguru(conditions):
    conditions_windguru= windguru_scraper.main()
    conditions["conditions_windguru"]=conditions_windguru
    print("conditions_windguru",conditions_windguru)

    # return conditions_windguru

def scrape_maree_info(conditions):
    conditions_maree_info= maree_info_scraper.main()
    conditions["conditions_maree_info"]=conditions_maree_info
    print("conditions_maree_info", conditions_maree_info)

# async def scrape_windguru_async():
#     conditions_windguru= await windguru_scraper.main()
#     # conditions["conditions_windguru"]=conditions_windguru
#     print("conditions_windguru",conditions_windguru)
#     return conditions_windguru

# async def scrape_maree_info_async():
#     conditions_maree_info= await maree_info_scraper.main()
#     # conditions["conditions_maree_info"]=conditions_maree_info
#     print("conditions_maree_info", conditions_maree_info)
#     return conditions_maree_info

def scrape_conditions(conditions_windguru,conditions_maree_info):
    conditions={"conditions_windguru":conditions_windguru, "conditions_maree_info":conditions_maree_info}
    print("conditions", conditions)
    return conditions

def get_conditons():
    return conditions

if __name__ == '__main__':
    # conditions_windguru= scrape_windguru
    # conditions_maree_info=scrape_maree_info
    queue = multiprocessing.Queue()
    queue.put(conditions)
    p1 = Process(target=scrape_windguru,args=(queue,))
    p1.start()
    p2 = Process(target=scrape_maree_info,args=(queue,))
    p2.start()
    p1.join()
    p2.join()
    print("conditions", conditions)
    # conditions= scrape_conditions(conditions["conditions_windguru"], conditions["conditions_maree_info"])
   
# %%
