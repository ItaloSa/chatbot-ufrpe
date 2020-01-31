import tflearn
import tensorflow as tf
import pickle
import nltk
from nltk.stem.lancaster import LancasterStemmer
import numpy as np

class RNNClassify:
    def __init__(self, path):
        self.path = path
        self.load_model()

    def load_model(self):
        nltk.download('punkt')
        self.data = pickle.load(open(self.path+'/training_data', 'rb'))
        num_neurons_per_layer = [8, 8]
        num_inner_layers = len(num_neurons_per_layer)
        activation = 'softmax'
        num_epoch = 1000
        tf.reset_default_graph()
        net = tflearn.input_data(shape=[None, len(self.data['train_x'][0])])
        for l in range(num_inner_layers):
            net = tflearn.fully_connected(net, num_neurons_per_layer[l])
        net = tflearn.fully_connected(net, len(self.data['train_y'][0]), activation=activation)
        net = tflearn.regression(net)
        self.model = tflearn.DNN(net)
        self.model.load(self.path+'/model.tflearn')

    def clean_up_sentence(self, sentence):
        stemmer = LancasterStemmer()
        # Tokeniza o padrão
        sentence_words = nltk.word_tokenize(sentence)
        # Aplica stemming para cada palavra
        sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
        return sentence_words

    # Retorna um array representando a sentença em: 0 or 1 para 
    # cada palavra do bloco (words) que existe na sentença
    def __bow(self, sentence, show_details=False):
        # Tokeniza o padrão
        sentence_words = self.clean_up_sentence(sentence)
        # Inicializa o bloco de palavras
        block = [0]*len(self.data['words'])
        for s in sentence_words:
            for i,w in enumerate(self.data['words']):
                if w == s: 
                    block[i] = 1
                    if show_details:
                        print ("found in block: %s" % w)
        return(np.array(block))

    # Recebe a intenção e um limiar para filtrar as predições
    # Retorna uma lista com a probabilidade de cada intenção
    def __get_prob_intentions(self, sentence, threshold=0.6):
        treated = self.__bow(sentence)
        prediction = self.model.predict([treated]).flatten()
        sorted_intent_predict = sorted(zip(prediction, self.data['classes']), key=lambda e: e[0], reverse=True)
        return list(filter(lambda e: e[0] > threshold, sorted_intent_predict))

    # Retorna uma resposta baseado na intenção
    def __get_response(self, sentence):
        prob_intentions = self.__get_prob_intentions(sentence)
        if len(prob_intentions) == 0: return ''
        highest = prob_intentions[0]
        confidence, intention = highest
        return intention
    
    def predict(self, sentence):
        return self.__get_response(sentence)