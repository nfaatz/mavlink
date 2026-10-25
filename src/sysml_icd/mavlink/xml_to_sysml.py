"""Generate SysML v2 text from MAVLink XML definitions."""

import xml.etree.ElementTree as ET
from pathlib import Path


def doc_block(text, indent):
    """Format a description as a SysML doc comment (list of lines)."""
    if not text:
        return []
    text = text.replace("*/", "* /")              # would otherwise end the comment
    lines = [" ".join(l.split()) for l in text.strip().splitlines()]
    lines = [l for l in lines if l]               # drop empty lines
    if not lines:
        return []
    pad = " " * indent
    # "doc" on its own line matches the formatter style of the editor,
    # so regenerating does not produce spurious diffs.
    if len(lines) == 1:
        return [f"{pad}doc", f"{pad}/* {lines[0]} */"]
    out = [f"{pad}doc", f"{pad}/* {lines[0]}"]
    out += [f"{pad} * {l}" for l in lines[1:]]
    out.append(f"{pad} */")
    return out


def gen_enums(xml_path):
    root = ET.parse(xml_path).getroot()
    out = [f"// GENERATED from {Path(xml_path).name} - do not edit by hand",
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

        next_value = 0                            # for entries without a value
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

    if out[-1] == "":
        out.pop()                                 # no blank line before closing brace
    out.append("} // package MavlinkEnums")
    return "\n".join(out) + "\n"
