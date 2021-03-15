import pymongo
import validate
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../'))
import config
import helpers
import datetime
from validate import validate_data
mongo_cursor = pymongo.MongoClient(config.MONGO_URL)
collection = mongo_cursor[config.MONGO_DB_NAME]

def is_visited(link: str):
    res = collection[config.COL_LINK_INDEX].find(
        {
        "domain":helpers.get_domain(link),
        "links":{"$in":[link]}
        }
    )
    if res.count() > 0:
        return True
    else:
        return False

def add_link(url,category,page_type):
    print(url,category,page_type)

def register_error(link):
    print('Register Error',link)

def register_visit(link: str):
    print('Register ',link)
    domain = helpers.get_domain(link)
    collection[config.COL_LINK_INDEX].update_one({"domain":domain},{"$push":{"links":link}},upsert=True)

def fill_data(news_data: dict):
    if not news_data.get('date'):
        news_data['date'] = str(datetime.datetime.utcnow())
    if not news_data.get('domain'):
        news_data['domain'] = helpers.get_domain(news_data['url'])
        
    return news_data

def insert_news(news_data: dict):
    # print(news_data)
    # validate here

    if validate_data(news_data):
        print('Data Validated')
        
        news_data = fill_data(news_data)

        collection[config.COL_NEWS_CONTENT].insert_one(news_data)
    else:
        print('Invalid Data')
