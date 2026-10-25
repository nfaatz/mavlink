"""Validate the SysML models; exit code 1 if any error is found (CI-ready)."""

import sys
from pathlib import Path

from sysml_icd.findings import ERROR
from sysml_icd.mavlink.validate import validate
from sysml_icd.sysml.parser import parse_files

ROOT = Path(__file__).resolve().parent.parent
SOURCES = [ROOT / "models" / "MavlinkMini.sysml",
           ROOT / "models" / "CommonQuantities.sysml",
           ROOT / "models" / "generated" / "MavlinkEnums.sysml"]

if __name__ == "__main__":
    findings = validate(parse_files(SOURCES))
    for f in findings:
        print(f)
    errors = sum(f.severity == ERROR for f in findings)
    print(f"{len(findings)} finding(s), {errors} error(s)")
    sys.exit(1 if errors else 0)
