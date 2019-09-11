
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import sys
import math

def make_ticklabels_invisible(fig):
    for i, ax in enumerate(fig.axes):
        ax.text(0.5, 0.5, "ax%d" % (i+1), va="center", ha="center")
        for tl in ax.get_xticklabels() + ax.get_yticklabels():
            tl.set_visible(False)

def plot_one_image(data_1day, data_1hour, data_5minutes_all, image_filename, start_datetime):

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

    plot_5minutes_x = plot_5minutes_y = []
    min_5minutes = sys.maxsize
    max_5minutes = -sys.maxsize

    for query_data in data_5minutes_all:
        one_query_x = one_query_y = []
        for index, trade_point in enumerate(query_data, start=0):
            price = trade_point['price']
            one_query_x = one_query_x + [trade_point['timestamp']]
            one_query_y = one_query_y + [price]
            if price < min_5minutes:
                min_5minutes= price
            if price > max_5minutes:
                max_5minutes = price

        plot_5minutes_x = plot_5minutes_x + one_query_x
        plot_5minutes_y = plot_5minutes_y + one_query_y
        
    diff_1day = max_1day - min_1day
    red_1day = min((diff_1day / max_1day) * 10, 1)
    diff_1hour = max_1hour - min_1hour
    red_1hour = min((diff_1hour / max_1hour) * 10, 1)
    diff_5minutes = max_5minutes - min_5minutes
    red_5minutes = min((diff_5minutes / max_5minutes) * 10, 1)

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

    plt.savefig(image_filename, dpi=49)

