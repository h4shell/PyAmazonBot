import config.config as config
import config.creds as creds
import string
import random
import requests


class PyAmazonBot:
    def __init__(self):
        self.token = creds.bot["TOKEN"]
        self.to = config.data['TO']

        self.headers = {
            "accept": "application/json",
            "User-Agent": "Telegram Bot SDK - (https://github.com/irazasyed/telegram-bot-sdk)",
            "content-type": "application/json"
        }

        self.apiURL = f'https://api.telegram.org/bot{self.token}/sendMessage'

    def codegen(self):

        self.var = random.choice(string.ascii_letters) + random.choice(string.ascii_letters) + random.choice(
            string.ascii_letters) + random.choice(string.ascii_letters) + random.choice(string.ascii_letters)

        return self.var

    def send_to_telegram(self, message):
        self.message = message

        self.payload = {'chat_id': self.to,
                        'parse_mode': 'HTML', 'text': self.message, 'parse_mode': "HTML", "disable_web_page_preview": True}
        self.response = requests.post(
            self.apiURL, json=self.payload, headers=self.headers).json()
        return self.response


if __name__ == '__main__':
    app = PyAmazonBot()
    n = app.send_to_telegram(app.codegen())
    print(n)
