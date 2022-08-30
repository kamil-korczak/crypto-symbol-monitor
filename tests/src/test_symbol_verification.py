import os
import pytest

from src.symbol_verification import SymbolVerification, SYMBOLS_SRC


class SymbolVerificationTestHelper:

    def __init__(self, file_path, symbol_verification):
        self.file_path = file_path
        self.symbol_verification = symbol_verification


@pytest.fixture(scope="class")
def get_symbols(temp_symbols_path):
    symbol_verification = SymbolVerification()
    symbol_verification.get_symbols(temp_symbols_path)
    return SymbolVerificationTestHelper(temp_symbols_path, symbol_verification)


@pytest.fixture(scope="class")
def load_symbols(get_symbols):
    get_symbols.symbol_verification.load_symbols(get_symbols.file_path)
    return get_symbols.symbol_verification


class TestSymbolVerification:

    def test_get_symbols(self, get_symbols):
        assert os.path.exists(
            get_symbols.file_path), 'File with symbols not exists'

    def test_load_symbols(self, load_symbols):
        assert isinstance(load_symbols.symbols, list)
        assert len(load_symbols.symbols), "Symbols is an empty list"

    def test_verify(self, load_symbols):
        assert load_symbols.verify('btcusdt'), 'The symbol does not exist'
        assert load_symbols.verify('ethusdt'), 'The symbol does not exist'
