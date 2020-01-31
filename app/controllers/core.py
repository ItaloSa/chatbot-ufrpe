import os
import urllib

from app.intel.model import Model

MODEL_URL = os.getenv('MODEL_DOWNLOAD_URL')
MODEL_PREPROC_URL = os.getenv('MODEL_PREPROC_URL')
MODELS_PATH = './app/models'
MODEL_PATH = f'{MODELS_PATH}/predictor'
MODEL_PREPROC_PATH = f'{MODELS_PATH}/predictor.preproc'
DATABASE_PATH = './app/data'
DATABASE_FILE_PATH = f'{DATABASE_PATH}/data.csv'
DATABASE_DOWNLOAD_URL = os.getenv('DATABASE_DOWNLOAD_URL')
DATA_PATH = './app/data/data.csv'

def setup():
    print('>> Setup')
    # if not os.path.exists(os.path.abspath(MODEL_PATH)):
    #     print('>> Download model')
    #     os.makedirs(MODELS_PATH)
    #     urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)
    #     urllib.request.urlretrieve(MODEL_PREPROC_URL, MODEL_PATH)
    # if not os.path.exists(os.path.abspath(DATABASE_PATH)):
    #     os.makedirs(DATABASE_PATH)
    #     urllib.request.urlretrieve(DATABASE_DOWNLOAD_URL, DATABASE_FILE_PATH)
    Model({'rnn':MODELS_PATH, 'data': DATA_PATH})

def handle(sentence):
    # predictor = ktrain.load_predictor('./intent.predictor')
    intent = get_intent(sentence)
    entities = Model().data.get_entities(sentence)
    print('sentence', sentence, intent, entities)
    return get_message(intent, entities)

def get_intent(sentence):
    return Model().RNN.predict(sentence)

def get_message(intent, entities):

    intents = {
        'duvida': ['', 'a Sua dúvida', ''],
        'pre_requisito': ['Pré-Requesitos', 'aos Pré-Requesitos', ''],
        'sala': ['sala', 'a Sala', ''],
        'ementa': ['Ementa', 'a Ementa', ''],
        'carga_horária': ['carga_horaria', 'a Carga Horária', 'horas'],
        'professor': ['docente', 'ao Docente', '']
    }

    intent = intents.get(intent, ['nao_entendi', 'Não entendi. Se quiser saber como posso te ajudar fale "o que você pode fazer"'])

    if intent[0] == 'nao_entendi':
        return intent[1]
    if intent[0] == 'duvida':
        return 'Você pode perguntar sobre: Pré requisito, sala, ementa, carga horária e o professor de uma disciplina. Lembre de escrever o nome certo, ainda não sou tão esperto'
    subject = entities['cadeira']
    data = Model().data.get_value(subject, intent[0])
    return f'Bom, referente a disciplina {subject} temos que {intent[1]} é:\n{data.strip()} {intent[2]}'
