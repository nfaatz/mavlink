"""Compare the models in the working tree against an older git version.

Usage:
    python scripts/diff_models.py              # against the last commit (HEAD)
    python scripts/diff_models.py --old v0.1   # against a tag, branch or commit

Exit code 1 if any change is BREAKING (CI-ready).
"""

import argparse
import subprocess
import sys
from pathlib import Path

from sysml_icd.mavlink.diff import BREAKING_LOUD, BREAKING_SILENT, compare, verdict
from sysml_icd.sysml.parser import parse_text

ROOT = Path(__file__).resolve().parent.parent
MODEL_FILES = ["models/MavlinkMini.sysml",
               "models/CommonQuantities.sysml",
               "models/generated/MavlinkEnums.sysml"]


def read_from_git(ref, path):
    """Return the file content at the given git ref, or None if it did not exist."""
    result = subprocess.run(["git", "show", f"{ref}:{path}"], cwd=ROOT,
                            capture_output=True, encoding="utf-8")
    return result.stdout if result.returncode == 0 else None


def load(texts):
    packages = []
    for text in texts:
        if text is not None:
            packages += parse_text(text)
    return packages


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--old", default="HEAD", help="git ref of the old version")
    args = parser.parse_args()

    old = load(read_from_git(args.old, p) for p in MODEL_FILES)
    new = load((ROOT / p).read_text(encoding="utf-8") for p in MODEL_FILES)

    changes = compare(old, new)
    for change in changes:
        print(change)
    result = verdict(changes)
    print(f"{len(changes)} change(s), verdict: {result}")
    sys.exit(1 if result in (BREAKING_LOUD, BREAKING_SILENT) else 0)
