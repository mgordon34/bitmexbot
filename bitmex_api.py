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

    def get_depth(self):
        return self.ws.market_depth()

    def get_price(self):
        return self.ws.get_ticker()['last']

    def get_bid(self):
        return self.ws.get_ticker()['buy']

    def get_ask(self):
        return self.ws.get_ticker()['sell']

    def get_orderbook(self, direction):
        result = self.cl.OrderBook.OrderBook_getL2(symbol=self.symbol, depth=1).result()
        for r in result[0]:
            if r['side'] == direction:
                return r['price']
        return result

    def get_orders(self):
        return self.ws.open_orders("")

    def get_order(self):
        result = self.cl.Order.Order_getOrders(symbol=self.symbol, filter='{"open": true}').result()
        return result[0]

    def get_recent(self):
        return self.ws.recent_trades()

    def get_funds(self):
        return self.ws.funds()

    def get_ticker(self):
        return self.ws.get_ticker()

    def get_position(self):
        result = self.cl.Position.Position_get().result()
        return result[0]

    def limit(self, trade_no, link_id, qty, p):
        for i in range(10):
            try:
                result = self.cl.Order.Order_new(symbol=self.symbol,
                    clOrdID=trade_no, clOrdLinkID=link_id, ordType='Limit',
                    orderQty=qty, price=p,
                    execInst='ParticipateDoNotInitiate').result()
                return result
            except Exception as e:
                print('received exception on limit, retrying...')
                print(e)

    def take_profit(self, qty, trigger, p):
        result = self.cl.Order.Order_new(symbol=self.symbol, ordType='LimitIfTouched', orderQty=qty, stopPx=trigger, price=p, execInst='Close').result()
        return result

    def stop(self, qty, p):
        result = self.cl.Order.Order_new(symbol=self.symbol, ordType='Stop', orderQty=qty, stopPx=p, execInst='Close').result()
        return result

    def set_stops(self, trade_no, link_id, qty, stop, tp, trigger):
        for attempt in range(10):
            try:
                res1 = self.cl.Order.Order_new(symbol=self.symbol, clOrdID='tp' + trade_no, clOrdLinkID=link_id, contingencyType='OneUpdatesTheOtherAbsolute', ordType='LimitIfTouched', orderQty=qty, price=tp, stopPx=trigger, execInst='Close, LastPrice').result()
                res2 = self.cl.Order.Order_new(symbol=self.symbol, clOrdID='stop' + trade_no, clOrdLinkID=link_id, contingencyType='OneUpdatesTheOtherAbsolute', ordType='Stop', orderQty=qty, stopPx=stop, execInst='Close, LastPrice').result()
            except:
                print('received exception, retrying...')
            else:
                break
        else:
            print('failed after 10 attempts, cancelling orders...')
            self.cancel_orders()

    def update_price(self, trade_no, price, stop, tp, trigger):
        for attempt in range(10):
            try:
                result = self.cl.Order.Order_amend(origClOrdID=trade_no, price=price).result()
                res1 = self.cl.Order.Order_amend(origClOrdID='tp' + trade_no, price=tp, stopPx=trigger).result()
                res2 = self.cl.Order.Order_amend(origClOrdID='stop' + trade_no, stopPx=stop).result()
            except Exception as e:
                print('error when updating price, retrying...')
            else:
                break

    def cancel_orders(self):
        result = self.cl.Order.Order_cancelAll(symbol='XBTUSD').result()
        return result
