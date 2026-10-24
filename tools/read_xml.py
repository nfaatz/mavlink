import xml.etree.ElementTree as ET

tree = ET.parse("test/mini.xml")   # Datei laden
root = tree.getroot()               # das Element <mavlink>

for msg in root.iter("message"):    # alle <message> im ganzen Baum
    name = msg.get("name")          # Attribut lesen
    msg_id = msg.get("id")
    print(name, msg_id)

    for field in msg.findall("field"):   # nur direkte Kinder <field>
        print("   ", field.get("type"), field.get("name"), field.get("units"), field.get("invalid"))