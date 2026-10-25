"""Compare two versions of a MAVLink interface model and classify each change.

The guiding question: does a peer built against the OLD version still work
with a peer built against the NEW version?
"""

from dataclasses import dataclass

from sysml_icd.mavlink.crc import crc_extra
from sysml_icd.mavlink.sysml_to_xml import find_enum_defs, find_message_defs, short_name
from sysml_icd.mavlink.wire import wire_order

# Change classes, ordered from harmless to most dangerous.
INFO = "INFO"                        # documentation only
COMPATIBLE = "COMPATIBLE"            # old peers keep working
CONDITIONAL = "CONDITIONAL"          # wire compatible, meaning at risk in one direction
BREAKING_LOUD = "BREAKING-LOUD"      # incompatible, MAVLink notices (CRC_EXTRA, unknown id)
BREAKING_SILENT = "BREAKING-SILENT"  # incompatible, nobody notices: wrong values arrive
SEVERITY_ORDER = [INFO, COMPATIBLE, CONDITIONAL, BREAKING_LOUD, BREAKING_SILENT]


@dataclass(frozen=True)
class Change:
    cls: str
    location: str
    detail: str

    def __str__(self):
        return f"{self.cls:16} {self.location:32} {self.detail}"


@dataclass(frozen=True)
class FieldInfo:
    name: str
    wire_type: str
    units: str | None
    invalid: str | None
    auto_version: bool
    semantic_type: str | None       # SysML type, e.g. AngularMeasureValue or MAV_TYPE
    doc: str


# --- snapshot: reduce a parsed model to plain, comparable data ----------------

def _norm(text):
    return " ".join((text or "").split())


def snapshot(packages):
    """Return {"messages": {...}, "enums": {...}} for one model version."""
    messages = {}
    for msg_def in find_message_defs(packages):
        fields = []
        for attr in msg_def.children:
            v = attr.get_metadata("MavlinkField").values
            fields.append(FieldInfo(
                name=attr.name,
                wire_type=short_name(v["wireType"]),
                units=v.get("units"),
                invalid=v.get("invalid"),
                auto_version=bool(v.get("autoVersion")),
                semantic_type=short_name(attr.type),
                doc=_norm(attr.doc)))
        messages[msg_def.name] = {
            "id": msg_def.get_metadata("MavlinkMessage").values["id"],
            "doc": _norm(msg_def.doc),
            "fields": fields}

    enums = {}
    for enum_def in find_enum_defs(packages):
        entries = {lit.name: (lit.get_metadata("MavlinkEnumValue").values["value"], _norm(lit.doc))
                   for lit in enum_def.children}
        enums[enum_def.name] = {
            "bitmask": bool(enum_def.get_metadata("MavlinkEnum").values.get("bitmask")),
            "doc": _norm(enum_def.doc),
            "entries": entries}
    return {"messages": messages, "enums": enums}


def message_crc(name, fields):
    return crc_extra(name, wire_order([(f.wire_type, f.name) for f in fields]))


# --- comparison -------------------------------------------------------------

def compare_messages(old, new):
    changes = []
    for name in old.keys() - new.keys():
        changes.append(Change(BREAKING_LOUD, name, "message removed"))
    for name in new.keys() - old.keys():
        changes.append(Change(COMPATIBLE, name, "message added (old peers ignore unknown ids)"))

    for name in sorted(old.keys() & new.keys()):
        o, n = old[name], new[name]
        if o["id"] != n["id"]:
            changes.append(Change(BREAKING_LOUD, name, f"id {o['id']} -> {n['id']}"))
        if o["doc"] != n["doc"]:
            changes.append(Change(INFO, name, "description changed"))

        crc_old, crc_new = message_crc(name, o["fields"]), message_crc(name, n["fields"])
        if crc_old != crc_new:
            changes.append(Change(BREAKING_LOUD, name,
                                  f"CRC_EXTRA {crc_old} -> {crc_new} (peers drop each other's packets)"))
        changes += compare_fields(name, o["fields"], n["fields"], crc_changed=crc_old != crc_new)
    return changes


