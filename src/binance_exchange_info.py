import json
import requests
import os
from src.config import SYMBOLS_SRC

BINANCE_EXCHANGE_INFO_API = 'https://www.binance.com/api/v3/exchangeInfo'


class BinanceExchangeInfo():

    response = None

    def connect(self):
        self.response = requests.get(url=BINANCE_EXCHANGE_INFO_API)

    def get_data(self):
        return self.response.json()

    def get_symbols(self, data):
        symbols = data.get('symbols')

        if symbols:
            return [symbol['symbol'].lower() for symbol in symbols]

    def save_symbols(self):
        symbols = self.get_symbols(self.get_data())

        os.makedirs(os.path.dirname(SYMBOLS_SRC), exist_ok=True)

        with open(SYMBOLS_SRC, 'w') as file_:
            json.dump(symbols, file_)
