import pytest
from voice_handler import VoiceHandler


def test_voice_handler_initialization():
    handler = VoiceHandler()
    assert handler is not None


def test_voice_handler_key_functionality():
    handler = VoiceHandler()
    result = handler.key_functionality()
    assert result is not None
