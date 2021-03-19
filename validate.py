"""
validate data
"""
import config
import helpers

def validate_link(link):
    if "http" not in link:
        return False
    if link[0] == "#":
        return False

    return True

# wip
def match(text,word_array):
    matched = []
    matches = 0
    text_arr = text.lower().split()
    print(text_arr)
    print(word_array)
    for i in text_arr:
        if i not in matched and i in word_array:
            print('match '+i)
            matched.append(i)
            matches+=1
    return matches / len(text_arr)


required_keys = config.REQUIRED_NEWS_FIELDS

def validate_data(data: dict):
    if not data:
        return False
    for k in required_keys:
        if not data.get(k):
            return False

    # sketch
    # match_res =match(data['title'],category_data['word_list'])
    # print(match_res)
    # if match_res < 0.35:
    #     return False

    return True