def compare_fields(msg_name, old_fields, new_fields, crc_changed):
    changes = []
    old_by_name = {f.name: f for f in old_fields}
    new_by_name = {f.name: f for f in new_fields}

    for name in old_by_name.keys() - new_by_name.keys():
        changes.append(Change(BREAKING_LOUD, f"{msg_name}.{name}", "field removed"))
    for name in new_by_name.keys() - old_by_name.keys():
        changes.append(Change(BREAKING_LOUD, f"{msg_name}.{name}", "field added"))

    for name in [f.name for f in old_fields if f.name in new_by_name]:
        o, n, loc = old_by_name[name], new_by_name[name], f"{msg_name}.{name}"
        if o.wire_type != n.wire_type:
            changes.append(Change(BREAKING_LOUD, loc, f"wire type {o.wire_type} -> {n.wire_type}"))
        # The following changes leave CRC_EXTRA untouched: MAVLink cannot notice them.
        if o.units != n.units:
            changes.append(Change(BREAKING_SILENT, loc, f"units {o.units!r} -> {n.units!r}"))
        if o.invalid != n.invalid:
            changes.append(Change(BREAKING_SILENT, loc, f"invalid value {o.invalid!r} -> {n.invalid!r}"))
        if o.semantic_type != n.semantic_type:
            changes.append(Change(BREAKING_SILENT, loc,
                                  f"meaning {o.semantic_type} -> {n.semantic_type}"))
        if o.auto_version != n.auto_version:
            changes.append(Change(BREAKING_SILENT, loc, "autoVersion changed"))
        if o.doc != n.doc:
            changes.append(Change(INFO, loc, "description changed"))

    common_old = [f.name for f in old_fields if f.name in new_by_name]
    common_new = [f.name for f in new_fields if f.name in old_by_name]
    if common_old != common_new and not crc_changed:
        changes.append(Change(INFO, msg_name,
                              "definition order changed, wire order unchanged "
                              "(generated function signatures may change)"))
    return changes


def compare_enums(old, new):
    changes = []
    for name in old.keys() - new.keys():
        changes.append(Change(BREAKING_SILENT, name, "enum removed"))
    for name in new.keys() - old.keys():
        changes.append(Change(COMPATIBLE, name, "enum added"))

    for name in sorted(old.keys() & new.keys()):
        o, n = old[name], new[name]
        if o["bitmask"] != n["bitmask"]:
            changes.append(Change(BREAKING_SILENT, name,
                                  f"bitmask {o['bitmask']} -> {n['bitmask']}"))
        if o["doc"] != n["doc"]:
            changes.append(Change(INFO, name, "description changed"))

        oe, ne = o["entries"], n["entries"]
        for entry in oe.keys() - ne.keys():
            changes.append(Change(BREAKING_SILENT, f"{name}.{entry}",
                                  "entry removed (old sender -> new receiver: unknown value)"))
        for entry in ne.keys() - oe.keys():
            changes.append(Change(CONDITIONAL, f"{name}.{entry}",
                                  "entry added (new sender -> old receiver: unknown value)"))
        for entry in sorted(oe.keys() & ne.keys()):
            (ov, od), (nv, nd) = oe[entry], ne[entry]
            if ov != nv:
                changes.append(Change(BREAKING_SILENT, f"{name}.{entry}", f"value {ov} -> {nv}"))
            if od != nd:
                changes.append(Change(INFO, f"{name}.{entry}", "description changed"))
    return changes


def compare(old_packages, new_packages):
    """Return all changes, most dangerous first."""
    old, new = snapshot(old_packages), snapshot(new_packages)
    changes = compare_messages(old["messages"], new["messages"])
    changes += compare_enums(old["enums"], new["enums"])
    return sorted(changes, key=lambda c: (-SEVERITY_ORDER.index(c.cls), c.location))


def verdict(changes):
    """The overall class is the worst single change (INFO if there are none)."""
    if not changes:
        return INFO
    return max((c.cls for c in changes), key=SEVERITY_ORDER.index)
