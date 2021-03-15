"""
serializes data from html page's 'meta' tags

"""

import requests
import random

from html.parser import HTMLParser
from lxml import html
from lxml.etree import ParserError

import time

def serialize_page(link: str):
    headers = {'User-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{}.0.{}.61 Safari/537.36'.format(random.randint(60,83),random.randint(3500,4000))}
    
    page_content = requests.get(link,headers=headers).content
    page_tree = html.fromstring(page_content)
    
    data = {}
    fields = [
            ['title','og:title'],
            ['description','og:description'],
            ['site_name','og:site_name'],
            ['published_time','article:published_time']
            ]
    for i in fields:
        buffer = page_tree.xpath("//head/meta[@property='{}']/@content".format(i[1]))
        if len(buffer) > 0:
            data[i[0]] = buffer[0]
    # if data.get('title') and data.get('published_time'):
    return data
    # else:
        # None
