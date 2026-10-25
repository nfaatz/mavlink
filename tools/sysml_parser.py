"""Minimal parser for the SysML v2 textual subset used in this project.

TECH-DEBT: This is NOT a full SysML v2 parser. It supports only:
    package, import, item def, enum def, attribute def,
    attribute usages (with type and multiplicity), enum literals,
    doc comments and metadata annotations (@Name { key = value; }).
Anything else raises ParseError. Replace with an official parser
(e.g. Pilot Implementation JSON export) once the subset grows.
See docs/adr/0001-own-subset-parser.md.
"""

import re
from dataclasses import dataclass, field


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class Metadata:
    name: str
    values: dict = field(default_factory=dict)


@dataclass
class Element:
    kind: str                       # "package", "item def", "attribute", ...
    name: str
    type: str | None = None         # declared type or specialized type
    multiplicity: str | None = None
    doc: str | None = None
    metadata: list = field(default_factory=list)
    children: list = field(default_factory=list)

    def get_metadata(self, name):
        """Return the metadata annotation with the given name, or None."""
        for md in self.metadata:
            if md.name == name:
                return md
        return None


class ParseError(Exception):
    pass


# ---------------------------------------------------------------------------
# Tokenizer
# ---------------------------------------------------------------------------

TOKEN_SPEC = [
    ("BLOCK",   r"/\*.*?\*/"),               # block comment, used as doc body
    ("COMMENT", r"//[^\n]*"),                # line comment, ignored
    ("STRING",  r'"(?:[^"\\]|\\.)*"'),
    ("NUMBER",  r"\d+(?:\.\d+)?"),
    ("NAME",    r"[A-Za-z_][A-Za-z0-9_]*"),
    ("OP",      r"::\*|::|:>|\.\.|[{}();:@=\[\],*]"),
    ("NEWLINE", r"\n"),
    ("SKIP",    r"[ \t\r]+"),
    ("ERROR",   r"."),
]
TOKEN_RE = re.compile("|".join(f"(?P<{k}>{p})" for k, p in TOKEN_SPEC), re.S)


@dataclass
class Token:
    kind: str
    value: str
    line: int


def tokenize(text):
    tokens, line = [], 1
    for m in TOKEN_RE.finditer(text):
        kind, value = m.lastgroup, m.group()
        if kind == "ERROR":
            raise ParseError(f"line {line}: unexpected character {value!r}")
        if kind not in ("SKIP", "NEWLINE", "COMMENT"):
            tokens.append(Token(kind, value, line))
        line += value.count("\n")
    tokens.append(Token("EOF", "", line))
    return tokens


