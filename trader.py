
import bitmex_delta
import datetime

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
        print("TODO: execute BUY API command.")

    def trade_fall(self):
        self.rise = False
        print("################################################")
        print("### !!! We are going to SELL (short) now !!! ###")
        print("################################################")
        print("TODO: execute SELL API command.")

    def close_trade(self, exit_price):
        print("TODO: execute close of all trades")
        
        if (self.rise):
            profit = exit_price - self.start_price
        else:
            profit = self.start_price - exit_price

        print("############# >> Closed trade profit/loss: " + str(profit) + " <<")

        csv_row = datetime.datetime.now().isoformat() + "," + str(profit) + "\n"
        with open('trades.csv','a') as fd:
            fd.write(csv_row)

