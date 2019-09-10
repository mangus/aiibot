
import os
import time
import datetime
from fastai.vision import *
import bitmex
import aii.predict as predictor

while (True):

    os.system('python create_one_image.py')

    prediction_start_time = now_time = datetime.datetime.now() - datetime.timedelta(hours=3) # timezone
    price_in_beginning = bitmex.get_current_price()
    print("Price right now: " + str(price_in_beginning))

    prediction = predictor.predict_image('now.png')
    print(prediction)

    print("Aii prediction for 1 minute: " + str(prediction[0]))
    time.sleep(60)

    price_1min_later = bitmex.get_current_price()
    print("Price 1 minute later: " + str(price_1min_later))

    price_diff = price_1min_later - price_in_beginning
    print("Price difference: " + str(price_diff))

    if (str(prediction[0]) == 'UP'):
        if (price_1min_later > price_in_beginning):
            right_or_wrong = 'RIGHT'
            reality = 'UP'
        else:
            right_or_wrong = 'WRONG'
            reality = 'DOWN'
    else: # DOWN
        if (price_1min_later <= price_in_beginning):
            right_or_wrong = 'RIGHT'
            reality = 'DOWN'
        else:
            right_or_wrong = 'WRONG'
            reality = 'UP'
    print("The current prediction was... " + right_or_wrong + "\n")

    csv_row = prediction_start_time.isoformat() + "," + str(price_in_beginning) + "," + str(price_1min_later) + "," + str(price_diff) + "," \
         + str(prediction[0]) + "," + reality + "," + right_or_wrong + "\n"
    with open('predictions.csv','a') as fd:
        fd.write(csv_row)


