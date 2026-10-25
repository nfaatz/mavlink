import xml.etree.ElementTree as ET

def load_messages(path):
    """Liefert {Nachrichtenname: Felder in Übertragungsreihenfolge}."""
    root = ET.parse(path).getroot()
    messages = {}
    for msg in root.iter("message"):
        fields = [(base_type(el.get("type")), el.get("name"))
                  for el in msg.findall("field")]
        messages[msg.get("name")] = sorted(fields, key=lambda tn: -SIZES[tn[0]])
    return messages