
import requests
import datetime
import time
from bitmex_websocket import BitMEXWebsocket

ws = BitMEXWebsocket(endpoint="https://www.bitmex.com/api/v1", symbol="XBTUSD", api_key=None, api_secret=None)
ws.get_instrument()

def get_current_price():
    data = ws.get_ticker()
    return data['last']

def print_request_info(request):
    print("URL: " + request.url)
    print("x-ratelimit-remaining: %d " % (int(request.headers["x-ratelimit-remaining"])))

def get_1day_data(start_datetime, print_info=False):
    url = "https://www.bitmex.com/api/v1/trade/bucketed?binSize=5m&partial=false&symbol=XBT&count=288&startTime=" + start_datetime.isoformat()
    r = requests.get(url)
    if (print_info):
        print_request_info(r)
    return r.json()

def get_1hour_data(start_datetime, print_info=False, count=60):
    url = "https://www.bitmex.com/api/v1/trade/bucketed?binSize=1m&partial=false&symbol=XBT&count=" + str(count) + "&startTime=" + start_datetime.isoformat()
    r = requests.get(url)
    if (print_info):
        print_request_info(r)
    return r.json()

def get_5minutes_all_data(start_5minutes_datetime, print_info=True, limit=True): # May need optimizing

    end_5minutes_datetime = start_5minutes_datetime + datetime.timedelta(minutes=5)

    have_all_data = False
    start = 0
    data_5minutes_all = []
    while (not have_all_data):

        url = "https://www.bitmex.com/api/v1/trade?symbol=XBT&count=500&columns=price&startTime=" + start_5minutes_datetime.isoformat() \
          + "&endTime=" + end_5minutes_datetime.isoformat() + "&start=" + str(start)        
        r = requests.get(url)
        if (print_info):
            print_request_info(r)
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

        if (limit):
            if int(r.headers["x-ratelimit-remaining"]) < 10:
                print("x-ratelimit-remaining below 10, waiting 10 seconds to say in 30/requests per minute...")
                time.sleep(10)

    return data_5minutes_all

