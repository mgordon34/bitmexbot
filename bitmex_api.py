import bitmex
from bitmex_websocket import BitMEXWebsocket
from datetime import datetime, time
from time import sleep
import urllib.parse

import config

class Bitmex():
    ws = BitMEXWebsocket(endpoint="https://www.bitmex.com/api/v1", symbol="XBTUSD", api_key=config.bitmex_key, api_secret=config.bitmex_secret)
    cl = bitmex.bitmex(test=False, api_key=config.bitmex_key, api_secret=config.bitmex_secret)
    symbol = "XBTUSD"

    def __init__(self):
        self.lasttime = datetime.now()
        self.lastupdate = self.lasttime
        self.lastprice = 0

        self.ws.get_instrument()

    def get_price(self):
        return self.ws.get_ticker()

    def get_bid(self):
        result = self.cl.OrderBook.OrderBook_getL2(symbol=self.symbol, depth=1).result()
        for r in result[0]:
            if r['side'] == 'Buy':
                return r['price']
        return result

    def get_ask(self):
        result = self.cl.OrderBook.OrderBook_getL2(symbol=self.symbol, depth=1).result()
        for r in result[0]:
            if r['side'] == 'Sell':
                return r['price']
        return result

    def get_orders(self):
        return self.ws.open_orders("")

    def get_order(self):
        result = self.cl.Order.Order_getOrders(symbol=self.symbol, filter='{"open": true}').result()
        return result[0]

    def get_recent(self):
        return self.ws.recent_trades()

    def buy_limit(self):
        result = self.cl.Order.Order_new(symbol=self.symbol, ordType='LimitIfTouched', orderQty=1, stopPx=6240.5, price=6240.5, execInst='Close').result()
        return result

