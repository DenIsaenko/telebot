import json

import requests
import json
def get_json(param):
    url = "https://aliexpress-datahub.p.rapidapi.com/item_search_2"
    querystring = {"q": param, "page": "1"}
    headers = {
        "X-RapidAPI-Key": "36ca46681fmsh384e994b5a825e4p119902jsn88ce1252c883",
        "X-RapidAPI-Host": "aliexpress-datahub.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring).text
    json_prod = json.loads(response)
    return json_prod
