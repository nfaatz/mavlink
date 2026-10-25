"""Read message definitions from a MAVLink XML file."""

import xml.etree.ElementTree as ET

from sysml_icd.mavlink.wire import base_type, wire_order


def load_messages(xml_path):
    """Return {message name: [(type, field name), ...] in wire order}."""
    root = ET.parse(xml_path).getroot()
    messages = {}
    for msg in root.iter("message"):
        fields = [(base_type(el.get("type")), el.get("name"))
                  for el in msg.findall("field")]
        messages[msg.get("name")] = wire_order(fields)
    return messages
