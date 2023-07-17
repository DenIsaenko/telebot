import json
import os.path

def write_func(path, info):
    with open(path, 'w', encoding='utf8') as file:
        json.dump(info, file, indent=4)

def read_func(path):
    with open(path, 'r', encoding='utf8') as file:
        data = json.load(file)
        return data
