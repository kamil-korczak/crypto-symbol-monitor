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

    def save_symbols(self, symbols, file_path=SYMBOLS_SRC):
        """
        :param file_path - for testing purpose, by default no need to specify.
        """

        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, 'w') as file_:
            json.dump(symbols, file_)
