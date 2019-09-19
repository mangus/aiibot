
import requests
import datetime

endpoint="http://192.168.1.127:4444"

def get_current_price():
    url = endpoint + "/instrument?symbol=XBTUSD"
    r = requests.get(url)
    data = r.json()
    return data[0]['lastPrice']

def get_last_5minutes():
    print("start 1 checkpoint")
    url = endpoint + "/trade?symbol=XBTUSD"
    r = requests.get(url)
    data = r.json()
    last_5min_data = filter_last_5minutes(data)
    data_5minutes_all = []
    data_5minutes_all.append(last_5min_data)
    return data_5minutes_all

def filter_last_5minutes(all_data): 
    return all_data[find_5minutes_index(all_data):len(all_data)]

def find_5minutes_index(all_data):
    index = int(len(all_data) / 2)
    step = index
    past_5minutes = datetime.datetime.fromisoformat(all_data[len(all_data) - 1]["timestamp"][:-5]) \
        - datetime.timedelta(minutes=5)
    check_datetime = datetime.datetime.fromisoformat(all_data[index]["timestamp"][:-5])
    while (check_datetime != past_5minutes):
        step = int(step / 2)
        if (step == 0):
            break;
        if (check_datetime > past_5minutes):
            index = index - step
        else:
            index = index + step
        check_datetime = datetime.datetime.fromisoformat(all_data[index]["timestamp"][:-5])
    return index

