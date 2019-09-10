
import requests
import time
import datetime
import sys
import random
import plotter
import bitmex

print("Creating one picture (data from right now)...")

start_datetime = datetime.datetime.now() - datetime.timedelta(hours=24) \
    - datetime.timedelta(hours=3) # timezone difference

print("%s" % (start_datetime.isoformat()))
sys.stdout.flush()

data_1day = bitmex.get_1day_data(start_datetime)
start_1hour_datetime = start_datetime + datetime.timedelta(hours=23)
data_1hour = bitmex.get_1hour_data(start_1hour_datetime)

data_5minutes_all = bitmex.get_5minutes_all_data(start_1hour_datetime)

model_start_datetime = start_datetime + datetime.timedelta(hours=3)
plotter.plot_one_image(data_1day, data_1hour, data_5minutes_all, 'now.png', model_start_datetime)

sys.exit()
