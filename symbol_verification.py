import time
import json
import os
from binance_exchange_info import BinanceExchangeInfo

SYMBOLS_FILENAME = 'binance_symbols.json'


class SymbolVerification:

    symbols = []

    def get_symbols(self):
        if os.path.exists(SYMBOLS_FILENAME):
            current_time = time.time()
            modified_time = os.path.getmtime(SYMBOLS_FILENAME)
            duration = current_time - modified_time

            if duration < 60 * 60 * 24:
                return

        binance_exchange_info = BinanceExchangeInfo()
        binance_exchange_info.connect()
        binance_exchange_info.save_symbols()

    def verify(self, symbol):
        if symbol in self.symbols:
            return True

    def load_symbols(self):
        with open(SYMBOLS_FILENAME) as file_:
            self.symbols = json.load(file_)
