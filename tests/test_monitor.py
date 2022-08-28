import decimal
import pytest

from monitor import CryptoSymbolMonitor

ARG_PARSER_MESSAGE = """usage: pytest [-h] [-d] symbol user_price

-------------------------------------
Crypto Market Symbol Monitoring Price
-------------------------------------

Monitoring the market data based on the symbol and a price and printing out every time the price goes above the input price.

Example usage:
# Monitor prices of `BTCUSDT` market and print price when it's above `20000`
$ ./monitor.py btcusdt 20000

positional arguments:
  symbol       Symbol of crypto market
  user_price   Price of a given  symbol

optional arguments:
  -h, --help   show this help message and exit
  -d, --debug
"""

ARG_PARSER_ERROR_MESSAGE = 'error: the following arguments are required: symbol, user_price\n'


@pytest.fixture
def monitor():
    return CryptoSymbolMonitor()


class TestMonitor:

    def test_parse_args(self, monitor):

        symbol, user_price = monitor.parse_args(['btcusdt', '20'])

        assert isinstance(symbol, str) and isinstance(
            user_price, decimal.Decimal)

    def test_parse_args__no_args(self, capsys, monitor):

        system_exited = False

        try:
            monitor.parse_args([])
        except SystemExit:
            system_exited = True

        assert system_exited, "App did not exited without providing args."

        output, error = capsys.readouterr()
        assert output == ARG_PARSER_MESSAGE, 'Message is different.'
        assert error == ARG_PARSER_ERROR_MESSAGE, 'Message error is different.'
