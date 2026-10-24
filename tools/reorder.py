import xml.etree.ElementTree as ET

SIZES = {
    "uint64_t": 8, "int64_t": 8, "double": 8,
    "uint32_t": 4, "int32_t": 4, "float": 4,
    "uint16_t": 2, "int16_t": 2,
    "uint8_t": 1, "int8_t": 1, "char": 1,
}

def base_type(t):
    if t == "uint8_t_mavlink_version":
        return "uint8_t"
    return t

def crc_accumulate(crc, data):
    for b in data:
        tmp = (b ^ (crc & 0xFF)) & 0xFF
        tmp = (tmp ^ (tmp << 4)) & 0xFF
        crc = ((crc >> 8) ^ (tmp << 8) ^ (tmp << 3) ^ (tmp >> 4)) & 0xFFFF
    return crc

def crc_extra(msg_name, ordered):
    crc = crc_accumulate(0xFFFF, (msg_name + " ").encode())
    for typ, field_name in ordered:
        crc = crc_accumulate(crc, (typ + " ").encode())
        crc = crc_accumulate(crc, (field_name + " ").encode())
    return (crc & 0xFF) ^ (crc >> 8)

def load_messages(path):
    """Liefert {Nachrichtenname: Felder in Übertragungsreihenfolge}."""
    root = ET.parse(path).getroot()
    messages = {}
    for msg in root.iter("message"):
        fields = [(base_type(el.get("type")), el.get("name"))
                  for el in msg.findall("field")]
        messages[msg.get("name")] = sorted(fields, key=lambda tn: -SIZES[tn[0]])
    return messages

if __name__ == "__main__":
    for name, ordered in load_messages("test/mini.xml").items():
        print(name, [n for t, n in ordered], crc_extra(name, ordered))