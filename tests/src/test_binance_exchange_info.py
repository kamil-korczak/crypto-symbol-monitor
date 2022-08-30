import os
import json
import random
import pytest
from src.binance_exchange_info import BinanceExchangeInfo


@pytest.fixture(scope='class')
def binance_exchange_info_connection():
    binance_exchange_info = BinanceExchangeInfo()
    binance_exchange_info.connect()
    return binance_exchange_info


@pytest.fixture(scope='class')
def get_symbols(binance_exchange_info_connection):
    data = binance_exchange_info_connection.get_data()
    return binance_exchange_info_connection.get_symbols(data)


class TestBinanceExchangeInfo:

    def test_response(self, binance_exchange_info_connection):
        assert binance_exchange_info_connection.response.status_code == 200

    def test_get_data__is_dict(self, binance_exchange_info_connection):
        assert isinstance(binance_exchange_info_connection.get_data(), dict)

    def test_get_symbols(self, get_symbols):
        assert isinstance(get_symbols, list)

        random_symbols = random.sample(get_symbols, 10)
        assert all(isinstance(symbol, str)
                   for symbol in random_symbols) is True, \
            "Not all symbols are strings in random list."

    def test_save_symbols(self, temp_symbols_path, binance_exchange_info_connection, get_symbols):
        binance_exchange_info_connection.save_symbols(get_symbols, temp_symbols_path)

        try:
            with open(temp_symbols_path) as file_:
                data = json.load(file_)
                file_is_json = True
        except ValueError:
            file_is_json = False

        assert file_is_json
