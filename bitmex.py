
import requests
import datetime
import time
import bitmex_auth

baseurl = 'https://www.bitmex.com/api/v1/'
auth = bitmex_auth.APIKeyAuth()

def print_request_info(request):
    print("URL: " + request.url)
    if "x-ratelimit-remaining" in request.headers:
        print("x-ratelimit-remaining: %d " % (int(request.headers["x-ratelimit-remaining"])))
    else:
        print("x-ratelimit-remaining: HEADER DOES NOT EXIST!")

def get_1day_data(start_datetime, print_info=False):
    url = baseurl + "trade/bucketed?binSize=5m&partial=false&symbol=XBT&count=288&startTime=" + start_datetime.isoformat()[:-9]
    r = requests.get(url)
    if (print_info):
        print_request_info(r)
    return r.json()

def get_1hour_data(start_datetime, print_info=False, count=60):
    url = baseurl + "trade/bucketed?binSize=1m&partial=false&symbol=XBT&count=" + str(count) + "&startTime=" + start_datetime.isoformat()[:-9]
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

        url = baseurl + "trade?symbol=XBT&count=500&columns=price&startTime=" + start_5minutes_datetime.isoformat()[:-9] \
          + "&endTime=" + end_5minutes_datetime.isoformat()[:-9] + "&start=" + str(start)        
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
            if "x-ratelimit-remaining" in r.headers and int(r.headers["x-ratelimit-remaining"]) < 10:
                print("x-ratelimit-remaining below 10, waiting 10 seconds to say in 30/requests per minute...")
                time.sleep(10)

    return data_5minutes_all

trade_amount = 400
stop_loss_diff = 8

def trade_buy(start_price):
    params={
        'symbol': 'XBTUSD',
        'ordType': 'Market',
        'orderQty': trade_amount
    }
    r = requests.post(baseurl + 'order', params=params, auth=auth)
    print(r.json())
    # Add stop loss
    params={
        'symbol': 'XBTUSD',
        'ordType': 'Stop',
        'orderQty': -trade_amount,
        'stopPx': start_price - stop_loss_diff
    }
    r = requests.post(baseurl + 'order', params=params, auth=auth)
    print(r.json())

def close_buy_trade():
    if position_is_open(): # Position may be closed by stop-loss order
        params={
            'symbol': 'XBTUSD',
            'ordType': 'Market',
            'orderQty': -trade_amount
        }
        r = requests.post(baseurl + 'order', params=params, auth=auth)
        print(r.json())
    # Add cancel stop loss
    r = requests.delete(baseurl + 'order/all', auth=auth)
    print(r.json())

def trade_sell(start_price):
    params={
        'symbol': 'XBTUSD',
        'ordType': 'Market',
        'orderQty': -trade_amount
    }
    r = requests.post(baseurl + 'order', params=params, auth=auth)
    print(r.json())
    # Add stop loss
    params={
        'symbol': 'XBTUSD',
        'ordType': 'Stop',
        'orderQty': trade_amount,
        'stopPx': start_price + stop_loss_diff
    }
    r = requests.post(baseurl + 'order', params=params, auth=auth)
    print(r.json())

def close_sell_trade():
    if position_is_open(): # Position may be closed by stop-loss order
        params={
            'symbol': 'XBTUSD',
            'ordType': 'Market',
            'orderQty': trade_amount
        }
        r = requests.post(baseurl + 'order', params=params, auth=auth)
        print(r.json())
    # Add cancel stop loss
    r = requests.delete(baseurl + 'order/all', auth=auth)
    print(r.json())

def position_is_open():
    r = requests.get(baseurl + 'position', auth=auth)
    json_data = r.json()
    return json_data[0]['isOpen']

def bitcoin_count_in_wallet():
    r = requests.get(baseurl + 'user/walletHistory', auth=auth)
    json_data = r.json()
    return json_data[0]['walletBalance']
    

