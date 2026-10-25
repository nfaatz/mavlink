"""Semantic validation of MAVLink definitions in a SysML model.

These rules check meaning, not bits: a model can pass every CRC_EXTRA
check and still violate them.
"""

from sysml_icd.findings import ERROR, WARNING, Finding
from sysml_icd.mavlink.sysml_to_xml import find_message_defs, short_name

# Physical quantity kind of each MAVLink unit string.
UNIT_KINDS = {
    "us": "duration", "ms": "duration", "s": "duration",
    "rad": "angle", "deg": "angle", "cdeg": "angle", "degE7": "angle",
    "rad/s": "angular velocity", "deg/s": "angular velocity",
    "mm": "length", "cm": "length", "m": "length",
    "mm/s": "speed", "cm/s": "speed", "m/s": "speed",
}

# Quantity kind of ISQ value types (library types, not parsed).
ISQ_KINDS = {
    "DurationValue": "duration",
    "AngularMeasureValue": "angle",
    "AngularVelocityValue": "angular velocity",
    "LengthValue": "length",
    "SpeedValue": "speed",
}

# Types that carry no physical dimension.
DIMENSIONLESS = {"Natural", "Integer", "Positive", "Real", "Boolean", "String"}


def collect_specializations(packages):
    """Map each attribute def to the type it specializes (name -> parent name)."""
    return {el.name: short_name(el.type)
            for pkg in packages for el in pkg.children
            if el.kind == "attribute def" and el.type}


def collect_enum_names(packages):
    return {el.name for pkg in packages for el in pkg.children if el.kind == "enum def"}


def quantity_kind(type_name, specializations):
    """Follow the specialization chain until a known ISQ type is reached.

    Example: VelocityComponentValue -> SpeedValue -> "speed".
    Returns None if the chain ends without a known type.
    """
    name, seen = short_name(type_name), set()
    while name and name not in seen:           # 'seen' guards against cycles
        if name in ISQ_KINDS:
            return ISQ_KINDS[name]
        seen.add(name)
        name = specializations.get(name)
    return None


def iter_fields(packages):
    """Yield (location, attribute, MavlinkField values) for every message field."""
    for msg_def in find_message_defs(packages):
        for attr in msg_def.children:
            md = attr.get_metadata("MavlinkField")
            yield f"{msg_def.name}.{attr.name}", attr, (md.values if md else {})


# --- rules --------------------------------------------------------------------

def check_units(packages):
    """The wire unit must match the physical quantity of the attribute type."""
    specializations = collect_specializations(packages)
    enum_names = collect_enum_names(packages)
    findings = []

    for location, attr, values in iter_fields(packages):
        unit = values.get("units")
        type_name = short_name(attr.type)
        dimensionless = type_name in DIMENSIONLESS or type_name in enum_names
        kind = quantity_kind(type_name, specializations)

        if unit is None:
            if kind is not None:
                findings.append(Finding("UNIT-MISSING", WARNING, location,
                                        f"type {type_name} ({kind}) has no unit"))
            continue
        if unit not in UNIT_KINDS:
            findings.append(Finding("UNIT-UNKNOWN", WARNING, location,
                                    f"unit '{unit}' is not known, cannot check it"))
            continue
        if dimensionless:
            findings.append(Finding("UNIT-ON-DIMENSIONLESS", ERROR, location,
                                    f"unit '{unit}' on dimensionless type {type_name}"))
            continue
        if kind is None:
            findings.append(Finding("UNIT-UNCHECKED", WARNING, location,
                                    f"quantity kind of type {type_name} is unknown"))
            continue
        if UNIT_KINDS[unit] != kind:
            findings.append(Finding("UNIT-MISMATCH", ERROR, location,
                                    f"unit '{unit}' ({UNIT_KINDS[unit]}) does not match "
                                    f"type {type_name} ({kind})"))
    return findings


RULES = [check_units]


def validate(packages):
    """Run all rules and return the combined findings."""
    findings = []
    for rule in RULES:
        findings += rule(packages)
    return findings
