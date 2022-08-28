import time
import json
import os
from src.config import SYMBOLS_SRC
from src.binance_exchange_info import BinanceExchangeInfo


class SymbolVerification:

    symbols = []

    def get_symbols(self):
        # TODO should be refactored for better testing
        if os.path.exists(SYMBOLS_SRC):
            current_time = time.time()
            modified_time = os.path.getmtime(SYMBOLS_SRC)
            duration = current_time - modified_time

            if duration < 60 * 60 * 24:
                return

        binance_exchange_info = BinanceExchangeInfo()
        binance_exchange_info.connect()
        symbols = binance_exchange_info.get_symbols(
            binance_exchange_info.get_data())
        binance_exchange_info.save_symbols(symbols)

    def load_symbols(self):
        # TODO should be refactored for better testing
        with open(SYMBOLS_SRC) as file_:
            self.symbols = json.load(file_)

    def verify(self, symbol):
        if symbol in self.symbols:
            return True
