"""MAVLink wire format rules: type sizes and field reordering."""

# Size in bytes of each MAVLink base type.
SIZES = {
    "uint64_t": 8, "int64_t": 8, "double": 8,
    "uint32_t": 4, "int32_t": 4, "float": 4,
    "uint16_t": 2, "int16_t": 2,
    "uint8_t": 1, "int8_t": 1, "char": 1,
}


def base_type(xml_type):
    """Map special MAVLink XML types to their plain base type."""
    if xml_type == "uint8_t_mavlink_version":
        return "uint8_t"
    return xml_type

# TECH-DEBT: extension fields are not supported (must keep XML order, excluded from CRC)
def wire_order(fields):
    """Sort (type, name) pairs into MAVLink wire order.

    Largest types first; the sort is stable, so fields of equal size
    keep their definition order.
    """
    return sorted(fields, key=lambda tn: -SIZES[tn[0]])
