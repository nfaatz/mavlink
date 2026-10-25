import xml.etree.ElementTree as ET


def doc_block(text, indent):
    """Formatiert eine Beschreibung als SysML-doc-Kommentar (Liste von Zeilen)."""
    if not text:
        return []
    text = text.replace("*/", "* /")              # würde den Kommentar sonst beenden
    lines = [" ".join(l.split()) for l in text.strip().splitlines()]
    lines = [l for l in lines if l]               # Leerzeilen entfernen
    if not lines:
        return []
    pad = " " * indent
    if len(lines) == 1:
        return [f"{pad}doc /* {lines[0]} */"]
    out = [f"{pad}doc", f"{pad}/* {lines[0]}"]
    out += [f"{pad} * {l}" for l in lines[1:]]
    out.append(f"{pad} */")
    return out


def gen_enums(xml_path):
    root = ET.parse(xml_path).getroot()
    out = [f"// GENERIERT aus {xml_path} – nicht von Hand ändern",
           "package MavlinkEnums {",
           "    private import MavlinkProfile::*;",
           ""]

    for enum in root.iter("enum"):
        out.append(f"    enum def {enum.get('name')} {{")
        out += doc_block(enum.findtext("description"), 8)

        if enum.get("bitmask") == "true":
            out.append("        @MavlinkEnum { bitmask = true; }")
        else:
            out.append("        @MavlinkEnum;")

        next_value = 0                            # für Einträge ohne value
        for entry in enum.findall("entry"):
            raw = entry.get("value")
            value = int(raw, 0) if raw is not None else next_value
            next_value = value + 1

            out.append(f"        enum {entry.get('name')} {{")
            out += doc_block(entry.findtext("description"), 12)
            out.append(f"            @MavlinkEnumValue {{ value = {value}; }}")
            out.append("        }")

        out.append("    }")
        out.append("")

    out.append("}")
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    with open("models/MavlinkEnums.sysml", "w", encoding="utf-8") as f:
        f.write(gen_enums("test/mini.xml"))