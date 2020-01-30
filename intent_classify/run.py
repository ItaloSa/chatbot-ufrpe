from intent_classify import train_test_split, IntentClassify
import json

def database_from_json(path_file):
    file = open('database.txt')
    json_string = file.read().encode().decode('utf-8')
    dic = json.loads(json_string)
    file.close()
    return dic

database = database_from_json('database.txt')['database']
train_data, test_data = train_test_split(database)
classifier = IntentClassify(train_data, test_data)
predictor = classifier.getPredictor()

print(predictor.predict('como posso dispensar ESO'))
