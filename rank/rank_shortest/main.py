
def shortest_rank(data):
    return len(data['title'])


def rank(data:dict) -> dict:

    for i in data.keys():
        data[i].sort(key=shortest_rank)
        index = 0
        for x in data[i]:
            x['rank'] = index
            index += 1

    return data