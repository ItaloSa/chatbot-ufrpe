from random import shuffle
import ktrain
import os.path

def train_test_split(data, test_size=.3):
		train = []
		test = []
		for classe in data:
			s = classe['sentencas']
			shuffle(s)
			train.append({'classe': classe['classe'], 'sentencas': s[int(len(classe['sentencas'])*test_size):]})
			test.append({'classe': classe['classe'], 'sentencas': s[0:int(len(classe['sentencas'])*test_size)]})
		return train, test

class IntentClassify:

	def __init__(self, training_data, test_data):
		self.training_data = training_data
		self.test_data = test_data
		self.classes = list(set([a['classe'] for a in training_data]))

	def getPredictor(self):
		if os.path.exists('/temp/intent.predictor'):
			return ktrain.load_predictor('/temp/intent.predictor')

		x_train, y_train, x_test, y_test = [], [], [], []
		for classe in self.training_data:
		    for sentenca in classe['sentencas']:
		        y_train.append(self.classes.index(classe['classe']))
		        x_train.append(sentenca)

		for classe in self.test_data:
		    for sentenca in classe['sentencas']:
		        y_test.append(self.classes.index(classe['classe']))
		        x_test.append(sentenca)

		array = ktrain.text.texts_from_array(
			x_train=x_train, y_train=y_train,
			x_test=x_test, y_test=y_test,
			class_names=self.classes,
			preprocess_mode='bert',
			lang='pt',
			maxlen=350,
			max_features=35000
        )
		(x_train,  y_train), (x_test, y_test), preproc = array

		model = ktrain.text.text_classifier('bert', train_data=(x_train, y_train), preproc=preproc)
		learner = ktrain.get_learner(model, train_data=(x_train, y_train), batch_size=6)

		learner.fit_onecycle(2e-5, 4)

		learner.validate(val_data=(x_test, y_test), class_names=self.classes)

		predictor = ktrain.get_predictor(learner.model, preproc)
		
		predictor.save('/temp/predictor')

		return predictor