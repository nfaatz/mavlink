"""Shared paths and fixtures; pytest loads this file automatically."""

import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

from sysml_icd.mavlink.sysml_import import load_messages_sysml
from sysml_icd.mavlink.xml_import import load_messages
from sysml_icd.sysml.parser import parse_files

ROOT = Path(__file__).resolve().parent.parent
MINI_XML = ROOT / "fixtures" / "mini.xml"
MODELS = ROOT / "models"


@pytest.fixture(scope="session")
def xml_messages():
    return load_messages(MINI_XML)


@pytest.fixture(scope="session")
def sysml_messages():
    return load_messages_sysml([MODELS / "MavlinkMini.sysml"])


@pytest.fixture(scope="session")
def mini_xml_root():
    return ET.parse(MINI_XML).getroot()


@pytest.fixture(scope="session")
def enum_packages():
    return parse_files([MODELS / "generated" / "MavlinkEnums.sysml"])


@pytest.fixture(scope="session")
def model_packages():
    """All models together: messages, enums and own quantity types."""
    return parse_files([MODELS / "MavlinkMini.sysml",
                        MODELS / "CommonQuantities.sysml",
                        MODELS / "generated" / "MavlinkEnums.sysml"])
