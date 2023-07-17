a = [('c', 'd', 2), ('m', 'b', 4), ('h', 'f', 1)]
print(sorted(a, key=lambda i: i[2]))


import requests
import json
def get_json(param):
    url = "https://aliexpress-datahub.p.rapidapi.com/item_search_2"
    querystring = {"q": param, "page": "1"}
    headers = {
        "X-RapidAPI-Key": "ff618643f6msh2edfb56ebed1800p1a6e05jsn77b6a6d78ae2",
        "X-RapidAPI-Host": "aliexpress-datahub.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring).text
    json_prod = json.loads(response)
    return json_prod


user_input = get_json('iphone')
print(user_input)
resLST = user_input['result']['resultList']
titels = list(map(lambda x: (x['item']['title'],
                             x['item']['itemUrl'],
                             x['item']['sales']/x['item']['sku']['def']['promotionPrice']), resLST))
led = sorted(titels, key=lambda i: i[2], reverse=True)
print('\n'.join(led[0][:2]))
titels = list(map(lambda x: x['item']['title'], resLST))
print(titels)










