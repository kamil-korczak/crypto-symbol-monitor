#!/usr/bin/env python

import argparse
from argparse import RawTextHelpFormatter
import decimal
import sys
from binance_price_monitor import BinancePriceMonitor

CRYPTO_MARKET_SYMBOL_MONITORING_DESCRIPTION = \
"""
-------------------------------------
Crypto Market Symbol Monitoring Price
-------------------------------------

Monitoring the market data based on the symbol and a price 
and printing out every time the price goes above the input price.

Example usage:
# Monitor prices of `BTCUSDT` market and print price when it's above `20000`
$ ./monitor.py btcusdt 20000 

"""



class MonitorArgsParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)


def show_menu():

    args_parser = MonitorArgsParser(
        description=CRYPTO_MARKET_SYMBOL_MONITORING_DESCRIPTION,
        formatter_class=RawTextHelpFormatter)

    args_parser.add_argument("symbol", help="Symbol of crypto market", type=str)
    args_parser.add_argument("user_price", help="Price of a given  symbol", type=str)
    args = args_parser.parse_args()

    symbol=args.symbol.lower()
    user_price=decimal.Decimal(args.user_price)
    
    run_app(symbol, user_price)
    

def run_app(symbol, user_price):
    bpm = BinancePriceMonitor(symbol, user_price)
    bpm.run()

if __name__ == '__main__':
    show_menu()