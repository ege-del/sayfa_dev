from datetime import datetime


def rank_newest(element):
    return element['date'].timestamp()


def rank(catergory: str,data:dict) -> dict:

    data.sort(key=rank_newest,reverse=True)
    index = 0
    for i in data:
        i['ranker_name'] = "newest"
        i['rank'] = index
        index += 1

    return data