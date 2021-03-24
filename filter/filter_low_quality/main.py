# binary filter
# to complement ranker
import random

def title_filter(data) -> int:
    #mockup
    return random.randint(0,1)


def _filter(category: str,data: list) -> list:
    for i in data:
        i['filter_name'] = "low_quality"
        i['filter'] = title_filter(i['title'])
    return data