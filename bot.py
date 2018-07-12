import bitmex_api
import mail

class Bot():
    def __init__(self):
        self.trades = {}
        self.last_message = 0

        self.mail = mail.Mail()
        self.mail.connect()
        self.bitmex = bitmex_api.Bitmex()

    def run(self):
        # lastprice = 0
        # while True:
        #     price = self.bitmex.get_price()
        #     if price != lastprice:
        #         lastprice = price
        #         print(price)
        print('Price: ' + str(self.bitmex.get_price()))
        message = self.mail.check_for_mail()
        if message:
            print('Message Received: ' + str(message))
        else:
            print('No message')

        print('Open orders:')
        print(self.bitmex.get_orders())
 
        print('Recent trades:')
        print(self.bitmex.get_recent())
 
        print('Pricee:')
        print(self.bitmex.get_bid())

        print('Order:')
        print(self.bitmex.get_order()[0]['orderQty'])

        print('Making order:')
        print(self.bitmex.buy_limit())

bot = Bot()
bot.run()
