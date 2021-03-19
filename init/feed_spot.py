"""
feed spot provides list of rss feeds based on a category
this script turns the page into rss links and inserts it to mongo
"""
import requests
from lxml import html
import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '../'))
import config
import pymongo
import time

from collect.rss.rss import serialize as serialize_rss

from urllib import parse

mongo_cursor = pymongo.MongoClient(config.MONGO_URL)
collection = mongo_cursor[config.MONGO_DB_NAME]

#test
links = [
"https://blog.feedspot.com/genetics_rss_feeds/,genetics",
"https://blog.feedspot.com/neuroscience_blogs/,neuroscience",
"https://blog.feedspot.com/neuroscience_podcasts/,neuroscience",
"https://blog.feedspot.com/chemistry_websites/,chemistry",
"https://blog.feedspot.com/dna_blogs/,genetics",
]

for row in links:
    page_content = requests.get(row.split(',')[0], timeout=10).content
    
    rss_links = html.fromstring(page_content).xpath("//a[contains(concat(' ',normalize-space(@class),' '),'frss')]/@href")
    for i in rss_links:
        link_clean = parse.unquote(i.split('site:')[1])
        res = collection[config.COL_CRAWL_TARGET].find_one({"link":link_clean})
        if res == None:
            print(link_clean)
            collection[config.COL_CRAWL_TARGET].insert(
                {
                    "link":link_clean,
                    "category":row.split(',')[1],
                    "page_type":"rss"
                }
            )
        else:
            print('record exists.')

    time.sleep(1)