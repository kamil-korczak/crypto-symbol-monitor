import os
import pytest

TEST_SYMBOLS_SRC = 'test_binance_symbols.json'


@pytest.fixture(scope='session')
def temp_test_path(tmp_path_factory):
    return tmp_path_factory.mktemp("symbols")


@pytest.fixture(scope='session')
def temp_symbols_path(temp_test_path):
    return os.path.join(temp_test_path, TEST_SYMBOLS_SRC)
