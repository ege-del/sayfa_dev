import feedparser

import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '../../'))
import config
from db import is_visited,insert_news,register_visit,register_error
import helpers
# import config
# trying alternative names
# notice find_key dosent check for stricth match
# this means they key 'desc' will also catch 'description'
# source = ['author','source','organization','author']
# date = ['date','published','timestamp','time_stamp','updated','time']
# title = ['title','headline']
# subtitle = ['subtitle','desc']
# url = ['link','url']

# field_targets = {
#     "source":source,
#     "title":title,
#     "subtitle":subtitle,
#     "url":url,
#     "date":date,
# }

# def find_key(possibles: list,keys: list):
#     for i in keys:
#         for x in possibles:
#             # not a strict match
#             if x in i:
#                 return i
#     return None

def serialize(link: str,category):
    try:
        parse_res = feedparser.parse(link)

        feed_keys = parse_res.feed.keys()

        for entry in parse_res.entries:
            print(link)
            serialized_data = {
                "category":category,
                "page_type":"rss",
                "url":entry.link,
                "date":helpers.format_date(entry.get('published',None)),
                "title":entry.get('title',None),
                "subtitle":entry.get('description',None),
                "author":entry.get('author',None),
                "domain":helpers.get_domain(entry.link),
            }
            # for field in field_targets.keys():
            #     key_res = find_key(field_targets[field],feed_keys)
            #     # entry.get(key_res) is to fix inconsistent key values from the rss feed
            #     if key_res and entry.get(key_res):
            #         serialized_data[field] = entry[key_res]
            # print(ujson.dumps(serialized_data,indent=4))
            insert_news(serialized_data)        
    except Exception as e:
        print('ERR ',e)

