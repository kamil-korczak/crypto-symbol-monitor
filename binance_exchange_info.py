import json
import requests

BINANCE_EXCHANGE_INFO_API = 'https://www.binance.com/api/v3/exchangeInfo'
SYMBOLS_FILENAME = 'binance_symbols.json'


class BinanceExchangeInfo():

    response = None

    def connect(self):
        self.response = requests.get(url=BINANCE_EXCHANGE_INFO_API)

    def get_data(self):
        return self.response.json()

    def get_symbols(self, data):
        symbols = data.get('symbols')

        if symbols:
            return [symbol.get('symbol').lower() for symbol in symbols]

    def save_symbols(self):
        symbols = self.get_symbols(self.get_data())

        with open(SYMBOLS_FILENAME, 'w') as file_:
            json.dump(symbols, file_)
