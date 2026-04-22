import pytest
from file_handler import FileHandler


def test_file_handler_initialization():
    handler = FileHandler()
    assert handler is not None


def test_file_handler_key_functionality():
    handler = FileHandler()
    result = handler.key_functionality()
    assert result is not None
