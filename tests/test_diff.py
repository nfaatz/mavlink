import pytest

from conftest import MODELS
from sysml_icd.mavlink.diff import (BREAKING_LOUD, BREAKING_SILENT, COMPATIBLE,
                                    CONDITIONAL, INFO, compare, verdict)
from sysml_icd.sysml.parser import parse_text

MINI = (MODELS / "MavlinkMini.sysml").read_text(encoding="utf-8")
QUANTITIES = (MODELS / "CommonQuantities.sysml").read_text(encoding="utf-8")
ENUMS = (MODELS / "generated" / "MavlinkEnums.sysml").read_text(encoding="utf-8")

NEW_MESSAGE = """
    item def NEW_MSG {
        @MavlinkMessage { id = 999; }
        attribute x : Natural { @MavlinkField { wireType = WireType::uint8_t; } }
    }
} // package MavlinkMini"""


def model(mini=MINI, enums=ENUMS):
    return parse_text(mini) + parse_text(QUANTITIES) + parse_text(enums)


def edit(text, old, new):
    """Replace exactly one occurrence, so a test never edits the wrong spot silently."""
    assert text.count(old) == 1, f"anchor not unique: {old!r}"
    return text.replace(old, new)


def summary(changes):
    return {(c.cls, c.location) for c in changes}


def test_identical_models_have_no_changes():
    assert compare(model(), model()) == []
    assert verdict([]) == INFO


# pytest.param(..., id=...) gives each case a short name. Without it pytest
# builds the test id from the parameter values, i.e. from the whole model text.
@pytest.mark.parametrize("mini, enums, expected", [
    pytest.param(
        edit(MINI, 'uint32_t; units = "ms"; }\n        }\n        attribute roll',
                   'uint32_t; units = "s"; }\n        }\n        attribute roll'), ENUMS,
        {(BREAKING_SILENT, "ATTITUDE.time_boot_ms")},
        id="units-ms-to-s"),
    pytest.param(
        edit(MINI, "WireType::uint16_t", "WireType::int16_t"), ENUMS,
        {(BREAKING_LOUD, "GLOBAL_POSITION_INT"), (BREAKING_LOUD, "GLOBAL_POSITION_INT.hdg")},
        id="wire-type-changed"),
    pytest.param(
        edit(MINI, "/* Roll angle (-pi..+pi) */", "/* Roll angle in radians */"), ENUMS,
        {(INFO, "ATTITUDE.roll")},
        id="description-changed"),
    pytest.param(
        edit(MINI, "} // package MavlinkMini", NEW_MESSAGE), ENUMS,
        {(COMPATIBLE, "NEW_MSG")},
        id="message-added"),
    pytest.param(
        MINI, edit(ENUMS, "        enum MAV_STATE_UNINIT {",
                   "        enum MAV_STATE_NEW { @MavlinkEnumValue { value = 99; } }\n"
                   "        enum MAV_STATE_UNINIT {"),
        {(CONDITIONAL, "MAV_STATE.MAV_STATE_NEW")},
        id="enum-entry-added"),
    pytest.param(
        MINI, edit(ENUMS, "value = 128;", "value = 64;"),
        {(BREAKING_SILENT, "MAV_MODE_FLAG.MAV_MODE_FLAG_SAFETY_ARMED")},
        id="enum-value-changed"),
])
def test_change_classification(mini, enums, expected):
    assert summary(compare(model(), model(mini, enums))) == expected


def test_verdict_is_worst_change():
    mini = edit(MINI, "WireType::uint16_t", "WireType::int16_t")
    enums = edit(ENUMS, "value = 128;", "value = 64;")
    assert verdict(compare(model(), model(mini, enums))) == BREAKING_SILENT


def test_most_dangerous_changes_come_first():
    mini = edit(MINI, "/* Roll angle (-pi..+pi) */", "/* Roll angle in radians */")
    enums = edit(ENUMS, "value = 128;", "value = 64;")
    changes = compare(model(), model(mini, enums))
    assert [c.cls for c in changes] == [BREAKING_SILENT, INFO]