import sys
import pymongo
import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '../'))
import config

mongo_cursor = pymongo.MongoClient(config.MONGO_URL)
category_collection = mongo_cursor[config.MONGO_DB_NAME][config.COL_CATEGORY]

category_arr = []
for i in config.CATEGORY_PATH_LIST:
    print(i)
    category_arr += open(i,'r',encoding='utf-8').read().split('\n')

for i in category_arr:
    if category_collection.find_one({"name":i}) == None:
        category_collection.insert_one({"name":i,})
    else:
        print('record exits')

