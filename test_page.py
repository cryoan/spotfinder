# %%

import asyncio

async def async_func(task_no):
    print(f'{task_no} :Velotio ...')
    await asyncio.sleep(1)
    print(f'{task_no}... Blog!')

async def main():
    taskA = asyncio.create_task(async_func('taskA'))
    taskB = asyncio.create_task(async_func('taskB'))
    taskC = asyncio.create_task(async_func('taskC'))
    await asyncio.wait([taskA,taskB,taskC])
   

await main()



# %%
import asyncio

async def async_func(task_no):
    print(f'{task_no} :Velotio ...')
    await asyncio.sleep(1)
    print(f'{task_no}... Blog!')

async def main():
    taskA = (async_func('taskA'))
    taskB = (async_func('taskB'))
    taskC = (async_func('taskC'))
    await asyncio.wait([taskA,taskB,taskC])
   

await main()

# %%
import aiohttp
import asyncio
import nest_asyncio
from bs4 import BeautifulSoup

nest_asyncio.apply()
class WebScraper(object):
    def __init__(self, urls):
        self.urls = urls
        # Global Place To Store The Data:
        self.all_data  = []
        self.master_dict = {}
        # Run The Scraper:
        asyncio.run(self.main())

    async def fetch(self, session, url):
        try:
            async with session.get(url) as response:
                # 1. Extracting the Text:
                text = await response.text()
                # 2. Extracting the  Tag:
                title_tag = await self.extract_title_tag(text)
                return text, url, title_tag
        except Exception as e:
            print(str(e))
            
    async def extract_title_tag(self, text):
        try:
            soup = BeautifulSoup(text, 'html.parser')
            return soup.title
        except Exception as e:
            print(str(e))

    async def main(self):
        tasks = []
        headers = {
            "user-agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"}
        async with aiohttp.ClientSession(headers=headers) as session:
            for url in self.urls:
                tasks.append(self.fetch(session, url))

            htmls = await asyncio.gather(*tasks)
            self.all_data.extend(htmls)

            # Storing the raw HTML data.
            for html in htmls:
                if html is not None:
                    url = html[1]
                    self.master_dict[url] = {'Raw Html': html[0], 'Title': html[2]}
                else:
                    continue

# 1. Create a list of URLs for our scraper to get the data for:
urls = ['https://understandingdata.com/', 'http://twitter.com/']
# 2. Create the scraper class instance, this will automatically create a new 
scraper = WebScraper(urls = urls)

# scraper.master_dict['https://understandingdata.com/']['Title']
# scraper.master_dict['https://understandingdata.com/']['Raw Html']
scraper.master_dict
# %%
