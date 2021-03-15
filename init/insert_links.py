import pymongo
import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '../'))
import config

mongo_cursor = pymongo.MongoClient(config.MONGO_URL)
future_news = mongo_cursor[config.MONGO_DB_NAME]

links = []
for i in config.LINK_PATH_LIST:
    print(i)
    links += open(i,'r',encoding='utf-8').read().split('\n')

collection = future_news[config.COL_CRAWL_TARGET]

for i in links:
    print(i)
    cat_arr = i.split(',')
    if collection.find_one({"link":cat_arr[0]}) == None:
        print(cat_arr[0])
        collection.insert_one({
            "link":cat_arr[0],
            "category":cat_arr[1],
            "page_type":cat_arr[2]
        })
    else:
        print('record exits')

