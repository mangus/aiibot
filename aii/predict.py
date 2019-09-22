
from fastai.vision import *
learn = load_learner("./aii/")

def predict_image(path):
    img = open_image(path)
    prediction = learn.predict(img)
    convert_hack = str(prediction[0])
    predicted_price_diff = float(convert_hack[1:-1])
    return predicted_price_diff
