
def rank_shortest(data):
    return len(data['title'])


def rank(cateogry: str,data:dict) -> dict:

    data.sort(key=rank_shortest)
    index = 0
    for i in data:
        i['ranker_name'] = "shortest"
        i['rank'] = index
        index += 1

    return data