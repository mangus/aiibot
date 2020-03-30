
import bitmex
import bitmex_delta
import datetime
import time
import os
import aii.predict as predictor
import config
import sys

class Trade:

    rise = True
    start_price = 0

    def __init__(self, start_price):
        self.start_price = start_price

    def trade_rise(self):
        self.rise = True
        print("##############################################")
        print("### !!! We are going to BUY (long) now !!! ###")
        print("##############################################")
        bitmex.trade_buy(self.start_price)
        self.wait_for_trade_close()

    def trade_fall(self):
        self.rise = False
        print("################################################")
        print("### !!! We are going to SELL (short) now !!! ###")
        print("################################################")
        bitmex.trade_sell(self.start_price)
        self.wait_for_trade_close()

    def close_trade(self, exit_price):
        
        if (self.rise):
            bitmex.close_buy_trade()
            profit = exit_price - self.start_price
        else:
            bitmex.close_sell_trade()
            profit = self.start_price - exit_price

        print("### Price diff in this trade was: " + str(exit_price - self.start_price))
        print("### Closed trade theoretical profit/loss without fees and stop-losses: " + str(profit * config.one_trade_amount))
        print("################################################")

        wallet_info = bitmex.get_wallet_info()
        a_row = datetime.datetime.now().isoformat() + ": " + str(wallet_info['walletBalance'] / 100000000) + " BTC\n"
        with open('wallet.log','a') as fd:
            fd.write(a_row)

    def wait_for_trade_close(self):
        print("### Now we check the market every ~60 seconds and find a good exit point... ###")
        exit_trade = False
        no_another_close = False
        while (not exit_trade):
            nice_wait(56) # Leave some time for calculations, that's why 56 instead of 60
            if bitmex.position_is_open():
                os.system('python create_one_image.py')
                predicted_price_diff = predictor.predict_image('now.png')
                print("### Aii predicted price change for 1 minute: " + str(predicted_price_diff))
                print("### Price checkpoint: " + str(bitmex_delta.get_current_price()))
                if self.rise:
                    if predicted_price_diff > 0:
                        print("### Still expecting a rise, staying in this trade another ~60 seconds...")
                    else:
                        print("### Expecting a price fall, exiting this trade now...")
                        exit_trade = True
                else:
                    if predicted_price_diff < 0:
                        print("### Still expecting a fall, staying in this trade another ~60 seconds...")
                    else:
                        print("### Expecting a price rise, exiting this trade now...")
                        exit_trade = True
            else:
                print("### Trade was automatically exited by stop-loss order!")
                print("######################################################")
                exit_trade = True
                no_another_close = True

            sys.stdout.flush()

        if (not no_another_close):
            self.close_trade(bitmex_delta.get_current_price())

def nice_wait(seconds, only_price=False):
    start_price = bitmex_delta.get_current_price()
    for i in range(seconds):
        time.sleep(1)
        price_diff = bitmex_delta.get_current_price() - start_price
        if price_diff > 0:
            add_plus = "+"
        else:
            add_plus = ""

        if only_price:
            print_this = add_plus + str(price_diff) + "$"
        else:
            print_this = str(seconds - i) + "|" + add_plus + str(price_diff) + "$"

        print(print_this, end=' ', flush=True)
    print('')

