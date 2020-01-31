import pandas as pd
from difflib import SequenceMatcher

THRESHOLD = 0.45

class Data:
    def __init__(self, path):
        self.dataframe = pd.read_csv(path)

    def similar(self, a, b):
        return SequenceMatcher(None, a, b).ratio()

    def get_entities(self, sentence):
        return { 'cadeira': self.get_cadeira(sentence) }

    def get_cadeira(self, sentence):
        disciplina_list = self.dataframe['disciplina'].tolist()
        entities = []
        for item in sentence.split():
            for d in disciplina_list:
                if self.similar(item, d) >= THRESHOLD:
                    entities.append(d)
        entities = list(set(entities))
        if len(entities) > 0:
            return entities[0]
        return None

    def get_value(self, cadeira, coluna):
        linha = self.dataframe[self.dataframe['disciplina'] == cadeira]
        return linha[coluna].to_string(index=False)
    
