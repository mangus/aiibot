
import requests
import datetime
from bitmex_websocket import BitMEXWebsocket

ws = BitMEXWebsocket(endpoint="https://testnet.bitmex.com/api/v1", symbol="XBTUSD", api_key=None, api_secret=None)
ws.get_instrument()

def get_current_price():
    data = ws.get_ticker()
    return data['last']

def get_1day_data(start_datetime):
    url = "https://www.bitmex.com/api/v1/trade/bucketed?binSize=5m&partial=false&symbol=XBT&count=288&startTime=" + start_datetime.isoformat()
    r = requests.get(url)
    return r.json()

def get_1hour_data(start_datetime):
    url = "https://www.bitmex.com/api/v1/trade/bucketed?binSize=1m&partial=false&symbol=XBT&count=60&startTime=" + start_datetime.isoformat()
    r = requests.get(url)
    return r.json()

def get_5minutes_all_data(start_1hour_datetime): # May need optimizing

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

    return data_5minutes_all

