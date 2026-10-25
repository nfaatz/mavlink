import pytest

from reference_values import EXPECTED_CRC
from sysml_icd.mavlink.crc import crc_extra


@pytest.mark.parametrize("name, expected", EXPECTED_CRC.items())
def test_crc_extra_from_xml(xml_messages, name, expected):
    assert crc_extra(name, xml_messages[name]) == expected


def test_heartbeat_reordering(xml_messages):
    names = [n for t, n in xml_messages["HEARTBEAT"]]
    assert names[0] == "custom_mode"
