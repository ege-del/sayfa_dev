import tldextract
from dateutil.parser import parse as date_parse
import random

def rand_hash():
    return "%16x" % random.getrandbits(64)

def format_date(date : str):
    if date == None:
        return None
    return date_parse(date)

def get_domain(link: str):
    return tldextract.extract(link).domain

