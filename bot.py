import signal
import sys

import bitmex_api
import mail
import datetime

class Bot():
    def __init__(self):
        self.trades = {}
        self.last_message = 0
        self.trade_no = 19
        self.last_update = datetime.datetime.now()

        self.mail = mail.Mail()
        self.mail.connect()
        self.bitmex = bitmex_api.Bitmex()

        self.percent = .02

    def calc_size(self, price, _range):
        # balance = self.bitmex.get_balance()
        balance = 30
        n1 = price / 100.0
        n2 = (balance * self.percent) / (_range / price * 100.0)
        return n1 * n2

    def is_open(self):
        orders = self.bitmex.get_orders()
        for order in orders:
            if order['ordType'] == 'Limit':
                return True
        return False

    def enter_trade(self, message):
        _range = message['range']
        size = self.calc_size(self.bitmex.get_price(), _range)
        price = 0

        self.trade_no += 1
        self.trades[self.trade_no] = {}

        if message['direction'] == 'long':
            print('last: {}'.format(self.bitmex.get_price() - .5))
            print('bid: {}'.format(self.bitmex.get_bid()))
            price = max(self.bitmex.get_bid(), self.bitmex.get_price() - .5)
            print('entering trade at {}'.format(price))

            self.bitmex.limit(str(self.trade_no), 'link' + str(self.trade_no),
                size, price)
            self.bitmex.set_stops(str(self.trade_no),
                'link' + str(self.trade_no), -size, price - _range, price + _range,
                price + _range - 1.0)
        elif message['direction'] == 'short':
            print('last: {}'.format(self.bitmex.get_price() + .5))
            print('ask: {}'.format(self.bitmex.get_ask()))
            price = min(self.bitmex.get_ask(), self.bitmex.get_price() + .5)
            print('entering trade at {}'.format(price))

            self.bitmex.limit(str(self.trade_no), 'link' + str(self.last_message), -size, price)
            self.bitmex.set_stops(str(self.trade_no), 'link' + str(self.last_message),
                size, price + _range, price - _range, price - _range + 1.0)
        else:
            print('something wrong: direction not valid: {}'.format(direction))
            return
        
        self.trades[self.trade_no] = {
            'direction': message['direction'],
            'price': price,
            'range': _range,
            'age': 0,
        }

    def run(self):
        # price = self.bitmex.get_ask()
        # self.bitmex.set_stops('id', -1, price - 50, price)
        # mymsg = {"num": 5, "direction": "long", "range": 40}
        # self.enter_trade(mymsg)

        while True:
            t = datetime.datetime.now()
            if t.second == 5 and (t - self.last_update).total_seconds() > 5:
                self.last_update = t

                # first clear any trade still open
                if self.is_open():
                    age = self.trades[self.trade_no]['age']
                    if age <= 0:
                        print('adding to age of order...')
                    elif age > 0:
                        print('order too old, cancelling...')
                        self.bitmex.cancel_orders()
                    self.trades[self.trade_no]['age'] += 1

                # checking for new message. If there is a new message, enter
                # the trade
                message = self.mail.check_for_mail()
                if message:
                    positions = self.bitmex.get_position()
                    for i in positions:
                        if i['symbol'] == 'XBTUSD':
                            positions = i['currentQty']

                    if self.last_message != 0 and positions == 0:
                        print('Message Received: ' + str(message))
                        self.enter_trade(message)
                    else:
                        print('ignoring first message')
                    self.last_message += 1
            elif t.second == 15 and (t - self.last_update).total_seconds() > 5:
                self.last_update = t
                if self.is_open():
                    trade_price = self.trades[self.trade_no]['price']
                    curr_price = self.bitmex.get_price()
                    dirr = self.trades[self.trade_no]['direction']
                    _range = self.trades[self.trade_no]['range']
                    if dirr == 'long':
                       bid = self.bitmex.get_bid()
                       new_price = max(bid, curr_price - .5)
                       if (new_price - trade_price > 1 and new_price - trade_price < 20):
                           print('detected price difference, updating...')
                           self.trades[self.trade_no]['price'] = new_price
                           self.bitmex.update_price(str(self.trade_no), new_price, new_price - _range, new_price + _range, new_price + _range - 1)
                    elif dirr == 'short':
                       ask = self.bitmex.get_ask()
                       new_price = min(ask, curr_price + .5)
                       if (trade_price - new_price > 1 and trade_price - new_price < 20):
                           print('detected price difference, updating...')
                           self.trades[self.trade_no]['price'] = new_price
                           self.bitmex.update_price(str(self.trade_no), new_price, new_price + _range, new_price - _range, new_price - _range + 1)
                

# def signal_handler(sig, frame):
#     print('received kill signal')
#     sys.exit(0)
# 
# signal.signal(signal.SIGINT, signal_handler)


while True:
    try:
        bot = Bot()
        bot.run()
    except Exception as e:
        print('ran into exception {}\n, re-running...'.format(str(e)))
    else:
        break
