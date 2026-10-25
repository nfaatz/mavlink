"""Generate MAVLink XML definitions from a parsed SysML model."""

import xml.etree.ElementTree as ET


def find_enum_defs(packages):
    """Yield all enum defs annotated with @MavlinkEnum."""
    for pkg in packages:
        for el in pkg.children:
            if el.kind == "enum def" and el.get_metadata("MavlinkEnum") is not None:
                yield el


def add_description(parent, doc):
    """Append a <description> child if the element has a doc comment."""
    if doc:
        ET.SubElement(parent, "description").text = " ".join(doc.split())


def build_enums(packages):
    """Return an <enums> element for all MAVLink enums in the model."""
    enums_el = ET.Element("enums")
    for enum_def in find_enum_defs(packages):
        enum_el = ET.SubElement(enums_el, "enum", name=enum_def.name)
        if enum_def.get_metadata("MavlinkEnum").values.get("bitmask"):
            enum_el.set("bitmask", "true")
        add_description(enum_el, enum_def.doc)

        for literal in enum_def.children:
            md = literal.get_metadata("MavlinkEnumValue")
            if md is None:
                raise ValueError(f"{enum_def.name}.{literal.name}: missing @MavlinkEnumValue")
            entry_el = ET.SubElement(enum_el, "entry",
                                     value=str(md.values["value"]),
                                     name=literal.name)
            add_description(entry_el, literal.doc)
    return enums_el


def find_message_defs(packages):
    """Yield all item defs annotated with @MavlinkMessage."""
    for pkg in packages:
        for el in pkg.children:
            if el.kind == "item def" and el.get_metadata("MavlinkMessage") is not None:
                yield el


def short_name(qualified_name):
    """'MavlinkEnums::MAV_TYPE' -> 'MAV_TYPE'."""
    return qualified_name.split("::")[-1] if qualified_name else None


def build_messages(packages):
    """Return a <messages> element for all MAVLink messages in the model.

    Fields keep their definition order; wire order is derived by mavgen.
    """
    enum_names = {e.name for e in find_enum_defs(packages)}
    messages_el = ET.Element("messages")

    for msg_def in find_message_defs(packages):
        msg_id = msg_def.get_metadata("MavlinkMessage").values["id"]
        msg_el = ET.SubElement(messages_el, "message", id=str(msg_id), name=msg_def.name)
        add_description(msg_el, msg_def.doc)

        for attr in msg_def.children:
            md = attr.get_metadata("MavlinkField")
            if md is None:
                raise ValueError(f"{msg_def.name}.{attr.name}: missing @MavlinkField")
            values = md.values

            wire_type = short_name(values["wireType"])
            if values.get("autoVersion"):
                wire_type = "uint8_t_mavlink_version"     # magic type, filled by the library

            field_el = ET.SubElement(msg_el, "field", type=wire_type, name=attr.name)
            if short_name(attr.type) in enum_names:        # semantic type is a MAVLink enum
                field_el.set("enum", short_name(attr.type))
            for key in ("units", "invalid"):
                if key in values:
                    field_el.set(key, values[key])
            if attr.doc:
                field_el.text = " ".join(attr.doc.split())
    return messages_el


def build_mavlink_xml(packages, version=3, dialect=0):
    """Return a complete <mavlink> document as an ElementTree."""
    root = ET.Element("mavlink")
    ET.SubElement(root, "version").text = str(version)
    ET.SubElement(root, "dialect").text = str(dialect)
    root.append(build_enums(packages))
    root.append(build_messages(packages))
    ET.indent(root, space="    ")
    return ET.ElementTree(root)
