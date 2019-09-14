
import datetime
import random
import bitmex
import plotter

print("Aii v3 will rule (the wooorld)! Creating dataset...")

start_datetime = datetime.datetime(2018, 1, 1, 0, 0, 0)
very_start_datetime = start_datetime
while (True):

    print("\n\n%s" % (start_datetime.isoformat()))

    data_1day = bitmex.get_1day_data(start_datetime, print_info=True)

    start_1hour_datetime = start_datetime + datetime.timedelta(hours=23)
    data_1hour = bitmex.get_1hour_data(start_1hour_datetime, print_info=True, count=61)

    start_5minutes_datetime = start_1hour_datetime + datetime.timedelta(minutes=55)
    data_5minutes_all = bitmex.get_5minutes_all_data(start_5minutes_datetime)

    # Save machine learning dependent variable
    price_diff = data_1hour[60]['close'] - data_1hour[59]['close']
    price_diff = round(price_diff, 4)
    
    print("price_diff: %f" % (price_diff))

    csv_row = start_datetime.isoformat() + "," + str(price_diff) + "\n"
    with open('dataset/prices.csv','a') as fd:
        fd.write(csv_row)

    filename = "dataset/plots/" + start_datetime.isoformat() + ".png"
    plotter.plot_one_image(data_1day, data_1hour, data_5minutes_all, filename, start_datetime)
    
    # Calculating new start time
    # + 24 hours (do not use current data)
    start_datetime = start_datetime + datetime.timedelta(days=1)
    # + random (up to 24 hours) to get a random beginning in day
    start_datetime = start_datetime + datetime.timedelta(seconds=random.randint(1, 24*3600))

    if (start_datetime + datetime.timedelta(hours=24) > datetime.datetime.now()):
        print("Reached NOW, going back to beginning for the next round...")
        start_datetime = very_start_datetime + datetime.timedelta(seconds=random.randint(1, 24*3600))

