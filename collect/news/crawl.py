"""
depth 1 crawl of links from mongo collection 'crawl_targets' where the field 'page_type' = 'news'
serialized results are inserted to collection 'news'
crawled links registered to collection 'link_index'
"""
import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '../'))

import requests
import time
import urllib

from html.parser import HTMLParser
from lxml import html
from lxml.etree import ParserError


from validate import validate_link,validate_data
from .serialize import serialize_page as serialize_page


from db import is_visited,insert_news,register_visit,register_error
import config
import helpers


def pull(link: str,category: str):
    if validate_link(link) == False:
        print('invalid link')
        return None

    try:
        page_content = requests.get(link, timeout=5).content
    except:
        print('request err')
        return None

    try:
        page_links = html.fromstring(page_content).xpath('//a/@href')
    except ParserError:
        print('parse err')
        return None
   
    print('crawling')
    for page_link in page_links:
        merged_link = urllib.parse.urljoin(link,page_link)
        if is_visited(merged_link) == False:
            if validate_link(merged_link):
                if helpers.get_domain(link) != helpers.get_domain(merged_link):
                    print("Skipping... Different Domain ")
                    continue

                print("Trying to Serialize ",merged_link)
                register_visit(merged_link)
                result = serialize_page(merged_link)
                
                if result:
                    # forcing date field on this crawler only
                    # non-article pages happend to have no date info
                    # without this filter filtering out bad pages is too much work

                    #TODO
                    #send parser info to inser_news then the validator and let validator skip this file
                    #if from crawl.py and date = None then return False
                    if result['date']:
                        print('Success')
                        result['category'] = category
                        result['url'] = merged_link
                        insert_news(result)
                    else:
                        print('Skipping because of no date')
                else:
                    print('Error Serializing')
                    register_error(merged_link)
            else:
                print("Invalid Link",merged_link)    
        else:
            print("Already Visited",merged_link)
    print('Sleeping')
    time.sleep(1)

