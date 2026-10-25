import pytest

from sysml_icd.findings import ERROR, WARNING
from sysml_icd.mavlink.validate import check_units, quantity_kind, validate
from sysml_icd.sysml.parser import parse_text


def model_with_field(type_name, units=None):
    """Build a minimal model with one message and one field."""
    unit_part = f' units = "{units}";' if units else ""
    return parse_text(f"""
        package T {{
            attribute def MyAngle :> AngularMeasureValue;
            enum def MyEnum {{ enum A; }}
            item def MSG {{
                @MavlinkMessage {{ id = 1; }}
                attribute f : {type_name} {{
                    @MavlinkField {{ wireType = WireType::float;{unit_part} }}
                }}
            }}
        }}
    """)


def test_reference_model_is_clean(model_packages):
    assert validate(model_packages) == []


@pytest.mark.parametrize("type_name, units, rule, severity", [
    ("AngularMeasureValue", "rad",   None,                    None),
    ("MyAngle",             "degE7", None,                    None),     # via specialization
    ("Natural",             None,    None,                    None),
    ("AngularMeasureValue", "mm",    "UNIT-MISMATCH",         ERROR),
    ("DurationValue",       "cm/s",  "UNIT-MISMATCH",         ERROR),
    ("Natural",             "ms",    "UNIT-ON-DIMENSIONLESS", ERROR),
    ("MyEnum",              "rad",   "UNIT-ON-DIMENSIONLESS", ERROR),
    ("LengthValue",         None,    "UNIT-MISSING",          WARNING),
    ("LengthValue",         "furlong", "UNIT-UNKNOWN",        WARNING),
    ("SomeUnknownType",     "m",     "UNIT-UNCHECKED",        WARNING),
])
def test_check_units(type_name, units, rule, severity):
    findings = check_units(model_with_field(type_name, units))
    if rule is None:
        assert findings == []
    else:
        assert [(f.rule, f.severity, f.location) for f in findings] == [(rule, severity, "MSG.f")]


def test_quantity_kind_follows_specialization_chain():
    specs = {"A": "B", "B": "SpeedValue"}
    assert quantity_kind("A", specs) == "speed"


def test_quantity_kind_survives_cycles():
    assert quantity_kind("A", {"A": "B", "B": "A"}) is None
