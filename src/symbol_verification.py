import time
import json
import os
from src.config import SYMBOLS_SRC
from src.binance_exchange_info import BinanceExchangeInfo


class SymbolVerification:

    symbols = []

    def get_symbols(self, file_path=SYMBOLS_SRC):
        """
        :param file_path - for testing purposes.
        """
        if os.path.exists(file_path):
            current_time = time.time()
            modified_time = os.path.getmtime(file_path)
            duration = current_time - modified_time

            if duration < 60 * 60 * 24:
                return

        binance_exchange_info = BinanceExchangeInfo()
        binance_exchange_info.connect()
        symbols = binance_exchange_info.get_symbols(
            binance_exchange_info.get_data())
        binance_exchange_info.save_symbols(symbols, file_path)

    def load_symbols(self, file_path=SYMBOLS_SRC):
        """
        :param file_path - for testing purposes.
        """
        with open(file_path) as file_:
            self.symbols = json.load(file_)

    def verify(self, symbol):
        if symbol in self.symbols:
            return True
