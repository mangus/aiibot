
from bitmex_websocket import BitMEXWebsocket
ws = BitMEXWebsocket(endpoint="https://testnet.bitmex.com/api/v1", symbol="XBTUSD", api_key=None, api_secret=None)
ws.get_instrument()

def get_current_price():
    data = ws.get_ticker()
    return data['last']