# ---------------------------------------------------------------------------
# Parser (recursive descent: one method per grammar rule)
# ---------------------------------------------------------------------------

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    # --- token helpers -----------------------------------------------------

    def peek(self):
        return self.tokens[self.pos]

    def accept(self, value):
        """Consume the next token if it has the given value."""
        if self.peek().value == value:
            self.pos += 1
            return True
        return False

    def expect(self, value=None, kind=None):
        tok = self.peek()
        if (value is not None and tok.value != value) or \
           (kind is not None and tok.kind != kind):
            wanted = value or kind
            raise ParseError(f"line {tok.line}: expected {wanted!r}, got {tok.value!r}")
        self.pos += 1
        return tok

    # --- grammar rules -----------------------------------------------------

    def parse_file(self):
        packages = []
        while self.peek().kind != "EOF":
            packages.append(self.parse_package())
        return packages

    def parse_package(self):
        self.expect("package")
        pkg = Element("package", self.expect(kind="NAME").value)
        self.expect("{")
        while not self.accept("}"):
            member = self.parse_member()
            if member is not None:
                pkg.children.append(member)
        return pkg

    def parse_member(self):
        self.accept("private") or self.accept("public")
        tok = self.peek()

        if self.accept("import"):
            self.parse_qualified_name()
            self.accept("::*")
            self.expect(";")
            return None                          # imports are not needed yet

        if tok.value in ("item", "enum", "attribute") and \
           self.tokens[self.pos + 1].value == "def":
            self.pos += 2
            el = Element(f"{tok.value} def", self.expect(kind="NAME").value)
            if self.accept(":>"):
                el.type = self.parse_qualified_name()
            self.parse_body(el)
            return el

        raise ParseError(f"line {tok.line}: unsupported construct {tok.value!r}")

    def parse_body(self, el):
        if self.accept(";"):
            return
        self.expect("{")
        while not self.accept("}"):
            tok = self.peek()
            if self.accept("doc"):
                el.doc = clean_doc(self.expect(kind="BLOCK").value)
            elif tok.kind == "BLOCK":
                self.pos += 1                    # plain comment, ignored
            elif self.accept("@"):
                el.metadata.append(self.parse_metadata())
            elif self.accept("attribute"):
                el.children.append(self.parse_attribute())
            elif self.accept("enum"):
                lit = Element("enum", self.expect(kind="NAME").value)
                self.parse_body(lit)
                el.children.append(lit)
            else:
                raise ParseError(f"line {tok.line}: unexpected {tok.value!r} in body of {el.name}")

    def parse_attribute(self):
        attr = Element("attribute", self.expect(kind="NAME").value)
        if self.accept(":"):
            attr.type = self.parse_qualified_name()
        if self.accept("["):
            attr.multiplicity = self.parse_multiplicity()
        self.parse_body(attr)
        return attr

    def parse_multiplicity(self):
        parts = []
        while not self.accept("]"):
            parts.append(self.peek().value)
            self.pos += 1
        return "".join(parts)                    # e.g. "0..*"

    def parse_metadata(self):
        md = Metadata(self.parse_qualified_name())
        if self.accept(";"):
            return md
        self.expect("{")
        while not self.accept("}"):
            key = self.expect(kind="NAME").value
            self.expect("=")
            md.values[key] = self.parse_value()
            self.expect(";")
        return md

    def parse_value(self):
        tok = self.peek()
        if tok.kind == "STRING":
            self.pos += 1
            return tok.value[1:-1]
        if tok.kind == "NUMBER":
            self.pos += 1
            return float(tok.value) if "." in tok.value else int(tok.value)
        if tok.value in ("true", "false"):
            self.pos += 1
            return tok.value == "true"
        return self.parse_qualified_name()       # e.g. WireType::uint8_t

    def parse_qualified_name(self):
        parts = [self.expect(kind="NAME").value]
        while self.accept("::"):
            parts.append(self.expect(kind="NAME").value)
        return "::".join(parts)


def clean_doc(raw):
    """Strip /* */ and leading '*' from each line of a doc comment."""
    lines = [l.strip() for l in raw[2:-2].splitlines()]
    lines = [l[1:].strip() if l.startswith("*") else l for l in lines]
    return "\n".join(l for l in lines if l)


def parse_text(text):
    return Parser(tokenize(text)).parse_file()


def parse_files(paths):
    packages = []
    for path in paths:
        with open(path, encoding="utf-8") as f:
            packages += parse_text(f.read())
    return packages


# ---------------------------------------------------------------------------
# Extraction: SysML model -> same structure as reorder.load_messages()
# ---------------------------------------------------------------------------

def load_messages_sysml(paths):
    """Return {message name: [(wire type, field name), ...] in wire order}."""
    from tools.reorder import SIZES

    messages = {}
    for pkg in parse_files(paths):
        for el in pkg.children:
            if el.kind != "item def" or el.get_metadata("MavlinkMessage") is None:
                continue
            fields = []
            for attr in el.children:
                md = attr.get_metadata("MavlinkField")
                if md is None:
                    raise ParseError(f"{el.name}.{attr.name}: missing @MavlinkField")
                wire_type = md.values["wireType"].split("::")[-1]
                fields.append((wire_type, attr.name))
            messages[el.name] = sorted(fields, key=lambda tn: -SIZES[tn[0]])
    return messages


if __name__ == "__main__":
    from tools.reorder import crc_extra

    msgs = load_messages_sysml(["models/MavlinkMini.sysml"])
    for name, ordered in msgs.items():
        print(name, [n for t, n in ordered], crc_extra(name, ordered))