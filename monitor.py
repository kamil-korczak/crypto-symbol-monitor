#!/usr/bin/env python

import argparse
from argparse import RawTextHelpFormatter
import decimal
import sys
from src.logging import create_logger
from src.symbol_verification import SymbolVerification
from src.binance_price_monitor import BinancePriceMonitor

CRYPTO_MARKET_SYMBOL_MONITORING_DESCRIPTION = \
    """-------------------------------------
Crypto Market Symbol Monitoring Price
-------------------------------------

Monitoring the market data based on the symbol and a price \
and printing out every time the price goes above the input price.

Example usage:
# Monitor prices of `BTCUSDT` market and print price when it's above `20000`
$ ./monitor.py btcusdt 20000"""


class MonitorArgsParser(argparse.ArgumentParser):

    def error(self, message):
        sys.stderr.write(f'error: {message}\n')
        self.print_help()
        sys.exit(2)


class CryptoSymbolMonitor:

    def __init__(self):
        self.debug = None
        self.name = __name__
        self.logging = None

    def load_logger(self):
        self.logging = create_logger(self)

    def parse_args(self, app_args):

        args_parser = MonitorArgsParser(
            description=CRYPTO_MARKET_SYMBOL_MONITORING_DESCRIPTION,
            formatter_class=RawTextHelpFormatter)

        args_parser.add_argument(
            "symbol", help="Symbol of crypto market", type=str)
        args_parser.add_argument(
            "user_price", help="Price of a given  symbol", type=str)

        # Debug as optional argument
        args_parser.add_argument('-d', '--debug', action='store_true')

        args = args_parser.parse_args(app_args)

        self.debug = args.debug
        self.load_logger()

        symbol = args.symbol.lower()

        symbol_verification = SymbolVerification()
        symbol_verification.get_symbols()
        symbol_verification.load_symbols()

        while not symbol_verification.verify(symbol):
            self.logging.error('The given symbol is not available. Try again.')
            symbol = input("Symbol of crypto market: ").lower()

        user_price = None

        while not isinstance(user_price, decimal.Decimal):
            try:
                if not user_price:
                    user_price = decimal.Decimal(args.user_price)
                else:
                    user_price = decimal.Decimal(user_price)
            except decimal.InvalidOperation:
                self.logging.info(
                    'The text provided is not a decimal number.')
                user_price = input('Price of a given symbol: ')

        return (symbol, user_price)

    def run_app(self, symbol, user_price):
        self.logging.info('Binance Price Monitor starting...')
        bpm = BinancePriceMonitor(self, symbol, user_price)
        bpm.run()


if __name__ == '__main__':
    app_args_ = None
    if len(sys.argv) > 1:
        app_args_ = sys.argv[1:]

    crypto_symbol_monitor = CryptoSymbolMonitor()
    symbol_, user_price_ = crypto_symbol_monitor.parse_args(app_args_)
    crypto_symbol_monitor.run_app(symbol_, user_price_)
