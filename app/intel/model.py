# import ktrain
from app.intel.rnn_classify import RNNClassify
from app.intel.data import Data

class Model:
    class __sigleton:
        def __init__(self, path):
            self.path = path
            #self.BERT = ktrain.load_predictor(path)
            self.RNN = RNNClassify(path['rnn'])
            self.RNN.load_model()
            self.data = Data(path['data'])
        def __str__(self):
            return repr(self) + self.path
    instance = None
    def __init__(self, path=None):
        if not Model.instance:
            if not path:
                raise 'require path'
            Model.instance = Model.__sigleton(path)
    def __getattr__(self, name):
        return getattr(self.instance, name)