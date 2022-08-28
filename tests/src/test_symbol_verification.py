import os
import pytest

from src.symbol_verification import SymbolVerification, SYMBOLS_SRC


@pytest.fixture(scope="module")
def get_symbols():
    symbol_verification = SymbolVerification()
    symbol_verification.get_symbols()
    return symbol_verification


@pytest.fixture(scope="module")
def load_symbols(get_symbols):
    get_symbols.load_symbols()
    return get_symbols


class TestSymbolVerification:

    def test_get_symbols(self, get_symbols):
        # TODO Symbols should be saved in temp dir. Source method should be refactored.
        assert os.path.exists(SYMBOLS_SRC)

    def test_load_symbols(self, load_symbols):
        assert isinstance(load_symbols.symbols, list)
        assert len(load_symbols.symbols), "Symbols is an empty list"

    def test_verify(self, load_symbols):
        assert load_symbols.verify('btcusdt'), 'The symbol does not exist'
        assert load_symbols.verify('ethusdt'), 'The symbol does not exist'
