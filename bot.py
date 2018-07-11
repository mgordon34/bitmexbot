import bitmex
import mail

class Bot():
    def __init__(self):
        self.trades = {}
        self.last_message = 0

        self.mail = mail.Mail()
        self.mail.connect()
        self.bitmex = bitmex.Bitmex()

    def run(self):
        print('Price: ' + str(self.bitmex.get_price()))
        message = self.mail.check_for_mail()
        if message:
            print('Message Received: ' + str(message))
        else:
            print('No message')

bot = Bot()
bot.run()
bot.run()
