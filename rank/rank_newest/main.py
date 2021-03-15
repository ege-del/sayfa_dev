from datetime import datetime


def shortest_rank(data):
    return data['date'].timestamp()


def rank(data:dict) -> dict:

    for i in data.keys():
        data[i].sort(key=shortest_rank,reverse=True)
        index = 0
        for x in data[i]:
            x['rank'] = index
            index += 1

    return data