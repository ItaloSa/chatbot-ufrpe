import json

def database_from_json(path_file):
    file = open('database.txt')
    json_string = file.read().encode().decode('utf-8')
    dic = json.loads(json_string)
    file.close()
    return dic