
import os
import time
import datetime
from fastai.vision import *
import bitmex
import bitmex_delta
import aii.predict as predictor
import trader

def nice_wait(seconds):
    for i in range(seconds):
        time.sleep(1)
        print(seconds - i, end=' ', flush=True)
    print('')

def classify_price_movement(prediction):
    if abs(prediction) > 2:
        if prediction > 0:
            return "GOOD_UP"
        else:
            return "GOOD_DOWN"
    else:
        return "AROUND_ZERO"

while (True):

    os.system('python create_one_image.py')

    prediction_start_time = now_time = datetime.datetime.now(datetime.timezone.utc)
    price_in_beginning = bitmex_delta.get_current_price()
    print("Price right now: " + str(price_in_beginning))

    print("Making prediction based on image created (now.png)...")
    prediction = predictor.predict_image('now.png')
    convert_hack = str(prediction[0])
    predicted_price_diff = float(convert_hack[1:-1])

    print("Aii predicted price change for 1 minute: " + str(predicted_price_diff))
    predicted_movement_class = classify_price_movement(predicted_price_diff)
    print("That is in class of " + predicted_movement_class)
    trade = None
    if ("GOOD_UP" == predicted_movement_class):
        trade = trader.Trade(price_in_beginning)
        trade.trade_rise()
    elif ("GOOD_DOWN" == predicted_movement_class):
        trade = trader.Trade(price_in_beginning)
        trade.trade_fall()
    else:
        print("We are not going to trade this time.")

    nice_wait(60)

    price_1min_later = bitmex_delta.get_current_price()
    print("Price 1 minute later: " + str(price_1min_later))

    price_diff = price_1min_later - price_in_beginning
    print("Price difference: " + str(price_diff))

    if (trade):
        trade.close_trade(price_1min_later)
        print("")
    else:
        if (predicted_movement_class == classify_price_movement(price_diff)):
            right_or_wrong = 'RIGHT'
        else:
            right_or_wrong = 'WRONG'
        print("The current prediction was... " + right_or_wrong + "\n")


