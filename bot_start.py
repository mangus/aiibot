
import os
import datetime
from fastai.vision import *
import bitmex
import bitmex_delta
import aii.predict as predictor
import trader
import sys
import config

def classify_price_movement(prediction):
    if abs(prediction) > config.good_price_movement:
        if prediction > 0:
            return "GOOD_UP"
        else:
            return "GOOD_DOWN"
    else:
        return "AROUND_ZERO"

bitmex.print_wallet()
while (True):

    print("")
    os.system('python create_one_image.py')

    prediction_start_time = now_time = datetime.datetime.now(datetime.timezone.utc)
    price_in_beginning = bitmex_delta.get_current_price()
    print("Price right now: " + str(price_in_beginning))

    predicted_price_diff = predictor.predict_image('now.png')
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
        print("We are not going to trade; waiting ~7 seconds...")
        trader.nice_wait(7, only_price=True)
        price_diff = bitmex_delta.get_current_price() - price_in_beginning

    sys.stdout.flush()

