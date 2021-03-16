from flask import Flask, render_template, send_from_directory, request
import pymongo
import datetime
import config

import rank as rank_manager

category_cache = None

app = Flask(__name__,
            static_url_path='',
            template_folder='./templates/',
            static_folder='./static'
            )
mongo_cursor = pymongo.MongoClient(config.MONGO_URL)
collection = mongo_cursor[config.MONGO_DB_NAME]

# categories = list(map(lambda x : x['name'],collection["categories"].find({})))


@app.route("/api/category", methods=['GET'])
def category():
    global category_cache
    if category_cache == None:
        category_cache = [x['name'] for x in collection[config.COL_CATEGORY].find({})]
    print('returnin',category_cache)
    return {"data":category_cache}


@app.route("/api/news", methods=['GET'])
def news():
    #TODO fix
    # this is not using info from config.py
    print(request.args)
    query_date_range = datetime.datetime.today()  - datetime.timedelta(days=7)
    news = collection[config.COL_NEWS_CONTENT]
    sort_by = 'rank.'+request.args['rank_algorithm']
    sort_order = pymongo.DESCENDING if request.args['reverse_order'] == "yes" else pymongo.ASCENDING
    fetch = int(request.args['fetch'])

    query = {
            #find
            'date':
                {'$gte'             : query_date_range},
                'domain'            : {'$exists': 1},
                'date'              : {'$exists': 1},
                "ranked_document"   : True
            }
    project = {
            '_id': 0,
            'subtitle': 0
            }
    
    data_bundle = {}
    for i in request.args['category'].split(','):
        query['category'] = i
        res = news.find(query,project).sort(sort_by,sort_order).limit(fetch)
        print(res)
        data_bundle[i] = list(res)

    # data = rank_manager.algos[request.args['rank_algorithm']](data_bundle)
    return {"data": data_bundle}


app.config['TEMPLATES_AUTO_RELOAD'] = True


@app.route('/news')
@app.route('/')
def hello_world():
    return render_template('index.html')
