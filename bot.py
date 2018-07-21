import bitmex_api
import mail
import datetime

class Bot():
    def __init__(self):
        self.trades = {}
        self.last_message = 0
        self.last_update = datetime.datetime.now()

        self.mail = mail.Mail()
        self.mail.connect()
        self.bitmex = bitmex_api.Bitmex()

        self.percent = .02

    def calc_size(self, price, spread):
        balance = self.bitmex.get_balance()
        n1 = price / 100.0
        n2 = (balance * self.percent) / (spread / price * 100.0))
        return n1 * n2

    def run(self):
        price = self.bitmex.get_ask()
        self.bitmex.set_stops('id', -1, price - 50, price)

        while True:
            t = datetime.datetime.now()
            if t.second == 5 and (t - self.last_update).total_seconds() > 10:
                self.last_update = t
                print('Price: ' + str(self.bitmex.get_price()))
                message = self.mail.check_for_mail()
                if message:
                    print('Message Received: ' + str(message))
                else:
                    print('No message')


bot = Bot()
bot.run()
