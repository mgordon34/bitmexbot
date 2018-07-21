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
    
    def get_balance(self):
        return 50

    def get_price(self):
        return self.ws.get_ticker()

    def get_bid(self):
        return self.get_orderbook('Buy')

    def get_ask(self):
        return self.get_orderbook('Sell')

    def get_orderbook(self, direction):
        result = self.cl.OrderBook.OrderBook_getL2(symbol=self.symbol, depth=1).result()
        for r in result[0]:
            if r['side'] == direction:
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

    def limit(self, qty, p):
        result = self.cl.Order.Order_new(symbol=self.symbol, ordType='Limit', orderQty=qty, price=p).result()
        return result

    def take_profit(self, qty, trigger, p):
        result = self.cl.Order.Order_new(symbol=self.symbol, ordType='LimitIfTouched', orderQty=qty, stopPx=trigger, price=p, execInst='Close').result()
        return result

    def stop(self, qty, p):
        result = self.cl.Order.Order_new(symbol=self.symbol, ordType='Stop', orderQty=qty, stopPx=p, execInst='Close').result()
        return result

    def set_stops(self, link_id, qty, stop, tp):
        res1 = self.cl.Order.Order_new(symbol=self.symbol, clOrdLinkID=link_id, contingencyType='OneCancelsTheOther', ordType='Limit', orderQty=qty, price=tp, execInst='Close').result()
        res2 = self.cl.Order.Order_new(symbol=self.symbol, clOrdLinkID=link_id, contingencyType='OneCancelsTheOther', ordType='Stop', orderQty=qty, stopPx=stop, execInst='Close').result()
        print(res1)
        print(res2)
