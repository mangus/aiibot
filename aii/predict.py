
from fastai.vision import *
learn = load_learner("./aii/")

def predict_image(path):
    img = open_image(path)
    return learn.predict(img)
