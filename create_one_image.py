
import requests
import time
import datetime
import sys
import random
import plotter
import bitmex
import bitmex_delta

print("Creating one picture (data from right now)...")

start_datetime = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=24)

print("%s" % (start_datetime.isoformat()))
sys.stdout.flush()

data_1day = bitmex.get_1day_data(start_datetime, print_info=True)

start_1hour_datetime = start_datetime + datetime.timedelta(hours=23)
data_1hour = bitmex.get_1hour_data(start_1hour_datetime, print_info=True)

#start_5minutes_datetime = start_1hour_datetime + datetime.timedelta(minutes=55)
#data_5minutes_all = bitmex.get_5minutes_all_data(start_5minutes_datetime)
data_5minutes_all = bitmex_delta.get_last_5minutes()

plotter.plot_one_image(data_1day, data_1hour, data_5minutes_all, 'now.png', start_datetime)

print("Picture (now.png) created!")

sys.exit()
