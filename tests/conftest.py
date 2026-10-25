"""Shared paths and fixtures; pytest loads this file automatically."""

from pathlib import Path

import pytest

from sysml_icd.mavlink.sysml_import import load_messages_sysml
from sysml_icd.mavlink.xml_import import load_messages

ROOT = Path(__file__).resolve().parent.parent
MINI_XML = ROOT / "fixtures" / "mini.xml"
MODELS = ROOT / "models"


@pytest.fixture(scope="session")
def xml_messages():
    return load_messages(MINI_XML)


@pytest.fixture(scope="session")
def sysml_messages():
    return load_messages_sysml([MODELS / "MavlinkMini.sysml"])
