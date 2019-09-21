
import bitmex
import datetime
import time

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

    def trade_fall(self):
        self.rise = False
        print("################################################")
        print("### !!! We are going to SELL (short) now !!! ###")
        print("################################################")
        bitmex.trade_sell(self.start_price)

    def close_trade(self, exit_price):
        
        if (self.rise):
            bitmex.close_buy_trade()
            profit = exit_price - self.start_price
        else:
            bitmex.close_sell_trade()
            profit = self.start_price - exit_price

        print("############# Closed trade theoretical profit/loss without fees: " + str(profit))
        print("############# Wallet balance right now: >> " + str(bitmex.bitcoin_count_in_wallet() / 100000000) + " BTC <<")

        csv_row = datetime.datetime.now().isoformat() + "," + str(profit) + "\n"
        with open('trades.csv','a') as fd:
            fd.write(csv_row)


