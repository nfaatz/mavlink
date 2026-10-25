"""Regenerate models/generated/MavlinkEnums.sysml from the reference XML."""

from pathlib import Path

from sysml_icd.mavlink.xml_to_sysml import gen_enums

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "fixtures" / "mini.xml"
TARGET = ROOT / "models" / "generated" / "MavlinkEnums.sysml"

if __name__ == "__main__":
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    TARGET.write_text(gen_enums(SOURCE), encoding="utf-8")
    print(f"written: {TARGET.relative_to(ROOT)}")
