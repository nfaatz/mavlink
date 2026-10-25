import pytest
from tools.reorder import load_messages, crc_extra
from tools.sysml_parser import load_messages_sysml, parse_text, ParseError

EXPECTED = {"HEARTBEAT": 50, "ATTITUDE": 39, "GLOBAL_POSITION_INT": 104}


@pytest.fixture(scope="module")
def sysml_messages():
    return load_messages_sysml(["models/MavlinkMini.sysml"])


@pytest.mark.parametrize("name, expected", EXPECTED.items())
def test_crc_extra_from_sysml(sysml_messages, name, expected):
    assert crc_extra(name, sysml_messages[name]) == expected


def test_sysml_matches_xml(sysml_messages):
    """SysML model and reference XML must describe the same wire format."""
    assert sysml_messages == load_messages("test/mini.xml")


def test_unsupported_construct_fails_loudly():
    with pytest.raises(ParseError):
        parse_text("package X { metadata def M { } }")