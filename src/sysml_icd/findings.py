"""Validation findings, shared by all protocol validators."""

from dataclasses import dataclass

ERROR = "error"
WARNING = "warning"


@dataclass(frozen=True)
class Finding:
    rule: str          # stable rule id, e.g. "UNIT-MISMATCH"
    severity: str      # ERROR or WARNING
    location: str      # e.g. "GLOBAL_POSITION_INT.lat"
    message: str

    def __str__(self):
        return f"{self.severity.upper():7} {self.rule:22} {self.location}: {self.message}"
