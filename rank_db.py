import pymongo
import sys
sys.path.insert(0,'../')
from collect import crawler_pull,rss_serialize,serialize_page
import config
import datetime
import rank as rank_manager
import filter as filter_manager
import helpers
# from pymongo import UpdateOne

mongo_cursor = pymongo.MongoClient(config.MONGO_URL)
collection = mongo_cursor[config.MONGO_DB_NAME]

categories = [x['name'] for x in collection[config.COL_CATEGORY].find({})]
print(categories)


rank_date_epocs = {
	'week-start':"",
	'debug':datetime.datetime(1970, 1, 1)
}

def init_dates():
    rank_date_epocs['week-start'] = datetime.datetime.today()  - datetime.timedelta(days=7)

def rank_all():
    rank_session = helpers.rand_hash()
    print('Ranking Documents from starting date; ',rank_date_epocs[config.RANK_DATE_EPOCH])
    for category in categories:
        res = list(collection[config.COL_NEWS_CONTENT].find({'date':{'$gte':rank_date_epocs[config.RANK_DATE_EPOCH]},'category':category}))
        for current_ranker in rank_manager.algos.keys():
            print("ranker [{}] category [{}]".format(current_ranker,category))
            res = rank_manager.algos[current_ranker](category,res)

        for current_filter in filter_manager.algos.keys():
            print("filter [{}] category [{}]".format(current_filter,category))
            res = filter_manager.algos[current_filter](category,res)
        
        query_list = list(map(lambda x : pymongo.UpdateOne({'_id':x['_id']},{'$set':{"rank."+x['ranker_name']:x['rank'],"filter."+x['filter_name']:x['filter'],'ranked_document':True,'rank_session':rank_session}}),res))
        if len(query_list) > 0:
            print('Ranked {} documents...'.format(len(query_list)))
            result = collection[config.COL_NEWS_CONTENT].bulk_write(query_list)


if __name__ == "__main__":
    init_dates()

    rank_all()
