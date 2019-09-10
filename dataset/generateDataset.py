
# Natuke läbu kood siin... TODO better

import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import requests
import time
import datetime
import sys
import random
import math

def make_ticklabels_invisible(fig):
    for i, ax in enumerate(fig.axes):
        ax.text(0.5, 0.5, "ax%d" % (i+1), va="center", ha="center")
        for tl in ax.get_xticklabels() + ax.get_yticklabels():
            tl.set_visible(False)

print("Aii v2 will rule the wooorld! Creating dataset...")

start_datetime = datetime.datetime(2019, 1, 1, 0, 0, 0)
while (True):

    print("")
    print("%s" % (start_datetime.isoformat()))
    sys.stdout.flush()
    
    # for 1 day graph
    url = "https://www.bitmex.com/api/v1/trade/bucketed?binSize=5m&partial=false&symbol=XBT&count=288&startTime=" + start_datetime.isoformat()
    print(url)
    r = requests.get(url)
    data_1day = r.json()
    
    plot_1day_x = plot_1day_y = []
    min_1day = sys.maxsize
    max_1day = -sys.maxsize
    for index, trade_point in enumerate(data_1day, start=0):
        price = trade_point['close']
        plot_1day_x = plot_1day_x + [index]
        plot_1day_y = plot_1day_y + [price]
        if price < min_1day:
            min_1day = price
        if price > max_1day:
            max_1day = price

    # 1 hour
    start_1hour_datetime = start_datetime + datetime.timedelta(hours=23)
    url = "https://www.bitmex.com/api/v1/trade/bucketed?binSize=1m&partial=false&symbol=XBT&count=61&startTime=" + start_1hour_datetime.isoformat()
    print(url)
    r = requests.get(url)
    data_1hour = r.json()
    
    plot_1hour_x = plot_1hour_y = []
    min_1hour = sys.maxsize
    max_1hour = -sys.maxsize
    for index, trade_point in enumerate(data_1hour, start=0):
        if (index < 60): # Last value is ML dependent variable
            price = trade_point['close']
            plot_1hour_x = plot_1hour_x + [index]
            plot_1hour_y = plot_1hour_y + [price]
            if price < min_1hour:
                min_1hour = price
            if price > max_1hour:
                max_1hour = price
    
    # 5 minutes, different query from BitMex
    start_5minutes_datetime = start_1hour_datetime + datetime.timedelta(minutes=55)
    end_5minutes_datetime = start_5minutes_datetime + datetime.timedelta(minutes=5)
    
    have_all_data = False
    start = 0
    data_5minutes_all = []
    while (not have_all_data):
    
        url = "https://www.bitmex.com/api/v1/trade?symbol=XBT&count=500&columns=price&startTime=" + start_5minutes_datetime.isoformat() \
          + "&endTime=" + end_5minutes_datetime.isoformat() + "&start=" + str(start)
        print(url)
        
        r = requests.get(url)
        one_query_data = r.json()
        data_5minutes_all.append(one_query_data)
        
        if len(one_query_data) < 500:
            have_all_data = True
        elif len(one_query_data) == 500:
            start += 500
            # and make another query
        else:
            print("WTF, error.")
            sys.exit()
    
    plot_5minutes_x = plot_5minutes_y = []
    min_5minutes = sys.maxsize
    max_5minutes = -sys.maxsize
    
    for query_data in data_5minutes_all:
        for index, trade_point in enumerate(query_data, start=0):
            price = trade_point['price']
            plot_5minutes_x = plot_5minutes_x + [trade_point['timestamp']]
            plot_5minutes_y = plot_5minutes_y + [price]
            if price < min_5minutes:
                min_5minutes= price
            if price > max_5minutes:
                max_5minutes = price
        
    diff_1day = max_1day - min_1day
    red_1day = min((diff_1day / max_1day) * 10, 1)
    diff_1hour = max_1hour - min_1hour
    red_1hour = min((diff_1hour / max_1hour) * 10, 1)
    diff_5minutes = max_5minutes - min_5minutes
    red_5minutes = min((diff_5minutes / max_5minutes) * 10, 1)

    # Save machine learning dependent variable
    price_diff = data_1hour[60]['close'] - data_1hour[59]['close']
    price_diff = round(price_diff, 2)
    if (price_diff == 0):
        up_or_down = "ZERO"
    elif price_diff > 0:
        up_or_down = "UP"
    else:
        up_or_down = "DOWN"
    
    print("price_diff: %f" % (price_diff))
    csv_row = start_datetime.isoformat() + "," + str(price_diff) + "," + up_or_down + "\n"
    with open('dataset/prices.csv','a') as fd:
        fd.write(csv_row)

    # Plotting...
    plt.cla()
    plt.clf()
    
    plt.figure(0)
    ax_5min  = plt.subplot2grid((2, 2), (0, 0), colspan=2)
    ax_1day  = plt.subplot2grid((2, 2), (1, 0))
    ax_1hour = plt.subplot2grid((2, 2), (1, 1))
    make_ticklabels_invisible(plt.gcf())
    
    plt.subplots_adjust(left=0, right=1, bottom=0, top=1, wspace=0, hspace=0)    

    # Make green as where we are in content of 24H -- day/night/morning/evening
    minutes_since_midnight = (start_datetime - start_datetime.replace(hour=0, minute=0, second=0)).total_seconds() / 60
    if minutes_since_midnight == 0:
        minutes_since_midnight = 1
    color_in_radians = (minutes_since_midnight / 1440) * math.pi * 2
    green_daystate = (math.sin(color_in_radians) + 1) * 0.15

    ax_1day.plot(plot_1day_x, plot_1day_y)
    ax_1day.set_facecolor((red_1day, green_daystate, 0.0))
    
    ax_1hour.plot(plot_1hour_x, plot_1hour_y)
    ax_1hour.set_facecolor((red_1hour, green_daystate, 0.0))

    ax_5min.plot(plot_5minutes_x, plot_5minutes_y)
    ax_5min.set_facecolor((red_5minutes, green_daystate, 0.0))
    
    filename = "dataset/plots/" + start_datetime.isoformat() + ".png"
    plt.savefig(filename, dpi=49)
    
    # Calculating new start time
    # + 24 hours (do not use current data)
    start_datetime = start_datetime + datetime.timedelta(days=1)
    # + random (up to 24 hours) to get a random beginning in day
    start_datetime = start_datetime + datetime.timedelta(seconds=random.randint(1, 24*3600))

    if (start_datetime + datetime.timedelta(hours=24) > datetime.datetime.now()):
        print("All data downloaded!")
        print("Great job!")
        sys.exit()

    print("x-ratelimit-remaining: %d " % (int(r.headers["x-ratelimit-remaining"])))
    if int(r.headers["x-ratelimit-remaining"]) < 25:
        print("Waiting 10 seconds to say in 30/requests per minute...")
        time.sleep(10)

