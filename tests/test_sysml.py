import pytest

from reference_values import EXPECTED_CRC
from sysml_icd.mavlink.crc import crc_extra
from sysml_icd.sysml.parser import ParseError, parse_text


@pytest.mark.parametrize("name, expected", EXPECTED_CRC.items())
def test_crc_extra_from_sysml(sysml_messages, name, expected):
    assert crc_extra(name, sysml_messages[name]) == expected


def test_sysml_matches_xml(sysml_messages, xml_messages):
    """SysML model and reference XML must describe the same wire format."""
    assert sysml_messages == xml_messages


def test_unsupported_construct_fails_loudly():
    with pytest.raises(ParseError):
        parse_text("package X { metadata def M { } }")
