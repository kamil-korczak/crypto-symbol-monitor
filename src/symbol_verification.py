import time
import json
import os
from src.config import SYMBOLS_SRC
from src.binance_exchange_info import BinanceExchangeInfo


class SymbolVerification:

    symbols = []

    def get_symbols(self):
        if os.path.exists(SYMBOLS_SRC):
            current_time = time.time()
            modified_time = os.path.getmtime(SYMBOLS_SRC)
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
        with open(SYMBOLS_SRC) as file_:
            self.symbols = json.load(file_)
