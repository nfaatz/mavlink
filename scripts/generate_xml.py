"""Generate MAVLink XML from the SysML models into generated/mini_from_sysml.xml."""

from pathlib import Path

from sysml_icd.mavlink.sysml_to_xml import build_mavlink_xml
from sysml_icd.sysml.parser import parse_files

ROOT = Path(__file__).resolve().parent.parent
SOURCES = [ROOT / "models" / "MavlinkMini.sysml",
           ROOT / "models" / "generated" / "MavlinkEnums.sysml"]
TARGET = ROOT / "generated" / "mini_from_sysml.xml"

if __name__ == "__main__":
    TARGET.parent.mkdir(exist_ok=True)
    tree = build_mavlink_xml(parse_files(SOURCES))
    tree.write(TARGET, encoding="utf-8", xml_declaration=True)
    print(f"written: {TARGET.relative_to(ROOT)}")
