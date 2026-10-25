"""Extract MAVLink message definitions from a parsed SysML model."""

from sysml_icd.mavlink.wire import wire_order
from sysml_icd.sysml.parser import ParseError, parse_files


def load_messages_sysml(paths):
    """Return {message name: [(type, field name), ...] in wire order}.

    Same structure as xml_import.load_messages(), so both sources can be
    compared directly.
    """
    messages = {}
    for pkg in parse_files(paths):
        for el in pkg.children:
            if el.kind != "item def" or el.get_metadata("MavlinkMessage") is None:
                continue
            fields = []
            for attr in el.children:
                md = attr.get_metadata("MavlinkField")
                if md is None:
                    raise ParseError(f"{el.name}.{attr.name}: missing @MavlinkField")
                wire_type = md.values["wireType"].split("::")[-1]
                fields.append((wire_type, attr.name))
            messages[el.name] = wire_order(fields)
    return messages
