import urllib.parse
from bitmex_websocket import BitMEXWebsocket
from datetime import datetime, time
from time import sleep

import config

class Bitmex():
    ws = BitMEXWebsocket(endpoint="https://www.bitmex.com/api/v1", symbol="XBTUSD", api_key=config.bitmex_key, api_secret=config.bitmex_secret)

    def __init__(self):
        self.lasttime = datetime.now()
        self.lastupdate = self.lasttime
        self.lastprice = 0

        self.ws.get_instrument()

    def get_price(self):
        return self.ws.get_ticker()
