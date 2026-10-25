"""Round trip: MAVLink XML -> SysML -> MAVLink XML must preserve the content."""

import copy
import importlib.util
import subprocess
import sys

import pytest

from reference_values import EXPECTED_CRC
from sysml_icd.mavlink.sysml_to_xml import build_enums, build_mavlink_xml, build_messages


def normalize(text):
    """Collapse all whitespace so line breaks and indentation do not matter."""
    return " ".join((text or "").split())


def canonical_enums(enums_el):
    """Reduce an <enums> element to plain data that can be compared with ==."""
    result = []
    for enum in enums_el.findall("enum"):
        entries = [(e.get("name"), int(e.get("value"), 0), normalize(e.findtext("description")))
                   for e in enum.findall("entry")]
        result.append((enum.get("name"),
                       enum.get("bitmask") == "true",
                       normalize(enum.findtext("description")),
                       entries))
    return result


def canonical_messages(messages_el):
    """Reduce a <messages> element to plain data; field order is kept."""
    result = []
    for msg in messages_el.findall("message"):
        fields = [(dict(f.attrib), normalize(f.text)) for f in msg.findall("field")]
        result.append((msg.get("name"),
                       int(msg.get("id")),
                       normalize(msg.findtext("description")),
                       fields))
    return result


# --- enums ------------------------------------------------------------------

def test_enums_roundtrip(enum_packages, mini_xml_root):
    generated = build_enums(enum_packages)
    original = mini_xml_root.find("enums")
    assert canonical_enums(generated) == canonical_enums(original)


def test_roundtrip_detects_changed_value(enum_packages, mini_xml_root):
    """Guard against a comparison that is accidentally always true."""
    original = copy.deepcopy(mini_xml_root.find("enums"))
    original.find("enum/entry").set("value", "99")
    assert canonical_enums(build_enums(enum_packages)) != canonical_enums(original)


# --- messages ---------------------------------------------------------------

def test_messages_roundtrip(model_packages, mini_xml_root):
    generated = canonical_messages(build_messages(model_packages))
    original = canonical_messages(mini_xml_root.find("messages"))
    # compare per message for readable failure output
    for gen, orig in zip(generated, original):
        assert gen == orig, f"message {orig[0]} differs"
    assert len(generated) == len(original)


def test_roundtrip_detects_changed_field(model_packages, mini_xml_root):
    original = copy.deepcopy(mini_xml_root.find("messages"))
    original.find("message/field").set("type", "uint16_t")
    assert canonical_messages(build_messages(model_packages)) != canonical_messages(original)


# --- integration with the official generator --------------------------------

def test_mavgen_accepts_generated_xml(model_packages, tmp_path):
    """mavgen must accept our XML and derive the reference CRC_EXTRA values."""
    pytest.importorskip("pymavlink")
    xml_path = tmp_path / "from_sysml.xml"
    py_path = tmp_path / "from_sysml.py"
    build_mavlink_xml(model_packages).write(xml_path, encoding="utf-8", xml_declaration=True)

    subprocess.run([sys.executable, "-m", "pymavlink.tools.mavgen",
                    "--lang=Python3", "--wire-protocol=2.0",
                    f"--output={py_path}", str(xml_path)],
                   check=True, capture_output=True)

    spec = importlib.util.spec_from_file_location("from_sysml", py_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    crc_by_name = {cls.msgname: cls.crc_extra
                   for cls in vars(module).values()
                   if isinstance(cls, type) and hasattr(cls, "crc_extra") and hasattr(cls, "msgname")}
    for name, expected in EXPECTED_CRC.items():
        assert crc_by_name[name] == expected
