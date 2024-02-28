import pickle
import numpy as np

class Model:
    def __init__(self,img):
        self.img = img

    def load_model(self):
        # Load model saved from the pickle
        loaded_pickle_model = pickle.load(open("hand_writing_detection_model.pkl","rb"))
        return loaded_pickle_model

    def predictor(self, loaded_model):
        letter_prediction = loaded_model.predict(self.img)
        return letter_prediction