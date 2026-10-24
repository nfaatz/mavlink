import pytest
from tools.reorder import load_messages, crc_extra

EXPECTED = {"HEARTBEAT": 50, "ATTITUDE": 39, "GLOBAL_POSITION_INT": 104}

@pytest.fixture
def messages():
    return load_messages("test/mini.xml")

@pytest.mark.parametrize("name, expected", EXPECTED.items())
def test_crc_extra(messages, name, expected):
    assert crc_extra(name, messages[name]) == expected

def test_heartbeat_reordering(messages):
    names = [n for t, n in messages["HEARTBEAT"]]
    assert names[0] == "custom_mode"