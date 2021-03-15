import pymongo
import sys
sys.path.insert(0,'../')
from collect import crawler_pull,rss_serialize,serialize_page
import config
import datetime
import rank as rank_manager
import random
# from pymongo import UpdateOne

mongo_cursor = pymongo.MongoClient(config.MONGO_URL)
collection = mongo_cursor[config.MONGO_DB_NAME]

# not ready
# for i in collection[config.COL_CRAWL_TARGET].find({"page_type":"news"},{'_id':0}):
#     print(i)
#     crawler_pull(i['link'],i['category'])

for i in collection[config.COL_CRAWL_TARGET].find({'page_type':'rss'}):
    print(i)
    rss_serialize(i['link'],i['category'])